import time


def welcome():
    """欢迎仪式：打印欢迎横幅和问候信息"""
    banner = r"""
 ╔══════════════════════════════════════╗
 ║           Welcome!  欢迎              ║
 ╠══════════════════════════════════════╣
 ║      Hello, nice to meet you!        ║
 ╚══════════════════════════════════════╝
    """

    # 逐行打印，营造仪式感
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.05)

    print("\n🎉 欢迎来到 FastAPI 项目！\n")
    time.sleep(0.3)
    print("📁 当前文件：hello.py")
    print("🚀 准备好开始你的开发之旅了吗？\n")


if __name__ == "__main__":
    welcome()
