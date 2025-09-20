# 封装所有与视觉识别相关的操作 (策略模式 Strategy 的基础)
import cv2
import numpy as np
import mss

class VisionSystem:
    def __init__(self):
        self.sct = mss.mss()

    def grab_screen(self, roi):
        return np.array(self.sct.grab(roi))

    def find_template(self, screen_image, template_image, threshold, mask=None):
        """在指定图像中寻找模板，返回坐标和置信度"""
        gray_screen = cv2.cvtColor(screen_image, cv2.COLOR_BGRA2BGR)
        gray_screen = cv2.cvtColor(gray_screen, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray_screen, template_image, cv2.TM_CCOEFF_NORMED, mask=mask)
        _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            return max_loc, max_val
        return None, 0

# 创建一个全局单例
vision_system = VisionSystem()