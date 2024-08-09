import json
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class ToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("JK ToDo List")
        self.icon=PhotoImage(file='images/pretty.png')
        self.root.iconphoto(True,self.icon)

        # Set the style
        self.style = ttk.Style()
        self.style.theme_use("alt")

        # Configure the style
        self.style.configure('TNotebook.Tab', font=('Helvetica', '12'))
        self.style.configure('TButton', font=('Helvetica', '12', 'bold'))
        self.style.configure('TEntry', font=('Helvetica', '12'))

        # Create Notebook and Tabs
        self.notebook = ttk.Notebook(self.root)
        self.task_frame = ttk.Frame(self.notebook)
        self.important_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.task_frame, text="Task")
        self.notebook.add(self.important_frame, text="Important")

        # Configure grid for frames
        self.task_frame.grid_rowconfigure(0, weight=1)
        self.task_frame.grid_columnconfigure(0, weight=1)

        self.important_frame.grid_rowconfigure(0, weight=1)
        self.important_frame.grid_columnconfigure(0, weight=1)

        # Create listboxes and scrollbars for task_frame
        self.task_list_frame = ttk.Frame(self.task_frame)
        self.task_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.task_treeview = ttk.Treeview(self.task_list_frame, columns=['Task'], show='headings', height=10)
        self.task_treeview.pack(side="left", fill="both", expand=True)

        self.task_treeview.heading('Task', text='Task')

        self.task_scrollbar = ttk.Scrollbar(self.task_list_frame, orient="vertical", command=self.task_treeview.yview)
        self.task_scrollbar.pack(side="right", fill="y")

        self.task_treeview.config(yscrollcommand=self.task_scrollbar.set)

        # Create listboxes and scrollbars for important_frame
        self.important_list_frame = ttk.Frame(self.important_frame)
        self.important_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.important_treeview = ttk.Treeview(self.important_list_frame, columns=['Task'], show='headings', height=10)
        self.important_treeview.pack(side="left", fill="both", expand=True)

        self.important_treeview.heading('Task', text='Task')

        self.important_scrollbar = ttk.Scrollbar(self.important_list_frame, orient="vertical", command=self.important_treeview.yview)
        self.important_scrollbar.pack(side="right", fill="y")

        self.important_treeview.config(yscrollcommand=self.important_scrollbar.set)

        # Create a context menu for the task Treeview
        self.task_context_menu = Menu(self.task_treeview, tearoff=0)
        self.task_context_menu.add_command(label="Update", command=self.on_update_task)
        self.task_context_menu.add_command(label="Delete", command=self.on_delete_task)
        self.task_treeview.bind("<Button-3>", self.show_task_context_menu)
        
        # Create a context menu for the important Treeview
        self.important_context_menu = Menu(self.important_treeview, tearoff=0)
        self.important_context_menu.add_command(label="Update", command=self.on_update_task)
        self.important_context_menu.add_command(label="Delete", command=self.on_delete_task)
        self.important_treeview.bind("<Button-3>", self.show_important_context_menu)

        # Add widgets to task frame
        self.input_frame = ttk.Frame(self.task_frame)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.add_button = ttk.Button(self.input_frame, text="+", command=self.onclick)
        self.add_button.grid(row=0, column=0)

        self.entry = ttk.Entry(self.input_frame, width=30)
        self.entry.insert(0, "Add a Task")
        self.entry.state(['disabled'])
        self.entry.bind('<Return>', self.on_enter)
        self.entry.grid(row=0, column=1, padx=5)

        # Initialize counters for dynamic positioning of checkboxes
        self.task_count = 1
        self.important_count = 1

        # Set grid for notebook
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Manage row and column expansion
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Adjust frames to take half the screen width
        self.adjust_frame_width()

        # Load data from file
        self.load_data()
        

    def show_task_context_menu(self, event):
        # Clear selection in the important treeview
        self.important_treeview.selection_remove(self.important_treeview.selection())
        # Show the context menu at the current mouse position
        self.task_context_menu.tk_popup(event.x_root, event.y_root)
        
    def show_important_context_menu(self, event):
        # Clear selection in the task treeview
        self.task_treeview.selection_remove(self.task_treeview.selection())
        # Show the context menu at the current mouse position
        self.important_context_menu.tk_popup(event.x_root, event.y_root)

    def on_update_task(self):
        # Determine the currently selected tab
        current_tab_text = self.notebook.tab("current", "text")
        print(current_tab_text)
    
         # Identify the Treeview based on the active tab
        if current_tab_text == "Task":
            treeview = self.task_treeview
        elif current_tab_text == "Important":
            treeview = self.important_treeview
        else:
            messagebox.showinfo("Info", "No valid tab selected for update")
            return

        # Get the selected item from the identified Treeview
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showinfo("Info", "No item selected for update")
            return

        item_id = selected_item[0]
        item_text = treeview.item(item_id, 'values')[0]

        # Create a new Toplevel window for updating the task
        update_window = Toplevel(self.root)
        update_window.title("Update Task")

        # Add Entry widget with current task text
        self.update_entry = ttk.Entry(update_window, width=50)
        self.update_entry.insert(0, item_text)
        self.update_entry.pack(padx=10, pady=10)

        # Bind Enter key to save_update function
        self.update_entry.bind('<Return>', lambda event, item_id=item_id, treeview=treeview: self.save_update(item_id, treeview, update_window))

        # Add Save Button
        save_button = ttk.Button(update_window, text="Save", command=lambda: self.save_update(item_id, treeview, update_window))
        save_button.pack(pady=(0, 10))

    def save_update(self, item_id, treeview, update_window):
        new_text = self.update_entry.get()
        if not new_text:
            messagebox.showwarning("Warning", "Task cannot be empty")
            return

        print(f"Updating Treeview {treeview} Item ID: {item_id} with new text: {new_text}")

        # Update item in the correct Treeview
        treeview.item(item_id, values=[new_text])

        # Close the update window
        update_window.destroy()
    
        # Save data after update
        self.save_data()

    def on_delete_task(self):
        # Code to delete the selected task
        # Get selected item(s)
        current_tab_text = self.notebook.tab("current", "text")
        
        if current_tab_text == "Task":
            treeview = self.task_treeview
        elif current_tab_text == "Important":
            treeview = self.important_treeview
        else:
            messagebox.showinfo("Info", "No valid tab selected for deletion")
            return
        
        selected_items = treeview.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No items selected for deletion")
            return

        # Delete each selected item
        for item in selected_items:
            treeview.delete(item)
            
        # Save data after deletion
        self.save_data()

    def onclick(self):
        self.entry.config(state=NORMAL)
        self.entry.delete(0, END)
        self.entry.focus()

    def on_enter(self, event):
        task_text = self.entry.get()
        if task_text:  # Check if entry is not empty
            response = messagebox.askyesno(message="Do you want to add this task as important?")
            if response:
                self.important_treeview.insert('', 'end', values=[task_text])
                self.important_count += 1
                messagebox.showinfo('INFO','Added task successfully')
                
            else:
                self.task_treeview.insert('', 'end', values=[task_text])
                self.task_count += 1
                messagebox.showinfo('INFO','Added task successfully')
                
            # Reset the entry widget    
            self.entry.delete(0, END)
            self.entry.insert(0, "Add a Task")
            self.entry.config(state=['disabled'])

    def adjust_frame_width(self):
        # Adjust frames to take half the screen width
        screen_width = self.root.winfo_screenwidth()
        frame_width = int(screen_width / 2)
        self.root.geometry(f"{frame_width}x600")

    def load_data(self):
        # Load data from file
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                for task in data['tasks']:
                    self.task_treeview.insert('', 'end', values=[task])
                for task in data['important']:
                    self.important_treeview.insert('', 'end', values=[task])
        except FileNotFoundError:
            pass

    def save_data(self):
        # Save data to file
        tasks = [self.task_treeview.item(item, 'values')[0] for item in self.task_treeview.get_children()]
        important = [self.important_treeview.item(item, 'values')[0] for item in self.important_treeview.get_children()]
        data = {'tasks': tasks, 'important': important}
        with open('data.json', 'w') as file:
            json.dump(data, file)

    def on_closing(self):
        # Save data when window is closed
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = ToDoList(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
