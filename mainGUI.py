import tkinter as tk
from tkinter import messagebox
from classGame import GameLogic
from graphClass import Graph

# GUI Class to visualize the game
class GameGUI:
    def __init__(self, master, delay, graph):
        self.master = master
        self.master.title("The Sub and The Boat Game")
        self.delay = delay

        # initialize game logic
        try:
            self.game_logic = GameLogic(graph)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # set up canvas dimensions
        self.canvas_width = 1000
        self.canvas_height = 600
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(side=tk.TOP, pady=5)

        self.node_tags = {}

        # scale graph to fit the canvas
        self.scale_graph_to_canvas()
        # draw the graph, then update GUI
        self.draw_graph()
        self.update_ui()

        # start the game loop with sub move
        self.master.after(self.delay, self.sub_move)

    def scale_graph_to_canvas(self):
        # determine the bounding box of the original graph
        xs = [coord[0] for coord in self.game_logic.graph.nodes.values()]
        ys = [coord[1] for coord in self.game_logic.graph.nodes.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # define a margin so nodes aren't drawn right on the edge of the canvas
        margin = 50

        # Compute the width and height of the graph
        width = max_x - min_x
        height = max_y - min_y

        # Compute the available drawing area inside the canvas
        available_width = self.canvas_width - 2 * margin
        available_height = self.canvas_height - 2 * margin

        # Compute scale factor to fit the graph within the canvas while maintaining aspect ratio
        scale_factor = min(available_width / width if width > 0 else float('inf'),
                           available_height / height if height > 0 else float('inf'))

        # Compute the center of the original graph
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        # Compute the center of the canvas
        canvas_center_x = self.canvas_width / 2
        canvas_center_y = self.canvas_height / 2

        # Compute shift amounts to center the graph on the canvas
        shift_x = canvas_center_x - scale_factor * center_x
        shift_y = canvas_center_y - scale_factor * center_y

        # Apply scaling and shifting to each node's coordinates
        for node_id, (x, y) in self.game_logic.graph.nodes.items():
            new_x = x * scale_factor + shift_x
            new_y = y * scale_factor + shift_y
            self.game_logic.graph.nodes[node_id] = (new_x, new_y)

    def draw_graph(self):
        # draw lines
        for node, coords in self.game_logic.graph.nodes.items():
            x, y = coords
            for nbr in self.game_logic.graph.adjacency[node]:
                nx, ny = self.game_logic.graph.nodes[nbr]
                if node < nbr:
                    self.canvas.create_line(x, y, nx, ny, fill="black")

        # draw all nodes as circles
        for node, (x, y) in self.game_logic.graph.nodes.items():
            r = 15
            oval = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="lightblue", outline="blue", width=2)
            self.canvas.create_text(x, y, text=str(node), fill="black")
            self.node_tags[node] = oval

    # method for updating colors of the nodes that the boat and sub are currently on
    def update_ui(self):
        for node, oval in self.node_tags.items():
            color = "lightblue"
            width = 2

            if node == self.game_logic.sub_pos and node == self.game_logic.boat_pos:
                color = "purple"
                width = 3
            elif node == self.game_logic.sub_pos:
                color = "darkblue"
                width = 3
            elif node == self.game_logic.boat_pos:
                color = "orange"
                width = 3

            self.canvas.itemconfig(oval, fill=color, outline="blue", width=width)

        self.status_label.config(text=f"The Sub at {self.game_logic.sub_pos}, The Boat at {self.game_logic.boat_pos}")

    # method for handling sub move
    def sub_move(self):
        try:
            message = self.game_logic.sub_move()
            self.update_ui()
            if message:
                messagebox.showinfo("Game Over", message)
            else:
                self.master.after(self.delay, self.boat_move)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # method for handling boat move
    def boat_move(self):
        try:
            message = self.game_logic.boat_move()
            self.update_ui()
            if message:
                messagebox.showinfo("Game Over", message)
            else:
                self.master.after(self.delay, self.sub_move)
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    # tkinter object
    root = tk.Tk()
    # file for the graph
    file = "/Users/davidklasa/Documents/KTH/KTH Kandidatexamensjobb/Kod/graph1.csv"
    # delay 3 sek so can se moves
    delay = 3000
    # initializing the game with GUI
    game_gui = GameGUI(root, delay, Graph(file))
    root.mainloop()