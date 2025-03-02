import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry, Calendar
from datetime import datetime, timedelta
import calendar

class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = '#aaa'
        self.default_fg_color = self['foreground']
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        self._add_placeholder()
    
    def _clear_placeholder(self, e=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(foreground=self.default_fg_color)
    
    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground=self.placeholder_color)

class TodoGUI:
    def __init__(self, todo_data):
        """初始化GUI"""
        self.todo_data = todo_data
        self.root = tk.Tk()
        self.root.title("Todo")  # 更简约的标题
        self.root.geometry("1200x800")  # 更大的窗口
        
        # 定义更现代的配色方案
        self.colors = {
            'primary': '#1A73E8',      # Google Blue
            'secondary': '#8AB4F8',    # Light Blue
            'success': '#34A853',      # Google Green
            'danger': '#EA4335',       # Google Red
            'warning': '#FBBC04',      # Google Yellow
            'text': '#202124',         # Dark Gray
            'text_secondary': '#5F6368',# Secondary Text
            'bg': '#FFFFFF',           # White
            'bg_secondary': '#F8F9FA', # Light Gray
            'border': '#DADCE0'        # Border Color
        }
        
        # 配置窗口
        self.root.configure(bg=self.colors['bg'])
        self.root.option_add('*Font', '微软雅黑 10')
        
        # 自定义样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置按钮样式
        self.style.configure(
            "Modern.TButton",
            padding=(20, 10),
            font=('微软雅黑', 10),
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            relief='flat'
        )
        
        # 配置输入框样式
        self.style.configure(
            "Modern.TEntry",
            padding=(10, 5),
            fieldbackground=self.colors['bg'],
            borderwidth=1,
            relief='solid'
        )
        
        # 配置标签框样式
        self.style.configure(
            "Modern.TLabelframe",
            background=self.colors['bg'],
            padding=15,
            borderwidth=1,
            relief='solid'
        )
        
        self.style.configure(
            "Modern.TLabelframe.Label",
            font=('微软雅黑', 12, 'bold'),
            foreground=self.colors['text'],
            background=self.colors['bg']
        )

        self.create_widgets()
        self.bind_events()
        self.refresh_list()
    
    def create_widgets(self):
        """创建界面元素"""
        # 创建主容器
        main_container = ttk.Frame(self.root, style="Modern.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 左侧面板（固定宽度）
        left_panel = ttk.Frame(main_container, width=400)  # 在Frame上设置宽度
        left_panel.pack_propagate(False)  # 防止pack改变frame的大小
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20))
        
        # 搜索框
        search_container = ttk.Frame(left_panel)
        search_container.pack(fill=tk.X, pady=(0, 20))
        
        search_frame = ttk.Frame(search_container, style="Modern.TFrame")
        search_frame.pack(fill=tk.X)
        
        self.search_var = tk.StringVar()
        search_entry = PlaceholderEntry(
            search_frame,
            placeholder="🔍 搜索任务...",
            font=('微软雅黑', 11),
            style="Modern.TEntry"
        )
        search_entry.pack(fill=tk.X, ipady=8)
        
        # 添加任务区域
        add_task_frame = ttk.LabelFrame(
            left_panel,
            text=" 新建任务 ",
            style="Modern.TLabelframe"
        )
        add_task_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 任务输入框
        self.todo_input = PlaceholderEntry(
            add_task_frame,
            placeholder="✍️ 输入任务内容...",
            font=('微软雅黑', 11),
            style="Modern.TEntry"
        )
        self.todo_input.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # 优先级选择
        priority_frame = ttk.Frame(add_task_frame)
        priority_frame.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Label(
            priority_frame,
            text="优先级",
            font=('微软雅黑', 10),
            foreground=self.colors['text_secondary']
        ).pack(side=tk.LEFT)
        
        self.priority_var = tk.StringVar(value="normal")
        priorities = [
            ("高", "high", "🔴"),
            ("中", "normal", "🟡"),
            ("低", "low", "🔵")
        ]
        
        for text, value, emoji in priorities:
            ttk.Radiobutton(
                priority_frame,
                text=f"{emoji} {text}",
                value=value,
                variable=self.priority_var,
                style="Modern.TRadiobutton"
            ).pack(side=tk.LEFT, padx=10)
        
        # 右侧面板（70%宽度）
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 日历视图
        calendar_frame = ttk.LabelFrame(
            right_panel,
            text=" 日历视图 ",
            style="Modern.TLabelframe"
        )
        calendar_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.month_calendar = Calendar(
            calendar_frame,
            locale='zh_CN',
            selectmode='day',
            cursor="hand1",
            background=self.colors['bg'],
            foreground=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            normalbackground=self.colors['bg'],
            normalforeground=self.colors['text'],
            weekendbackground=self.colors['bg_secondary'],
            weekendforeground=self.colors['primary'],
            othermonthforeground=self.colors['text_secondary'],
            othermonthbackground=self.colors['bg'],
            font=('微软雅黑', 10),
            borderwidth=0,
            headersbackground=self.colors['bg'],
            headersforeground=self.colors['text']
        )
        self.month_calendar.pack(fill=tk.X, padx=15, pady=15)
        
        # 任务列表
        list_frame = ttk.LabelFrame(
            right_panel,
            text=" 任务列表 ",
            style="Modern.TLabelframe"
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.todo_list = tk.Listbox(
            list_container,
            font=('微软雅黑', 11),
            selectmode=tk.SINGLE,
            activestyle='none',
            relief='flat',
            bg=self.colors['bg'],
            fg=self.colors['text'],
            selectbackground=self.colors['bg_secondary'],
            selectforeground=self.colors['primary'],
            borderwidth=0,
            highlightthickness=0
        )
        self.todo_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.todo_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.todo_list.configure(yscrollcommand=scrollbar.set)
        
        # 添加操作按钮
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        complete_btn = ttk.Button(
            button_frame,
            text="✅ 完成任务",
            command=self.toggle_complete,
            style="Modern.TButton"
        )
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(
            button_frame,
            text="🗑️ 删除任务",
            command=self.delete_todo,
            style="Modern.TButton"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # 添加状态栏
        status_frame = ttk.Frame(right_panel)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="加载中...")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('微软雅黑', 9),
            foreground=self.colors['text_secondary']
        )
        status_label.pack(side=tk.LEFT)
        
        # 添加截止日期和分类选择（之前漏掉的）
        # 截止日期选择
        due_frame = ttk.Frame(add_task_frame)
        due_frame.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Label(
            due_frame,
            text="截止日期",
            font=('微软雅黑', 10),
            foreground=self.colors['text_secondary']
        ).pack(side=tk.LEFT)
        
        self.due_date_var = tk.StringVar()
        self.calendar = DateEntry(
            due_frame,
            width=12,
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            locale='zh_CN',
            date_pattern='yyyy-mm-dd',
            textvariable=self.due_date_var,
            font=('微软雅黑', 10)
        )
        self.calendar.pack(side=tk.LEFT, padx=10)
        
        # 分类选择
        category_frame = ttk.Frame(add_task_frame)
        category_frame.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Label(
            category_frame,
            text="分类",
            font=('微软雅黑', 10),
            foreground=self.colors['text_secondary']
        ).pack(side=tk.LEFT)
        
        self.category_var = tk.StringVar(value="默认")
        self.category_combobox = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=["📁 默认", "💼 工作", "🏠 生活", "📚 学习"],
            state="readonly",
            font=('微软雅黑', 10),
            width=15
        )
        self.category_combobox.pack(side=tk.LEFT, padx=10)
        
        # 添加任务按钮
        add_btn = ttk.Button(
            add_task_frame,
            text="✨ 添加任务",
            command=self.add_todo,
            style="Modern.TButton"
        )
        add_btn.pack(fill=tk.X, padx=15, pady=10)
    
    def bind_events(self):
        """绑定事件"""
        self.todo_input.bind('<Return>', lambda e: self.add_todo())
        self.todo_list.bind('<Double-Button-1>', lambda e: self.toggle_complete())
    
    def refresh_list(self, filter_date=None):
        """刷新待办事项列表"""
        self.todo_list.delete(0, tk.END)
        
        for todo in self.todo_data.get_todos():
            # 如果指定了日期筛选，检查任务是否属于该日期
            if filter_date:
                todo_date = todo.get('due_date')
                if not todo_date:
                    continue
                try:
                    task_date = datetime.strptime(todo_date, "%Y-%m-%d").date()
                    if task_date != filter_date:
                        continue
                except ValueError:
                    continue
            
            # 构建显示文本
            status = "✓" if todo.get("completed", False) else "☐"
            priority_marks = {"high": "⚡", "normal": "○", "low": "▽"}
            priority_mark = priority_marks.get(todo.get("priority", "normal"), "○")
            
            display_text = f"{status} {priority_mark} [{todo.get('category', '默认')}] {todo['content']}"
            if todo.get("due_date"):
                display_text += f" (截止: {todo['due_date']})"
            
            self.todo_list.insert(tk.END, display_text)
        
        # 更新状态栏
        total, completed = self.todo_data.get_stats()
        if filter_date:
            self.status_var.set(f"{filter_date.strftime('%Y-%m-%d')} 的任务：共 {self.todo_list.size()} 项")
        else:
            self.status_var.set(f"共 {total} 项，已完成 {completed} 项")
    
    def add_todo(self):
        """添加待办事项"""
        content = self.todo_input.get().strip()
        if content and content != self.todo_input.placeholder:
            try:
                # 获取截止日期
                due_date = self.due_date_var.get().strip()
                if due_date and not self._is_valid_date(due_date):
                    messagebox.showwarning("警告", "请输入正确的日期格式：YYYY-MM-DD")
                    return
                
                # 添加待办事项
                self.todo_data.add_todo(
                    content=content,
                    due_date=due_date if due_date else None,
                    priority=self.priority_var.get(),
                    category=self.category_var.get()
                )
                
                # 清空输入
                self.todo_input.delete(0, tk.END)
                self.todo_input._add_placeholder()
                self.due_date_var.set("")
                self.priority_var.set("normal")
                self.category_var.set("默认")
                
                # 在添加成功后刷新日历
                self.refresh_calendar()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("错误", f"添加待办事项时出错：{str(e)}")
        else:
            messagebox.showwarning("警告", "请输入待办事项内容！")
    
    def delete_todo(self):
        """删除待办事项"""
        selection = self.todo_list.curselection()
        if selection:
            index = selection[0]
            self.todo_data.delete_todo(index)
            # 在删除成功后刷新日历
            self.refresh_calendar()
            self.refresh_list()
        else:
            messagebox.showinfo("提示", "请选择要删除的待办事项！")
    
    def toggle_complete(self):
        """切换完成状态"""
        selection = self.todo_list.curselection()
        if selection:
            index = selection[0]
            self.todo_data.toggle_complete(index)
            # 在切换状态后刷新日历
            self.refresh_calendar()
            self.refresh_list()
        else:
            messagebox.showinfo("提示", "请选择要切换状态的待办事项！")
    
    def on_search(self, *args):
        """搜索功能实现"""
        search_text = self.search_var.get().lower()
        self.todo_list.delete(0, tk.END)
        for todo in self.todo_data.get_todos():
            if search_text in todo["content"].lower():
                prefix = "✓ " if todo["completed"] else "☐ "
                self.todo_list.insert(tk.END, prefix + todo["content"])
    
    def _is_valid_date(self, date_str):
        """验证日期格式"""
        try:
            from datetime import datetime
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def refresh_calendar(self):
        """更新日历上的任务标记"""
        # 清除所有标记
        self.month_calendar.calevent_remove('all')
        
        # 添加所有任务到日历
        for todo in self.todo_data.get_todos():
            due_date = todo.get('due_date')
            if due_date:
                try:
                    date = datetime.strptime(due_date, "%Y-%m-%d").date()
                    # 根据优先级和完成状态设置不同的标记颜色
                    if todo.get('completed'):
                        color = self.colors['success']
                    else:
                        priority_colors = {
                            'high': self.colors['danger'],
                            'normal': self.colors['warning'],
                            'low': self.colors['secondary']
                        }
                        color = priority_colors.get(todo.get('priority', 'normal'))
                    
                    # 添加事件标记
                    self.month_calendar.calevent_create(
                        date,
                        todo['content'],
                        todo.get('category', '默认'),
                        color
                    )
                except ValueError:
                    continue
    
    def on_date_selected(self, event=None):
        """当选择日期时更新任务列表"""
        selected_date = self.month_calendar.get_date()
        try:
            date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            self.refresh_list(filter_date=date)
        except ValueError:
            self.refresh_list()
    
    def run(self):
        """运行应用"""
        self.root.mainloop() 