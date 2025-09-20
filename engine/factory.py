# 定义游戏插件的抽象工厂基类 (抽象工厂模式 Abstract Factory)
from abc import ABC, abstractmethod

class GameFactory(ABC):
    @abstractmethod
    def load_configuration(self):
        pass

    @abstractmethod
    def create_initial_state(self, bot):
        pass