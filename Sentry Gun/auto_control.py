import cv2
import numpy as np
from centroidtracker import CentroidTracker
from non_max import non_max_suppression_fast
import os
from stepper import stepper
import threading
from servo import servo

class Auto:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.s = stepper()
        self.objectId = 0
        self.protopath = "MobileNet/MobileNetSSD_deploy.prototxt.txt"
        self.modelpath = "MobileNet/MobileNetSSD_deploy.caffemodel"
        self.detector = cv2.dnn.readNetFromCaffe(prototxt=self.protopath, caffeModel=self.modelpath)
        self.current_x_steps = 0
        self.current_y_steps = 0
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.W = 0
        self.H =0

        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


        self.list_id = []
        
    def Auto_camera(self):
        while True:
            rects = []
            
            if self.cap.isOpened():
                _,frame = self.cap.read()
                frame = cv2.resize(frame, (250,250), fx = 0, fy = 0)

                (self.H,self.W) = frame.shape[:2]
                rows,cols,_ = frame.shape
                center= int(cols/2)
                blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.W, self.H), 127.5)


                self.detector.setInput(blob)
                person_detections = self.detector.forward()
                for i in np.arange(0, person_detections.shape[2]):
                    confidence = person_detections[0, 0, i, 2]

                    if confidence > 0.2:
                        idx = int(person_detections[0, 0, i, 1])

                        if self.CLASSES[idx] != "person":
                            continue

                        person_box = person_detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                        (startX, startY, endX, endY) = person_box.astype("int")
                        rects.append(person_box)


                boundingboxes = np.array(rects)
                boundingboxes = boundingboxes.astype('int')
                rects = non_max_suppression_fast(boundingboxes, 0.3)

        
                tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)
                objects = tracker.update(rects)
                for (self.objectId, bbox) in objects.items():
                    self.x1, self.y1, self.x2, self.y2 = bbox
                    self.x1 = int(self.x1)
                    self.y1 = int(self.y1)
                    self.x2 = int(self.x2)
                    self.y2 = int(self.y2)
                                
                    cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)
                    text = "ID: {}".format(self.objectId)
                    cv2.putText(frame, text, (self.x1, self.y1-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 255), 1)
                    print(self.x1,self.x2,self.y1,self.y2)
                if self.objectId not in self.list_id:
                    self.list_id.append(self.objectId)

                
                if len(rects) > 0:
                    cv2.putText(frame, 'STATUS: DETECTED', (0,10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 0), 1) 
                else:
                    cv2.putText(frame, 'STATUS: NOT DETECTED', (0,10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 255), 1)			 
            
            cv2.imshow('frame',frame)
            threading.Thread(target = self.x_axis).start()  
            key = cv2.waitKey(1)
            
            if key == ord('q'):
                break
            
    
        self.cap.release()
        cv2.destroyAllWindows()
    def x_axis(self):
        target_steps_x = (2*30*(self.x1+self.x2 /2)/self.H) - 30
        target_steps_y = (2*15*(self.y1+self.y2 /2)/self.W) - 15
        print("T_X",target_steps_x)
        print("T_Y",target_steps_y)
        t_x = threading.Thread()
        t_y = threading.Thread()
        t_fire = threading.Thread()
        
        if (target_steps_x - self.current_x_steps) > 0:
            self.current_x_steps += 1
            if False:
                t_x = threading.Thread(target = self.right, args = (3,))
            else:
                t_x = threading.Thread(target = self.left, args = (3,))
        elif (target_steps_x - self.current_x_steps) < 0:
            self.current_x_steps -= 1
            if False:
                t_x = threading.Thread(target = self.left, args = (3,))
            else:
                t_x = threading.Thread(target = self.right, args = (3,))
                
        if (target_steps_y - self.current_y_steps) > 0:
            self.current_y_steps += 1
            if False:
                t_y = threading.Thread(target = self.up, args = (3,))
            else:
                t_y = threading.Thread(target = self.down, args = (3,))
        elif (target_steps_y - self.current_y_steps) < 0:
            self.current_y_steps -= 1
            if False:
                t_y = threading.Thread(target = self.up, args = (3,))
            else:
                t_y = threading.Thread(target = self.down, args = (3,))
                
        

        t_x.start()
        t_y.start()
        t_x.join()
        t_y.join()
                
                
                
    def right(self,steps):
        self.s.TURN_RIGHT(steps)
    
    def left(self,steps):
        self.s.TURN_LEFT(steps)
        
    def up(self,steps):
        servo()
        
    def down(self,steps):
        servo()
                
        
        
if __name__ == '__main__':
    a = Auto()
    a.Auto_camera()


        