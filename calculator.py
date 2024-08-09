from tkinter import *
from tkinter import ttk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x400")  # Increased width to accommodate wider history frame
        self.root.title("Calculator")
        self.root.config(background="#F09D61")

        # Create a style for the calculator
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 14, 'bold'), padding=10, background='#FFA500', relief='flat')
        self.style.map('TButton', background=[('active', '#FFB600')])

        # Initialize attributes
        self.current_input = ""
        self.last_operation = None
        self.total = None
        self.first_operand = None
        self.displayed_operation = ""

        # Entry widget for results
        self.entry = Entry(root, font=('Arial', 18, 'bold'), bd=2, relief=RAISED, justify='right', background="#333333", fg="#FFFFFF")
        self.entry.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.entry.focus()

        # Entry widget for operation display
        self.operation_display = Label(root, font=('Arial', 12), bg="#F09D61", fg="#FFFFFF", anchor='e')
        self.operation_display.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

        # Create frames for buttons and history
        self.button_frame = Frame(root, bg="#1E1E1E")
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        # Adjusted history frame with pack geometry manager
        self.history_frame = Frame(root, bg="#1E1E1E", borderwidth=2, relief=SUNKEN)
        self.history_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='ns')

        # Create a canvas inside history_frame to ensure proper width
        self.history_canvas = Canvas(self.history_frame, bg="#1E1E1E", width=400)
        self.history_canvas.pack(fill=BOTH, expand=True)

        self.history_label = Label(self.history_canvas, text="History", bg="#2E2E2E", fg="#FFFFFF", font=('Arial', 16, 'bold'))
        self.history_label.pack(pady=10, fill=X)

        self.history_listbox = Listbox(self.history_canvas, bg="#2E2E2E", fg="#FFFFFF", font=('Arial', 12), selectmode=SINGLE, borderwidth=1, relief=RAISED, width=40)
        self.history_listbox.pack(fill=BOTH, expand=True)

        # Define button layout including new buttons
        buttons = [
            (' ', ' C', '⌫', '+'),
            ('7', '8', '9', '÷'),
            ('4', '5', '6', 'x'),
            ('1', '2', '3', '-'),
            ('±', '0', '.','=')
        ]

        # Create buttons and add them to the grid
        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                button = ttk.Button(self.button_frame, text=text, command=lambda t=text: self.click_button(t))
                button.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')

        # Configure row and column weights for button frame
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Configure row and column weights for root window
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)  # Main calculator column
        root.grid_columnconfigure(1, weight=0)  # Fixed width for history frame

        # Track window state
        self.root.bind("<Configure>", self.update_history_visibility)

    def click_button(self, text):
        if text.isdigit():
            self.add_digit(text)
        elif text in {'+', '-', 'x', '÷'}:
            self.set_operation(text)
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '=':
            self.calculate_result()
        elif text == '±':
            self.toggle_sign()
        elif text == '.':
            self.add_decimal_point()

    def add_digit(self, digit):
        self.current_input += digit
        self.update_display()

    def set_operation(self, operator):
        if self.current_input:
            if self.first_operand is None:
                self.first_operand = int(self.current_input) if '.' not in self.current_input else float(self.current_input)
            else:
                self.calculate_result()
            self.last_operation = operator
            self.displayed_operation = f"{self.first_operand} {operator}"
            self.current_input = ""
            self.update_display()

    def clear(self):
        self.current_input = ""
        self.total = None
        self.last_operation = None
        self.first_operand = None
        self.displayed_operation = ""
        self.update_display()

    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
        self.update_display()

    def calculate_result(self):
        if self.current_input and self.last_operation and self.first_operand is not None:
            try:
                current_value = int(self.current_input) if '.' not in self.current_input else float(self.current_input)
                if self.last_operation == '+':
                    self.total = self.first_operand + current_value
                elif self.last_operation == '-':
                    self.total = self.first_operand - current_value
                elif self.last_operation == 'x':
                    self.total = self.first_operand * current_value
                elif self.last_operation == '÷':
                    self.total = self.first_operand / current_value
                
                # Update the history
                self.update_history(f"{self.displayed_operation} {self.current_input} = {self.total}")
                
                # Update main display with result
                self.current_input = str(int(self.total)) if self.total.is_integer() else str(self.total)
                self.first_operand = None
                self.last_operation = None
                self.displayed_operation = ""
            except ZeroDivisionError:
                self.current_input = "Error"
            except Exception as e:
                self.current_input = "Error"
        self.update_display()

    def toggle_sign(self):
        if self.current_input:
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
        self.update_display()

    def add_decimal_point(self):
        if '.' not in self.current_input:
            self.current_input += '.'
        self.update_display()

    def update_display(self):
        # Update operation display
        self.operation_display.config(text=self.displayed_operation + (f" {self.current_input}" if self.current_input else ""))
        # Update main display
        display_text = self.current_input if self.current_input else "0"
        self.entry.delete(0, END)
        self.entry.insert(0, display_text)

    def update_history(self, entry_text):
        self.history_listbox.insert(END, entry_text)

    def update_history_visibility(self, event=None):
        window_state = self.root.state()
        if window_state == 'normal':
            self.history_frame.grid_forget()
        elif window_state == 'zoomed':
            self.history_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='ns')
            self.history_frame.update_idletasks()  # Force update to ensure proper sizing
        else:
            self.history_frame.grid_forget()

if __name__ == "__main__":
    root = Tk()
    app = CalculatorApp(root)
    root.mainloop()
