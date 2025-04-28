import os
from pathlib import Path

# Đường dẫn cơ bản
BASE_DIR = Path(__file__).resolve().parent.parent

# Cấu hình MediaPipe
MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'max_num_hands': 2,
    'min_detection_confidence': 0.8,
    'min_tracking_confidence': 0.5
}

# Màu sắc cho các cử chỉ
COLORS = {
"Nam tay": (255, 0, 0), # Xanh lam
"Mo ban tay": (0, 255, 0), # Xanh lá
"Ngon cai gio len": (0, 0, 255), # Đỏ
"Ngon tro chi": (255, 255, 0), # Vàng
"Khong phat hien tay": (255, 255, 255) # Trắng
}

# Cấu hình lưu dữ liệu
SAVE_DATA = True
DATA_FORMAT = 'csv'  # 'csv', 'json' hoặc 'txt'
# Thêm vào configs/settings.py

# Cấu hình lưu hình ảnh
IMAGE_SAVE_CONFIG = {
    'enabled': True,  # Bật/tắt lưu hình ảnh
    'quality': 95,    # Chất lượng ảnh (0-100)
    'resize': None    # Kích thước resize (width, height) hoặc None để giữ nguyên
}