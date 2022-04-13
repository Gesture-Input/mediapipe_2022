import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class camera:
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)
        self.hands = mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5)
        self.success, self.image = self.cap.read()
        self.results = self.hands.process(self.image)
        self.loop = 0
        
    def camera_update(self):
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
    
    def get_data(self, data):
        for hand_landmarks in data.multi_hand_landmarks:
            result = hand_landmarks.landmark
        return result
    
    def release(self):
        self.cap.release()
        
    def run(self):
        while self.cap.isOpened():
            self.camera_update()
            if not self.success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            
            self.get_hand_data()
            
            self.draw_hand_data()
            
            if(self.results.multi_hand_landmarks != None):
                data = self.get_data(self.results)
                print(self.loop)
                print(data)
            self.loop+=1
            if cv2.waitKey(5) & 0xFF == 27:
                break
        
        self.release()

camera1 = camera(0)
camera1.run()
