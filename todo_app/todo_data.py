import json
import os
from datetime import datetime
import logging

logging.basicConfig(
    filename='data/todo_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TodoData:
    def __init__(self, filename="data/todos.json"):
        """初始化数据管理器"""
        self.filename = filename
        self.todos = []
        self._ensure_data_dir()
        self.load_todos()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
    
    def load_todos(self):
        """从文件加载待办事项"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
        except Exception as e:
            print(f"加载数据时出错: {e}")
            self.todos = []
    
    def save_todos(self):
        """保存待办事项到文件"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据时出错: {e}")
    
    def add_todo(self, content, due_date=None, priority="normal", category="默认"):
        """添加新待办事项"""
        try:
            todo = {
                "content": content,
                "completed": False,
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "due_date": due_date,  # 新增截止日期字段
                "priority": priority,
                "category": category  # 新增分类字段
            }
            self.todos.append(todo)
            self.save_todos()
            logging.info(f"添加新待办事项: {content}")
        except Exception as e:
            logging.error(f"添加待办事项时出错: {e}")
            raise
    
    def delete_todo(self, index):
        """删除指定待办事项"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self.save_todos()
    
    def toggle_complete(self, index):
        """切换完成状态"""
        if 0 <= index < len(self.todos):
            self.todos[index]["completed"] = not self.todos[index]["completed"]
            self.save_todos()
    
    def get_todos(self):
        """获取所有待办事项"""
        return self.todos
    
    def get_stats(self):
        """获取统计信息"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo["completed"])
        return total, completed
    
    def backup_data(self):
        """备份数据"""
        backup_file = f"data/todos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(self.filename, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as target:
                    target.write(source.read())
            return True
        except Exception as e:
            print(f"备份数据时出错: {e}")
            return False

    def export_todos(self, filename):
        """导出待办事项"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出数据时出错: {e}")
            return False

    def import_todos(self, filename):
        """导入待办事项"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_todos = json.load(f)
                self.todos.extend(imported_todos)
                self.save_todos()
            return True
        except Exception as e:
            print(f"导入数据时出错: {e}")
            return False 