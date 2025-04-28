import os
import cv2
import json
from datetime import datetime
from pathlib import Path
from configs.settings import BASE_DIR

class DataSaver:
    def __init__(self):
        self.base_data_dir = BASE_DIR / 'data'
        self._create_folders()
    
    def _create_folders(self):
        """Create folders for each gesture type"""
        self.gesture_folders = {
            "Nam tay": self.base_data_dir / "nam_tay",
            "Mo ban tay": self.base_data_dir / "mo_ban_tay",
            "Ngon cai gio len": self.base_data_dir / "ngon_cai",
            "Ngon tro chi": self.base_data_dir / "ngon_tro",
            "Khong phat hien tay": self.base_data_dir / "unknown"
        }
        
        # Create folders if they don't exist
        for folder in self.gesture_folders.values():
            folder.mkdir(parents=True, exist_ok=True)
    
    def save_gesture_data(self, gesture, handedness, frame, landmarks):
        """Save data to gesture-specific folder"""
        if gesture not in self.gesture_folders:
            gesture = "Khong phat hien tay"
            
        gesture_folder = self.gesture_folders[gesture]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        # Save image
        img_filename = f"{timestamp}_{handedness}.jpg"
        img_path = gesture_folder / img_filename
        cv2.imwrite(str(img_path), frame)
        
        # Save metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "gesture": gesture,
            "handedness": handedness,
            "image_path": str(img_path.relative_to(BASE_DIR)),
            "landmarks": self._serialize_landmarks(landmarks)
        }
        
        metadata_path = gesture_folder / f"{timestamp}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    def _serialize_landmarks(self, landmarks):
        """Convert landmarks to serializable format"""
        if landmarks is None:
            return None
            
        return {
            str(idx): {"x": lm.x, "y": lm.y, "z": lm.z}
            for idx, lm in enumerate(landmarks.landmark)
        }