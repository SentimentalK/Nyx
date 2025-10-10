# engine/debug_service.py
import cv2
import win32gui, win32con

class DebugService:
    def __init__(self, config):
        self.config = config
        self.is_topmost_set = False
        # 定义一个颜色映射表，方便状态类使用可读的颜色名称
        self.colors = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'yellow': (0, 255, 255),
            'purple': (255, 0, 255),
            'white': (255, 255, 255)
        }

    def render(self, base_image, draw_commands=None):
        """
        接收原始图像和一个绘制指令列表，然后渲染最终的调试视图。
        
        Args:
            base_image (numpy.ndarray): 未经修改的原始截图。
            draw_commands (list, optional): 包含绘制指令的字典列表。
                                             例如: [{'type': 'rectangle', 'rect': (x,y,w,h), 'color': 'red'}]
        """
        if not self.config['general']['debug_mode']:
            return

        # 创建一个副本进行绘制，以避免修改原始图像
        image_to_show = base_image.copy()

        # 1. 执行所有绘制指令
        if draw_commands:
            for cmd in draw_commands:
                color = self.colors.get(cmd.get('color', 'red'), (0, 0, 255)) # 默认红色
                
                if cmd['type'] == 'rectangle':
                    x, y, w, h = cmd['rect']
                    cv2.rectangle(image_to_show, (x, y), (x + w, y + h), color, 2)
                
                elif cmd['type'] == 'line':
                    cv2.line(image_to_show, cmd['start'], cmd['end'], color, 1)
                
                elif cmd['type'] == 'circle':
                    cv2.circle(image_to_show, cmd['center'], cmd['radius'], color, 2)
                
                # 未来可以轻松扩展更多指令，如 'text', 'arrow' 等

        # 2. 显示最终合成的图像
        window_name = self.config['general']['debug_window_name']
        cv2.imshow(window_name, image_to_show)

        # 3. 处理窗口置顶
        if not self.is_topmost_set:
            hwnd = win32gui.FindWindow(None, window_name)
            if hwnd:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                self.is_topmost_set = True