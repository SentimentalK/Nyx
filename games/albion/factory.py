import yaml
from pathlib import Path
from engine.factory import GameFactory

# 具体的游戏工厂实现
class AlbionFactory(GameFactory):
    def load_configuration(self):
        config_path = Path(__file__).parent / "config.yaml"
        print(f"正在从 {config_path} 加载Albion配置...")
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def create_initial_state(self, bot):
        # 导入具体的状态类
        from .states import AlbionFishingMinigameState
        # 返回我们为这个游戏设定的第一个状态
        return AlbionFishingMinigameState(bot)