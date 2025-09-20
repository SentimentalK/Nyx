import argparse
from nyx import Nyx

# 动态导入我们需要的游戏工厂
# 未来支持新游戏，只需要在这里加一个elif
def get_game_factory(game_name):
    if game_name.lower() == 'albion':
        from games.albion.factory import AlbionFactory
        return AlbionFactory()
    # elif game_name.lower() == 'stardew_valley':
    #     from games.stardew_valley.factory import StardewValleyFactory
    #     return StardewValleyFactory()
    else:
        raise ValueError(f"错误: 不支持的游戏 '{game_name}'")

def main():
    parser = argparse.ArgumentParser(description="Master Bot Framework")
    parser.add_argument("--game", type=str, default="albion", help="要运行的游戏插件名称 (例如: albion)")
    args = parser.parse_args()

    try:
        print(f"正在为游戏 '{args.game}' 创建工厂...")
        game_factory = get_game_factory(args.game)
        
        nyx = Nyx(game_factory)
        nyx.run()

    except Exception as e:
        print(f"程序启动失败或运行时发生严重错误: {e}")

if __name__ == "__main__":
    main()