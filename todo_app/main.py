from todo_data import TodoData
from todo_gui import TodoGUI

def main():
    # 创建数据管理器
    todo_data = TodoData()
    
    # 创建并运行GUI
    app = TodoGUI(todo_data)
    app.run()

if __name__ == "__main__":
    main() 