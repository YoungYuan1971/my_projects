import time
import tkinter as tk


class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Electronic Clock @Designer: YoungYuan')
        self.resizable(0, 0)
        self.time_text = ""
        self.lbl = tk.Label(
            self,
            text=self.time_text,
            font=("ds-digital", 60),
            background="#000000",
            foreground="#4998CC"
        )

        self.lbl.pack()
        self.update_time()

    def update_time(self):
        self.time_text = time.strftime("%Y-%m-%d\n%H:%M:%S %a")
        self.lbl.config(text=self.time_text)
        self.after(1000, self.update_time)


if __name__ == '__main__':
    clock = Clock()
    clock.mainloop()
