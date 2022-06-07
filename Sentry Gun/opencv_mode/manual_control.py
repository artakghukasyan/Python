import cv2
from stepper import stepper
class Manual():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.s = stepper()
    def manual_camera(self):
        
        while True:
            
            _,frame = self.cap.read()
            frame = cv2.resize(frame,(300,300),fx =0, fy = 0)
            
            
            h,w = frame.shape[:2]
            center_h = int(h / 2.0)
            center_w = int(w / 2.0)

            cv2.line(frame,(0,center_h),(w,center_h),(0,0,255),1)
            cv2.line(frame,(center_w,0),(center_w, h ),(0,0,255),1)
            
            frame = cv2.imshow("Frame", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('a'):
                self.left()
            if key == ord('d'):
                self.right()
            if key == ord('w'):
                self.up()
            if key == ord('s'):
                self.down()
        

        self.cap.release()
        cv2.destroyAllWindows()
    
    
    def right(self,):
        self.s.TURN_RIGHT(5)
    def left(self):
        self.s.TURN_LEFT(5)
    def up(self):
        self.s.TURN_RIGHT(5)
    def down(self):
        self.s.TURN_LEFT(5)
    

if __name__ == '__main__':
    m = Manual()
    m.manual_camera()