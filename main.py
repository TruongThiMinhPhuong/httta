import cv2
import numpy as np
from modules.gesturedetector import GestureDetector
from modules.data_saver import DataSaver
from configs.settings import COLORS

def main():
    # Khởi tạo các thành phần
    detector = GestureDetector()
    data_saver = DataSaver()
    cap = cv2.VideoCapture(0)
    
    # Thiết lập cửa sổ hiển thị
    cv2.namedWindow('Nhan dien cu chi tay', cv2.WINDOW_NORMAL)
    
    try:
        while cap.isOpened():
            # Đọc frame từ camera
            success, frame = cap.read()
            if not success:
                print("Không thể đọc frame từ camera")
                continue
            
            # Lật frame và chuyển đổi màu
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Nhận diện cử chỉ tay
            results = detector.hands.process(image)
            
            # Chuẩn bị hiển thị
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            gesture = "Khong phat hien tay"
            handedness = ""
            
            if results.multi_hand_landmarks:
                for hand_landmarks, hand_handedness in zip(
                    results.multi_hand_landmarks, 
                    results.multi_handedness
                ):
                    # Xác định tay trái/phải
                    handedness = hand_handedness.classification[0].label
                    
                    # Nhận diện cử chỉ
                    gesture = detector.recognize_gesture(hand_landmarks, handedness)
                    
                    # Vẽ bounding box và thông tin
                    h, w, _ = image.shape
                    landmark_array = np.array(
                        [(lm.x * w, lm.y * h) for lm in hand_landmarks.landmark]
                    )
                    x_min, y_min = np.min(landmark_array, axis=0)
                    x_max, y_max = np.max(landmark_array, axis=0)
                    
                    # Vẽ bounding box
                    cv2.rectangle(
                        image, 
                        (int(x_min)-20, int(y_min)-20), 
                        (int(x_max)+20, int(y_max)+20), 
                        COLORS.get(gesture, (255, 255, 255)), 
                        2
                    )
                    
                    # Vẽ thông tin cử chỉ
                    info_text = f"{handedness}: {gesture}"
                    cv2.putText(
                        image, 
                        info_text, 
                        (int(x_min)-20, int(y_min)-30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, 
                        COLORS.get(gesture, (255, 255, 255)), 
                        2
                    )
                    
                    # Lưu dữ liệu và hình ảnh
                    data_saver.save_gesture_data(gesture, handedness, frame, hand_landmarks)
            
            # Hiển thị frame
            cv2.imshow('Nhan dien cu chi tay', image)
            
            # Thoát khi nhấn ESC
            if cv2.waitKey(5) & 0xFF == 27:
                break
                
    except Exception as e:
        print(f"Co loi xay ra: {str(e)}")
        
    finally:
        # Giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()
        print("Ung dung da dung")

if __name__ == "__main__":
    main()