import time
import cv2
from engine.vision_system import vision_system
from engine.control_system import control_system
from engine.debug_service import DebugService

class Nyx:
    def __init__(self, game_factory):
        print("正在初始化Bot...")
        self.config = game_factory.load_configuration()
        self.vision = vision_system
        self.control = control_system
        self.debug = DebugService(self.config)
        self.is_running = True
        
        # Bot持有一个对工厂的引用，以便状态可以从中获取信息
        self.game_factory = game_factory

        # 状态需要Bot的引用来访问共享的系统（vision, control, config）
        self.current_state = game_factory.create_initial_state(self)
        print(f"Bot初始化完成，初始状态: {self.current_state.__class__.__name__}")

    def run(self):
        print("Bot主循环已启动...")
        try:
            while self.is_running:
                next_state = self.current_state.execute()
                if next_state is None:
                    self.is_running = False
                    print("状态返回None，准备退出主循环。")
                elif self.current_state != next_state:
                    print(f"状态转换: {self.current_state.__class__.__name__} -> {next_state.__class__.__name__}")
                    self.current_state = next_state
        finally:
            self.cleanup()

    def cleanup(self):
        print("执行清理工作...")
        cv2.destroyAllWindows()
        print("Bot已停止。")