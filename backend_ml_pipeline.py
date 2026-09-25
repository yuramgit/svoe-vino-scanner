import cv2
import numpy as np
from PIL import Image
import io

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Нормализация фото: устранение бликов и контраст (CLAHE)"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Перевод в LAB для работы только с яркостью (устранение бликов)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    merged = cv2.merge((cl, a, b))
    final_img = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    return final_img

class SigLIPMock:
    """Заглушка для инференса. В продакшене загружаем ONNX/Torch модель SigLIP 2"""
    def get_embedding(self, image: np.ndarray) -> list[float]:
        # В реальности: прогон через torchvision/transformers
        # Возвращаем рандомный вектор размерности 768 для теста архитектуры
        return np.random.rand(768).tolist()