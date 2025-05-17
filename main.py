import tkinter as tk
from calender_gui import CalendarGUI

def main():
    root = tk.Tk()
    app = CalendarGUI(root)
    root.update_idletasks()

    w = root.winfo_width()
    h = root.winfo_height()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)

    root.geometry(f"+{x}+{y}")
    root.mainloop()


main()
