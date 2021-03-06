"""
Developed by Lukasz Kolodzinski
"""

import tkinter as tk
import tkinter.messagebox as msg

class TransferList(tk.Tk):
    def __init__(self, players = None):
        super().__init__()

        if players is None:
            self.players = []
        else:
            self.players = players

        self.app_canvas = tk.Canvas(self)
        self.names_bar_frame = tk.Frame(self.app_canvas)
        self.text_frame = tk.Frame(self)

        self.scrolling = tk.Scrollbar(self.app_canvas, orient="vertical", command=self.app_canvas.yview)
        self.app_canvas.configure(yscrollcommand=self.scrolling.set)

        self.title("Wish Transfer")
        self.geometry("500x700")

        self.create_wish = tk.Text(self.text_frame, height=2, bg = "white", fg="black")

        self.app_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrolling.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame = self.app_canvas.create_window((0, 0), window=self.names_bar_frame, anchor="nw")
        self.create_wish.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_wish.focus_set()

        requested_player = tk.Label(self.app_canvas, text = "Add player's name here", bg = "lightgreen", fg = "black",
                                    pady=10, padx=190)
        requested_player.pack()
        
        for player in self.players:
            player.pack(side=tk.TOP, fill=tk.X)

        self.bind("<Return>", self.add_player)
        self.bind("<Configure>", self.scroll_canvas)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        # Button-4 and Button-5 handle mouse scroll for Linux
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.app_canvas.bind("<Configure>", self.canvas_width)

        self.color_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "lightblue", "fg": "black"}]

    def add_player(self, event=None):
        player_name = self.create_wish.get(1.0, tk.END).strip()

        if len(player_name) > 0:
            wished_player = tk.Label(self.names_bar_frame, text = player_name, pady=10)
            self.set_bar_color(len(self.players), wished_player)
            wished_player.bind("<Button-1>", self.remove_player)
            wished_player.pack(side=tk.TOP, fill=tk.X)
            self.players.append(wished_player)
        self.create_wish.delete(1.0, tk.END)

    def remove_player(self, event):
        player = event.widget
        if msg.askyesno("Confirm delte", "Do you want to delete {} ?".format(player.cget("text"))):
            self.players.remove(event.widget)
            event.widget.destroy()
            self.recolor_bars()

    def recolor_bars(self):
        for index, wished_player in enumerate(self.players):
            self.set_bar_color(index, wished_player)

    def set_bar_color(self, index, wished_player):
        _, choose_bar_color = divmod(index, 2)
        choosen_scheme = self.color_schemes[choose_bar_color]
        wished_player.configure(bg=choosen_scheme["bg"])
        wished_player.configure(fg=choosen_scheme["fg"])

    def scroll_canvas(self, event=None):
        self.app_canvas.configure(scrollregion=self.app_canvas.bbox("all"))

    def canvas_width(self, event):
        width_of_canvas = event.width
        self.app_canvas.itemconfig(self.canvas_frame, width=width_of_canvas)

    def mouse_scroll(self, event):
        if event.delta:
            self.app_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # Linux mouse scroll handling
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.app_canvas.yview_scroll(move, "units")

if __name__ == "__main__":
    transfer_list = TransferList()
    transfer_list.mainloop()