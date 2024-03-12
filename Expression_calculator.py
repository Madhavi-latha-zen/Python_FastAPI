# Using Eval

# def add(x, y):
#     return x + y

# def subtract(x, y):
#     return x - y

# def multiply(x, y):
#     return x * y

# def divide(x, y):
#     if y != 0:
#         return x / y
#     else:
#         return "Error: Cannot divide by zero"

# def calculate_expression(expression):
#     try:
#         result = eval(expression)
#         return result
#     except Exception as e:
#         return f"Error: {e}"

# expression = input("Enter the expression: ")
# result = calculate_expression(expression)

# print("Result:", result)#((((3*8)+2)-6)*12)/3



#without using Ebval method

from tkinter import Tk, Entry, Button, StringVar

def clear():
    entry_var.set("")

def btn_clk(char):
    entry_var.set(entry_var.get() + char)

def evaluate(expression):
    try:
        tokens = []
        current_num = ''
        for char in expression:
            if char.isdigit() or char == '.':
                current_num += char
            else:
                if current_num:
                    tokens.append(float(current_num))
                    current_num = ''
                tokens.append(char)

        if current_num:
            tokens.append(float(current_num))

        numbers = []
        operators = []

        for token in tokens:
            if isinstance(token, (int, float)):
                numbers.append(token)
            elif token in "+-*/":
                while operators and precedence(operators[-1]) >= precedence(token):
                    apply_operator(numbers, operators)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(numbers, operators)
                operators.pop()  # Remove '('

        while operators:
            apply_operator(numbers, operators)

        return numbers[0]

    except Exception as e:
        return "Error"

def apply_operator(numbers, operators):
    num2 = numbers.pop()
    num1 = numbers.pop()
    operator = operators.pop()

    if operator == '+':
        numbers.append(num1 + num2)
    elif operator == '-':
        numbers.append(num1 - num2)
    elif operator == '*':
        numbers.append(num1 * num2)
    elif operator == '/':
        if num2 == 0:
            raise ValueError("Division by zero!")
        numbers.append(num1 / num2)

def equal():
    expression = entry_var.get()
    result = evaluate(expression)
    entry_var.set(str(result))

def precedence(operator):
    if operator in '+-':
        return 1
    elif operator in '*/':
        return 2
    return 0

root = Tk()
root.title('Simple Calculator')

# Entry field to display and input the expression
entry_var = StringVar()
entry = Entry(root, textvariable=entry_var, font=('Arial', 14), justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=50, pady=20, ipadx=10, ipady=10)

# Buttons for digits, operators, and special functions
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ('(', 5, 0), (')', 5, 1)  # Added parentheses buttons
]

# Configure and place buttons in the grid
for (text, row, col) in buttons:
    button = Button(root, text=text, padx=25, pady=25, font=('Arial', 14), bd=4, relief='raised')
    button.grid(row=row, column=col, padx=5, pady=5)

    # Assign command based on button type
    if text.isdigit() or text in '()+-*/':
        button.config(command=lambda t=text: btn_clk(t))
        button.configure(bg='lightgray', fg='black', borderwidth=0, highlightthickness=0, bd=1, relief='solid')
    elif text == 'C':
        button.config(command=clear)
        button.configure(bg='orange', fg='black', borderwidth=0, highlightthickness=0, bd=1, relief='solid')
    elif text == '=':
        button.config(command=equal)
        button.configure(bg='green', fg='white', borderwidth=0, highlightthickness=0, bd=1, relief='solid')

# Start the GUI event loop
root.mainloop()
