import tkinter as tk
from ui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(master=root)
    app.run()