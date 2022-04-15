import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports


class GID:
    class camera:
        def __init__(self, index):
            self.cap = cv2.VideoCapture(index)
            self.hands = mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5)
            self.success, self.image = self.cap.read()
            self.results = self.hands.process(self.image)
        def update(self):
            self.success, self.image = self.cap.read()
        
        def get_hand_data(self):
            self.image.flags.writeable = False
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(self.image)
        
        def draw_hand_data(self):
            self.image.flags.writeable = True
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            if self.results.multi_hand_landmarks:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        self.image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(self.image, 1))
        
        def get_data(self):
            for hand_landmarks in self.results.multi_hand_landmarks:
                result = hand_landmarks.landmark
            return result
        
        def release(self):
            self.cap.release()
    
    def __init__(self):
        self.camera1 = self.camera(0)
        self.camera2 = self.camera(1)
        self.camera1_data = []
        self.camera2_data = []
        self.loop = 0
    
    def run(self):
        # while self.camera1.cap.isOpened():
        while self.camera1.cap.isOpened() and self.camera2.cap.isOpened():
            self.camera1.update()
            self.camera2.update()

            # if not self.camera1.success:
            if not self.camera1.success or not self.camera2.success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            self.camera1.get_hand_data()
            self.camera2.get_hand_data()
            
            
                
            self.camera1.draw_hand_data()
            # self.camera2.draw_hand_data()


            if(self.camera1.results.multi_hand_landmarks != None):
                self.camera1_data = self.camera1.get_data()
                # data = self.camera1.get_data()
                print(self.loop)
                print(self.camera1_data)

            if(self.camera2.results.multi_hand_landmarks != None):
                self.camera2_data = self.camera2.get_data()
                # data = self.camera2.get_data()
                print(self.loop)
                print(self.camera2_data)
            
            self.loop+=1
            if cv2.waitKey(5) & 0xFF == 27:
                break



    # def __init__(self):


# gid = GID()
# gid.run()
