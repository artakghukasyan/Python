import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image
from PIL import ImageTk
import time
import numpy as np
from centroidtracker import CentroidTracker
from non_max import non_max_suppression_fast
import smtplib
import os
from email.message import EmailMessage
import imghdr
import threading
from stepper import stepper
import sys
#from test import stepper



class App(threading.Thread):
	def __init__(self,is_true):
		super().__init__()
        #Raspberry pi setup
		threading.Thread.__init__(self)
		self.s = stepper()
		self.rl_x = 0
		# Root Settings  
		self.is_true = is_true
		self.root = tk.Tk()
		self.root.config(bg="#2A2E37")
		self.root.geometry('1000x500')
		self.root.bind('<Escape>', self.end_fullscreen)
		self.root.bind('<F11>', self.start_fullscreen)


		#MobileNet settings
		self.objectId = 0
		self.protopath = "MobileNet/MobileNetSSD_deploy.prototxt.txt"
		self.modelpath = "MobileNet/MobileNetSSD_deploy.caffemodel"
		self.detector = cv2.dnn.readNetFromCaffe(prototxt=self.protopath, caffeModel=self.modelpath)


		self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


		self.list_id = []
		# If it's True
		if self.is_true:
			is_true = True
		else:
			self.root.destroy()



		#Right Frame
		self.right_frame = tk.Frame(self.root , width = self.root.winfo_screenwidth() ,height = self.root.winfo_screenheight(), bg = '#2A2E37')
		self.right_frame.pack(side=  'right')

		

		self.start_button = tk.Button(self.right_frame, text = 'START', width = 15,highlightthickness = 0, font = ("Calibri", 13, 'bold'),bg = '#FD7D00', command = self.start_camera)
		self.stop_button = tk.Button(self.right_frame, text = 'EXIT', width = 15,highlightthickness=0, font = ("Calibri", 13, 'bold'),bg = '#FD7D00', command = self.stop_camera)
		self.start_button.grid(row = 1, column = 0, pady = 50, padx = 50, stick = 'nsew')
		self.stop_button.grid(row = 1, column = 1, pady = 50, padx = 50, stick = 'nsew')


		#Left Frame



		self.detected_label = tk.Label(self.root, text = 'STATUS: NOT DETECTED', font = ("Calibri", 15, 'bold'), bg = '#1A1D22', fg = 'red')
		self.detected_label.place(x =0 , y = 0)



		self.button_manual = tk.Button(self.root, text = 'MANUAL', font = ("Calibri", 13, 'bold'),width = 15, bg= '#6200EE', command = self.manual)
		self.button_automatic = tk.Button(self.root, text = 'AUTOMATIC', font = ("Calibri", 13, 'bold'),width = 15, bg= '#6200EE',command = self.start_camera)
		self.button_manual.place(x = 50, y = 70)
		self.button_automatic.place(x = 50, y = 150)

		

		# Video Capture
		self.video = cv2.VideoCapture(0)
		self.video.release()
		cv2.destroyAllWindows()
		self.no_image = ImageTk.PhotoImage(Image.open('Images/no_video.png'))
		#self.cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		self.camera_frame = tk.Label(self.right_frame,image = self.no_image, bg ='#2A2E37')
		self.camera_frame.grid(column = 0, row =0, columnspan = 3, padx = 20)

		self.button_email = tk.Button(self.root, text = "SEND MAIL", font = ("Calibri", 13,'bold'), width = 15, bg = '#6200EE', command = self.send_email)
		self.button_email.place(x = 50, y = 220)

	#Automatic Mode

	def camera(self): 
		rects = []
		if self.video.isOpened():
			_,frame = self.video.read()
			frame = cv2.resize(frame, (200,200), fx = 0, fy = 0)

			(H,W) = frame.shape[:2]

			blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)


			self.detector.setInput(blob)
			person_detections = self.detector.forward()
			for i in np.arange(0, person_detections.shape[2]):
				confidence = person_detections[0, 0, i, 2]

				if confidence > 0.2:
					idx = int(person_detections[0, 0, i, 1])

					if self.CLASSES[idx] != "person":
						continue

					person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
					(startX, startY, endX, endY) = person_box.astype("int")
					rects.append(person_box)
				
			
			boundingboxes = np.array(rects)
			boundingboxes = boundingboxes.astype('int')
			rects = non_max_suppression_fast(boundingboxes, 0.3)

			
			tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)
			objects = tracker.update(rects)
			for (self.objectId, bbox) in objects.items():
 				x1, y1, x2, y2 = bbox
 				x1 = int(x1)
 				y1 = int(y1)
 				x2 = int(x2)
 				y2 = int(y2)
 				cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
 				text = "ID: {}".format(self.objectId)
 				cv2.putText(frame, text, (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
 				#print(x1,x2,y1,y2)
			if self.objectId not in self.list_id:
				self.list_id.append(self.objectId)


			if len(rects) > 0:
				self.detected_label.config(text = f'STATUS: DETECTED {len(rects)} ', fg = 'green') 
			else:
				self.detected_label.config(text = 'STATUS: NOT DETECTED', fg = 'red') 
					
			

			frame = Image.fromarray(frame)
			frame = ImageTk.PhotoImage(frame)
			self.camera_frame.config(image=frame)
			self.camera_frame.image= frame
			self.camera_frame.after(1, self.camera)

	#Manual Mode
	def manual_camera(self):
		self.root.bind('<Left>', self.left_key)
		self.root.bind('<Right>', self.right_key)
		self.root.bind('<Up>', self.up_key)
		self.root.bind('<Down>', self.down_key)
		self.root.bind('<f>', self.f_key)
		
		_,frame = self.video.read()
		frame = cv2.resize(frame, (250,250), fx = 0, fy = 0)
		
		h,w = frame.shape[:2]
		center_h = int(h / 2.0)
		center_w = int(w / 2.0)
		
		cv2.line(frame,(0,center_h),(w,center_h),(255,0,0),1)
		cv2.line(frame,(center_w,0),(center_w, h ),(255,0,0),1)

		frame = Image.fromarray(frame)
		frame = ImageTk.PhotoImage(frame)
		self.camera_frame.config(image=frame)
		self.camera_frame.image= frame
		self.camera_frame.after(1, self.manual_camera)
		
	def start_camera(self):
		self.video = cv2.VideoCapture(0)
		self.button_manual.config(command = self.do_nothing, fg = 'gray', bg = '#eee')
		self.start_button.config(command = self.do_nothing, fg = 'gray', bg = '#eee')
		self.button_automatic.config(command = self.do_nothing, fg = 'gray', bg = '#eee')
		self.camera()

	def manual(self):
		self.video = cv2.VideoCapture(0)
		self.start_button.config(command = self.do_nothing, fg = 'gray', bg = '#eee')
		self.button_manual.config(command = self.do_nothing, fg = 'gray', bg = '#eee')
		self.button_automatic.config(command = self.do_nothing, fg = 'gray', bg = '#eee')
		self.manual_camera()

	def left_key(self,event):
		self.rl_x = self.rl_x + 5
		
		if self.rl_x == 70:
		   self.s.TURN_RIGHT(90)
		   self.rl_x = 0
		   
		self.s.TURN_LEFT(5)        
		
		
	def right_key(self,event):
		self.rl_x = self.rl_x - 5
		
		if self.rl_x == -70:
		   self.s.TURN_LEFT(90)
		   self.rl_x = 0
		   
		self.s.TURN_RIGHT(5)        
		
		
	def up_key(self,event = None):
		print("Up")

	def down_key(self,event = None):
		self.s.TURN_LEFT(50)

	def f_key(self,event = None):
		print("F")

	def do_nothing(slef):
		pass


	def send_email(self):


		sender = 'artakghukasyansentrygun@gmail.com'
		receiver = 'artakbala@gmail.com'
		password = 'egomovztnimrqqmz'

		if self.video.isOpened():
			path = r'/home/pi/Desktop/Sentry Gun/Images'
			_,frame = self.video.read()
			cv2.imwrite(os.path.join(path, 'sentry.jpg'), frame)

			try:

				with open('Images/sentry.jpg', 'rb') as f:
					img_data = f.read()

				msg = EmailMessage()
				msg['Subject'] = 'Sentry'
				msg['From'] = sender
				msg['To'] = receiver
				msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
				msg.add_attachment(img_data, maintype = 'image',subtype=imghdr.what(None, img_data))
				smpt = smtplib.SMTP('smtp.gmail.com',587)
				smpt.ehlo()
				smpt.starttls()
				smpt.ehlo()
				smpt.login(sender, password)
				smpt.sendmail(sender,receiver, msg.as_string())
				smpt.quit()
				os.remove('Images/sentry.jpg')
				messagebox.showinfo("Succes ", "Email Successfuly Sent!")
			except Exception as e:
				messagebox.showerror("Error", e)
		else:
			messagebox.showerror("Error","Press Start before sending email")



	def stop_camera(self):
		self.video.release()
		cv2.destroyAllWindows()
		self.camera_frame.config(image =self.no_image)
		self.detected_label.config(text= 'STATUS: NOT DETECTED', fg = 'red')
		self.start_button.config(command = self.start_camera, fg = '#000', bg = '#FD7D00')
		self.button_automatic.config(command = self.start_camera, fg = '#000', bg = '#6200EE')
		self.button_manual.config(command = self.manual, fg = '#000', bg = '#6200EE')
		self.root.destroy()

	def end_fullscreen(self,event = None):
		self.root.attributes('-fullscreen', False)

	def start_fullscreen(self,event = None):
		self.root.attributes('-fullscreen', True)




if __name__ == '__main__':
	app = App(True)
	app.root.mainloop()