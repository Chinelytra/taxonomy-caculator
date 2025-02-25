import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, getcontext

# 设置 Decimal 精度
getcontext().prec = 10

# 创建主窗口
window = tk.Tk()
window.title("测量计算器")
window.geometry("450x700")

# 配置网格行列
for col in range(5):
    window.columnconfigure(col, weight=1, uniform='col')
for row in range(10):  # 增加一行以容纳所有按钮
    window.rowconfigure(row, weight=1, uniform='row')

# 全局变量
first_number = None
operator = None
history = []
error_state = False
is_new_number = True

# 创建显示区域
display_frame = tk.Frame(window)
display_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")

# 显示输入框
display = tk.Entry(display_frame, font=("Arial", 20), justify="right")
display.pack(fill=tk.BOTH, expand=True)
display.insert(0, "0")

# 历史记录区域
history_frame = tk.Frame(window)
history_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", rowspan=2)

history_label = tk.Label(history_frame, text="历史记录：", anchor="w")
history_label.pack(fill=tk.X)

history_text = tk.Text(history_frame, height=8, font=("Arial", 10), state=tk.DISABLED)
history_text.pack(fill=tk.BOTH, expand=True)

# 更新历史记录显示
def update_history():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    for entry in history[-4:]:  # 显示最近4条记录
        history_text.insert(tk.END, entry + "\n")
    history_text.config(state=tk.DISABLED)
    history_text.see(tk.END)

# 更新显示
def update_display(value):
    global error_state
    display.delete(0, tk.END)
    display.insert(0, str(value))
    error_state = False

# 数字按钮点击
def number_click(num):
    global is_new_number
    if error_state:
        return
    if is_new_number:
        update_display(num)
        is_new_number = False
    else:
        current = display.get()
        update_display(current + num)

# 小数点按钮点击
def dot_click():
    global is_new_number
    if error_state:
        return
    current = display.get()
    if "." not in current:
        update_display(current + ".")
        is_new_number = False

# 操作符按钮点击
def operator_click(op):
    global first_number, operator, is_new_number, error_state
    if error_state:
        return
    try:
        current_value = Decimal(display.get())
        if first_number is None:
            first_number = current_value
            operator = op
            history.append(f"{first_number} {op} ")
        else:
            second_number = current_value
            result = perform_calculation(first_number, operator, second_number)
            if result is not None:
                update_display(result)
                first_number = result
                history[-1] += f"{second_number} = {result}"
                history.append(f"{result} {op} ")
            else:
                return
        is_new_number = True
        update_history()
    except Exception as e:
        handle_error(str(e))

# 执行计算
def perform_calculation(first, op, second):
    try:
        if op == "+":
            result = first + second
        elif op == "-":
            result = first - second
        elif op == "×" or op == "*":
            result = first * second
        elif op == "÷" or op == "/":
            if second == 0:
                raise ZeroDivisionError
            result = first / second
        else:
            return None
        return result
    except Exception as e:
        handle_error(str(e))
        return None

# 处理错误
def handle_error(message):
    global error_state
    error_state = True
    messagebox.showerror("错误", message)
    update_display("错误")
    history.append(f"错误：{message}")
    update_history()

# 等于按钮点击
def equal_click(event=None):
    global first_number, operator, is_new_number, error_state
    if error_state or operator is None:
        return
    try:
        second_number = Decimal(display.get())
        result = perform_calculation(first_number, operator, second_number)
        if result is not None:
            update_display(result)
            history[-1] += f"{second_number} = {result}"
            update_history()
            first_number = None
            operator = None
            is_new_number = True
    except Exception as e:
        handle_error(str(e))

# 退格按钮点击
def backspace_click():
    if error_state:
        return
    current = display.get()
    if len(current) > 1:
        update_display(current[:-1])
    else:
        update_display("0")

# 固定小数按钮（0.0 和 0.00）
def decimal_click(precision):
    global is_new_number
    if error_state:
        return
    if is_new_number:
        update_display(precision)
    else:
        current = display.get()
        update_display(current + precision)
    is_new_number = False

# 自定义值按钮点击
def custom_value_click(value):
    global is_new_number
    update_display(str(value))
    is_new_number = False
    history.append(f"输入常量：{value}")
    update_history()

# 清除按钮点击
def clear_click():
    global first_number, operator, is_new_number, history
    first_number = None
    operator = None
    is_new_number = True
    history.clear()  # 一次性清空历史记录
    update_display("0")
    update_history()

# 键盘事件处理
def handle_keypress(event):
    key = event.char
    if key == "\b":  # 退格键
        backspace_click()
    elif key in "0123456789":
        number_click(key)
    elif key == ".":
        dot_click()
    elif key in "+-*/":
        operator_click(key if key != "*" else "×")
    elif key == "=" or key == "\r":
        equal_click()
    elif key.lower() == "c":
        clear_click()

# 按钮配置
buttons = [
    ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("÷", 3, 3), ("×", 3, 4),
    ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("+", 4, 4),
    ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("0", 5, 3), ("=", 5, 4),
    ("C", 6, 0), (".", 6, 1), ("←", 6, 2), ("0.0", 6, 3), ("0.00", 6, 4),
    ("0.67x-0.0556", 7, 0), ("0.8x-0.0471", 7, 1), ("1x-0.0378", 7, 2),
    ("1.2x-0.0310", 7, 3), ("1.5x-0.0250", 7, 4),
    ("2x-0.0185", 8, 0), ("2.5x-0.0152", 8, 1), ("3x-0.0126", 8, 2),
    ("3.5x-0.0109", 8, 3), ("4x-0.0095", 8, 4),
    ("4.5x-0.0083", 9, 0)  # 单独一行，确保大小一致
]

# 自定义按钮值
custom_values = {
    "0.67x-0.0556": Decimal('0.0556'),
    "0.8x-0.0471": Decimal('0.0471'),
    "1x-0.0378": Decimal('0.0378'),
    "1.2x-0.0310": Decimal('0.0310'),
    "1.5x-0.0250": Decimal('0.0250'),
    "2x-0.0185": Decimal('0.0185'),
    "2.5x-0.0152": Decimal('0.0152'),
    "3x-0.0126": Decimal('0.0126'),
    "3.5x-0.0109": Decimal('0.0109'),
    "4x-0.0095": Decimal('0.0095'),
    "4.5x-0.0083": Decimal('0.0083')
}

# 创建按钮
for (text, row, col) in buttons:
    btn_bg = "light blue" if text in custom_values else None
    btn_font = ("Arial", 12) if text not in ["0.0", "0.00"] and text not in custom_values else ("Arial", 10) if text in ["0.0", "0.00"] else ("Arial", 8)

    if text in "0123456789":
        cmd = lambda x=text: number_click(x)
    elif text == ".":
        cmd = dot_click
    elif text in "+-×÷":
        cmd = lambda x=text: operator_click(x)
    elif text == "=":
        cmd = equal_click
    elif text == "C":
        cmd = clear_click
    elif text == "←":
        cmd = backspace_click
    elif text in ["0.0", "0.00"]:
        cmd = lambda x=text: decimal_click(x)
    elif text in custom_values:
        cmd = lambda x=custom_values[text]: custom_value_click(x)

    btn = tk.Button(
        window,
        text=text,
        font=btn_font,
        bg=btn_bg,
        command=cmd
    )
    btn.grid(
        row=row,
        column=col,
        padx=2,
        pady=2,
        sticky="nsew"
    )

# 绑定键盘事件
window.bind("<Key>", handle_keypress)

# 启动主循环
window.mainloop()