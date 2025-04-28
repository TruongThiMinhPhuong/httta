import math
import mediapipe as mp
from configs.settings import MEDIAPIPE_CONFIG, COLORS

class GestureDetector:
    def __init__(self):
        self._init_hands_detector()
        
    def _init_hands_detector(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(**MEDIAPIPE_CONFIG)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
    
    @staticmethod
    def calculate_distance(point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def is_finger_extended(self, tip, pip, mcp, wrist):
        angle = math.degrees(math.atan2(tip.y - pip.y, tip.x - pip.x) - 
                            math.atan2(mcp.y - pip.y, mcp.x - pip.x))
        distance_tip_wrist = self.calculate_distance(tip, wrist)
        distance_mcp_wrist = self.calculate_distance(mcp, wrist)
        return angle < 0 and distance_tip_wrist > distance_mcp_wrist
    
    def recognize_gesture(self, landmarks, handedness):
        wrist = landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
        
        # Lấy các điểm landmark cho từng ngón
        fingers = []
        for finger_tip, finger_pip, finger_mcp in [
            (mp.solutions.hands.HandLandmark.THUMB_TIP, mp.solutions.hands.HandLandmark.THUMB_IP, mp.solutions.hands.HandLandmark.THUMB_MCP),
            (mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP, mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP, mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP),
            (mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP, mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP, mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP),
            (mp.solutions.hands.HandLandmark.RING_FINGER_TIP, mp.solutions.hands.HandLandmark.RING_FINGER_PIP, mp.solutions.hands.HandLandmark.RING_FINGER_MCP),
            (mp.solutions.hands.HandLandmark.PINKY_TIP, mp.solutions.hands.HandLandmark.PINKY_PIP, mp.solutions.hands.HandLandmark.PINKY_MCP)
        ]:
            tip = landmarks.landmark[finger_tip]
            pip = landmarks.landmark[finger_pip]
            mcp = landmarks.landmark[finger_mcp]
            fingers.append(self.is_finger_extended(tip, pip, mcp, wrist))
        
        extended_count = sum(fingers)
        
        if extended_count == 0:
            return "Nam tay"
        elif extended_count == 5:
            return "Mo ban tay"
        elif extended_count == 1 and fingers[0]:  # Ngón cái
            return "Ngon cai gio len"
        elif extended_count == 1 and fingers[1]:  # Ngón trỏ
            return "Ngon tro chi"
        
        return "Cu chi khac"