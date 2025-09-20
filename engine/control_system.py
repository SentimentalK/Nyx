# 封装所有与鼠标键盘控制相关的操作 (外观模式 Facade)
import pyautogui

class ControlSystem:
    def __init__(self):
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False

    def mouse_down(self, button='left'):
        pyautogui.mouseDown(button=button)

    def mouse_up(self, button='left'):
        pyautogui.mouseUp(button=button)

# 创建一个全局单例，方便各处调用
control_system = ControlSystem()