import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.text_widgets = []  # List to store multiple text widgets
        self.current_file = None
        self.zoom_factor = 1.0  # Initial zoom factor
        self.create_text_widget()
        self.create_menu()

    def create_text_widget(self):
        text_widget = tk.Text(self.root, wrap="word", undo=True)
        text_widget.pack(expand="yes", fill="both")
        self.text_widgets.append(text_widget)

    def create_menu(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create the file menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_command(label="Save All", command=self.save_all_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # Create the edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        edit_menu.add_command(label="Goto Line", command=self.goto_line)  # Add Goto Line option

        # Create the view menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Change Font Size", command=self.change_font_size)
        view_menu.add_command(label="Toggle Wrap Text", command=self.toggle_wrap_text)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)

    def new_file(self):
        self.create_text_widget()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                text_widget = self.text_widgets[-1]  # Get the current text widget
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, content)
            self.root.title(f"Text Editor - {file_path}")
            self.current_file = file_path

    def save_file(self):
        if self.current_file is None:
            self.save_as_file()
        else:
            text_widget = self.text_widgets[-1]  # Get the current text widget
            content = text_widget.get(1.0, tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            text_widget = self.text_widgets[-1]  # Get the current text widget
            content = text_widget.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path
            self.root.title(f"Text Editor - {file_path}")

    def save_all_files(self):
        for i, text_widget in enumerate(self.text_widgets, start=1):
            file_path = self.current_file if i == 1 else self.current_file.replace('.txt', f'_{i}.txt')
            content = text_widget.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path

    def undo(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        text_widget.event_generate("<<Undo>>")

    def redo(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        text_widget.event_generate("<<Redo>>")

    def cut(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        text_widget.event_generate("<<Cut>>")

    def copy(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        text_widget.event_generate("<<Copy>>")

    def paste(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        text_widget.event_generate("<<Paste>>")

    def select_all(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        text_widget.tag_add("sel", "1.0", tk.END)

    def change_font_size(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        new_font_size = simpledialog.askinteger("Change Font Size", "Enter Font Size:", parent=self.root, minvalue=1)
        if new_font_size:
            current_font = text_widget.cget("font")
            font_family, _, font_size = current_font.rpartition(" ")
            new_font = (font_family, new_font_size)
            text_widget.configure(font=new_font)

    def toggle_wrap_text(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        wrap_state = text_widget.cget("wrap")
        new_wrap_state = "none" if wrap_state == "word" else "word"
        text_widget.configure(wrap=new_wrap_state)

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_zoom()

    def update_zoom(self):
        text_widget = self.text_widgets[-1]  # Get the current text widget
        current_font = text_widget.cget("font")
        font_family, _, font_size = current_font.rpartition(" ")

        try:
            # Try converting the font size to a float
            current_font_size = float(font_size)
        except ValueError:
            # If conversion fails, use the current font size
            current_font_size = 12  # Default font size

        new_font_size = int(current_font_size * self.zoom_factor)
        new_font = (font_family, new_font_size)
        text_widget.configure(font=new_font)

    def find_text(self):
        search_text = simpledialog.askstring("Find", "Enter text to find:", parent=self.root)
        if search_text:
            text_widget = self.text_widgets[-1]  # Get the current text widget
            start_index = text_widget.search(search_text, "1.0", tk.END)
            if start_index:
                end_index = f"{start_index}+{len(search_text)}c"
                text_widget.tag_remove("sel", "1.0", tk.END)  # Clear previous selection
                text_widget.tag_add("sel", start_index, end_index)
                text_widget.mark_set("insert", start_index)
                text_widget.see("insert")

    def replace_text(self):
        search_text = simpledialog.askstring("Replace", "Enter text to replace:", parent=self.root)
        if search_text:
            replace_text = simpledialog.askstring("Replace", f"Enter replacement text for '{search_text}':", parent=self.root)
            if replace_text:
                text_widget = self.text_widgets[-1]  # Get the current text widget
                start_index = text_widget.search(search_text, "1.0", tk.END)
                while start_index:
                    end_index = f"{start_index}+{len(search_text)}c"
                    text_widget.delete(start_index, end_index)
                    text_widget.insert(start_index, replace_text)
                    start_index = text_widget.search(search_text, end_index, tk.END)

    def goto_line(self):
        line_number = simpledialog.askinteger("Goto Line", "Enter line number:", parent=self.root, minvalue=1)
        if line_number:
            text_widget = self.text_widgets[-1]  # Get the current text widget
            line_count = text_widget.index("end-1c").split(".")[0]
            if line_number <= int(line_count):
                target_line = f"{line_number}.0"
                text_widget.mark_set("insert", target_line)
                text_widget.see("insert")
            else:
                tk.messagebox.showwarning("Goto Line", f"Line number exceeds total lines ({line_count}) in the document.")

if __name__ == "__main__":
    root = tk.Tk()
    text_editor = TextEditor(root)
    root.mainloop()

