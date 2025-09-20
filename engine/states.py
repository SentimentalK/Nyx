# 定义状态机的抽象基类 (状态模式 State)
from abc import ABC, abstractmethod

class BotState(ABC):
    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def execute(self):
        """执行当前状态的逻辑，并返回下一个状态"""
        pass