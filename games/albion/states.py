# 实现Albion游戏的所有具体状态
import cv2
import random
import win32gui, win32con
from engine.states import BotState

class AlbionFishingMinigameState(BotState):
    def __init__(self, bot):
        super().__init__(bot)
        self.is_mouse_pressed = False
        self.window_set_topmost = False

        # 从工厂获取模板图片路径并加载
        template_path = "games/albion/templates/bobber.png"
        
        # 加载模板和蒙版
        self.bobber_color = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if self.bobber_color is None:
            raise FileNotFoundError(f"未找到模板文件: {template_path}")
            
        self.bobber_gray = cv2.cvtColor(self.bobber_color, cv2.COLOR_BGR2GRAY)
        _, self.bobber_mask = cv2.threshold(self.bobber_gray, 0, 255, cv2.THRESH_BINARY)
        self.template_w, self.template_h = self.bobber_gray.shape[::-1]
        print("钓鱼小游戏状态初始化，模板加载成功。")

    def execute(self):
        # --- 1. 从配置中读取参数 ---
        roi = self.bot.config['fishing']['minigame_roi']
        threshold = self.bot.config['vision']['confidence_threshold']
        min_p, max_p = self.bot.config['fishing']['release_threshold_range'].values()
        
        # --- 2. 生成动态阈值 ---
        random_percentage = random.uniform(min_p, max_p)
        dynamic_release_threshold = int(roi['width'] * random_percentage)

        # --- 3. 视觉识别 ---
        screen_image = self.bot.vision.grab_screen(roi)
        location, confidence = self.bot.vision.find_template(
            screen_image, self.bobber_gray, threshold, mask=self.bobber_mask
        )
        
        bobber_center_x = -1
        if location:
            bobber_center_x = location[0] + self.template_w // 2

        # --- 4. 决策逻辑 ---
        if bobber_center_x != -1:
            if bobber_center_x < dynamic_release_threshold:
                if not self.is_mouse_pressed:
                    self.bot.control.mouse_down()
                    self.is_mouse_pressed = True
                    print(f"状态: ...左侧 ({bobber_center_x} < {dynamic_release_threshold})，按下")
            else:
                if self.is_mouse_pressed:
                    self.bot.control.mouse_up()
                    self.is_mouse_pressed = False
                    print(f"状态: ...右侧 ({bobber_center_x} >= {dynamic_release_threshold})，松开")
        else:
            if self.is_mouse_pressed:
                self.bot.control.mouse_up()
                self.is_mouse_pressed = False
                print("状态: 识别丢失，松开 (安全模式)")

        # --- 5. Debug视图 ---
        if self.bot.config['general']['debug_mode']:
            # 创建一个空的绘制指令列表
            draw_commands = []
            
            # 如果找到了目标，就添加一个“画矩形”的指令
            if location:
                rect_data = (location[0], location[1], self.template_w, self.template_h)
                draw_commands.append({'type': 'rectangle', 'rect': rect_data, 'color': 'red'})
            
            # 添加一个“画线”的指令
            line_start = (dynamic_release_threshold, 0)
            line_end = (dynamic_release_threshold, roi['height'])
            draw_commands.append({'type': 'line', 'start': line_start, 'end': line_end, 'color': 'purple'})

            # 将原始图像和指令列表一起交给DebugService
            self.bot.debug.render(screen_image, draw_commands)

        # --- 6. 检查退出 ---
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if self.is_mouse_pressed: self.bot.control.mouse_up()
            return None # 返回None表示结束

        # 默认情况下，保持在当前状态
        return self