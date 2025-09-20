import cv2
import win32gui, win32con

class DebugService:
    def __init__(self, config):
        self.config = config
        self.is_topmost_set = False # 用于确保置顶只执行一次

    def render(self, image_to_show):
        """接收一个图像，并根据配置决定是否并如何显示它"""
        
        # 1. 检查调试模式是否开启，如果没有开启，则直接返回
        if not self.config['general']['debug_mode']:
            return

        window_name = self.config['general']['debug_window_name']
        
        # 2. 显示图像
        cv2.imshow(window_name, image_to_show)

        # 3. 处理窗口置顶（只执行一次）
        if not self.is_topmost_set:
            hwnd = win32gui.FindWindow(None, window_name)
            if hwnd:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                                     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                self.is_topmost_set = True