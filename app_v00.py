import tkinter as tk

class Node:
    def __init__(self, canvas, id, x, y, width, height, label, shape="rectangle", is_event=False):
        self.canvas = canvas
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.shape = shape
        self.is_event = is_event
        if not self.is_event:
            self.draw()
        self.timer_text_id = None
        self.timer_value = None

    def draw(self):
        if self.shape == "rectangle":
            self.graphic = self.canvas.create_rectangle(
                self.x, self.y, self.x + self.width, self.y + self.height,
                fill="white", outline="black", width=2)
        elif self.shape == "diamond":
            w, h = self.width, self.height
            self.graphic = self.canvas.create_polygon(
                self.x + w / 2, self.y,
                self.x + w, self.y + h / 2,
                self.x + w / 2, self.y + h,
                self.x, self.y + h / 2,
                fill="white", outline="black", width=2
            )
        elif self.shape == "oval":
            self.graphic = self.canvas.create_oval(
                self.x, self.y, self.x + self.width, self.y + self.height,
                fill="white", outline="black", width=2
            )
        elif self.shape == "circle":
            r = self.width / 2
            self.graphic = self.canvas.create_oval(
                self.x, self.y, self.x + 2 * r, self.y + 2 * r,
                fill="black", outline="black"
            )
        self.label_text = self.canvas.create_text(
            self.x + self.width / 2,
            self.y + self.height / 2,
            text=self.label, font=("Arial", 9), width=self.width - 10
        )

    def activate(self):
        if self.id == "Task_2":
            self.canvas.itemconfig(self.graphic, fill="red")  # Kırmızı yap
        elif self.shape == "circle":
            self.canvas.itemconfig(self.graphic, fill="black")
        elif not self.is_event:
            self.canvas.itemconfig(self.graphic, fill="lightgreen")

    def deactivate(self):
        if self.shape == "circle":
            self.canvas.itemconfig(self.graphic, fill="white")
        elif not self.is_event:
            self.canvas.itemconfig(self.graphic, fill="white")

    def set_timer(self, value):
        # Timer değeri güncelle, göster
        self.timer_value = value
        x = self.x + self.width + 10
        y = self.y + self.height / 2
        text = str(value) if value is not None else ""
        if self.timer_text_id is None:
            self.timer_text_id = self.canvas.create_text(x, y, text=text, font=("Arial", 12, "bold"), fill="red")
        else:
            self.canvas.itemconfig(self.timer_text_id, text=text)

    def clear_timer(self):
        if self.timer_text_id:
            self.canvas.delete(self.timer_text_id)
            self.timer_text_id = None
            self.timer_value = None


class StateMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("State Machine Visualization")

        self.active_state_label = tk.Label(self.root, text="Aktif State: ", font=("Arial", 14))
        self.active_state_label.pack(pady=5)
        
        # Input switchler için IntVar
        self.a_input = tk.IntVar(value=0)
        self.b_input = tk.IntVar(value=0)

        # Frame for inputs and control
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        


        # Switch butonları (toggle button gibi)
        self.a_button = tk.Button(control_frame, text="A Input (A_DONE): OFF", width=20, command=self.toggle_a)
        self.a_button.pack(side=tk.LEFT, padx=5)

        self.b_button = tk.Button(control_frame, text="B Input (B_PASSIVE): OFF", width=20, command=self.toggle_b)
        self.b_button.pack(side=tk.LEFT, padx=5)

        # Simülasyon durdur/başlat butonu
        self.is_running = True
        self.toggle_button = tk.Button(control_frame, text="Pause", width=15, command=self.toggle_run)
        self.toggle_button.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=1200, height=800, bg="white")
        self.canvas.pack()
        self.nodes = {}
        self.transitions = []
        self.visited_nodes = []

        self.current_state = "Task_1"
        self.delay = 5  # 500 ms delay, ayarını buradan değiştirebilirsin

        tk.Label(control_frame, text="Delay (ms):").pack(side=tk.LEFT, padx=5)
        self.delay_var = tk.StringVar(value=str(self.delay))
        self.delay_entry = tk.Entry(control_frame, width=6, textvariable=self.delay_var)
        self.delay_entry.pack(side=tk.LEFT)
        self.delay_entry.bind("<Return>", self.update_delay)

        # Timer için geri sayım değerleri (örnek süreler)
        self.timers = {
            "Exit1": 5,   # saniye cinsinden
            "Exit2": 5,
            "Task_2": 5
        }
        self.current_timers = {
            "Exit1": None,
            "Exit2": None,
            "Task_2": None
        }

        self.create_nodes()
        self.create_transitions()
        self.draw_all_transitions()

        self.run_loop_id = None
        self.run_state_machine()

    def update_delay(self, event=None):
        try:
            val = int(self.delay_var.get())
            if val < 50:
                val = 50  # Çok düşük değerleri engelle
            self.delay = val
        except ValueError:
            # Hatalı girişte eski değeri koru ve tekrar yazdır
            self.delay_var.set(str(self.delay))

    # Toggle fonksiyonları
    def toggle_a(self):
        new_val = 1 - self.a_input.get()
        self.a_input.set(new_val)
        self.a_button.config(text=f"A Input (A_DONE): {'ON' if new_val else 'OFF'}")

    def toggle_b(self):
        new_val = 1 - self.b_input.get()
        self.b_input.set(new_val)
        self.b_button.config(text=f"B Input (B_PASSIVE): {'ON' if new_val else 'OFF'}")

    def toggle_run(self):
        if self.is_running:
            # Durdur
            self.is_running = False
            self.toggle_button.config(text="Başlat")
            if self.run_loop_id is not None:
                self.root.after_cancel(self.run_loop_id)
                self.run_loop_id = None
        else:
            # Başlat
            self.is_running = True
            self.toggle_button.config(text="Duraklat")
            self.run_state_machine()

    def create_node(self, id, x, y, label, shape="rectangle", width=120, height=50, is_event=False):
        self.nodes[id] = Node(self.canvas, id, x, y, width, height, label, shape, is_event)

    def create_transition(self, from_id, to_id, label="", from_side="bottom", to_side="top"):
        self.transitions.append((from_id, to_id, label, from_side, to_side))

    def get_connector_point(self, node, side):
        x, y, w, h = node.x, node.y, node.width, node.height
        if side == "top":
            return x + w / 2, y
        elif side == "bottom":
            return x + w / 2, y + h
        elif side == "left":
            return x, y + h / 2
        elif side == "right":
            return x + w, y + h / 2
        else:
            return x + w / 2, y + h

    def draw_arrow(self, fx, fy, tx, ty):
        self.canvas.create_line(fx, fy, tx, ty, arrow=tk.LAST, width=2)

    def draw_all_transitions(self):
        self.canvas.delete("arrow_label")
        self.canvas.delete("arrow_line")
        label_offsets = {}

        for (from_id, to_id, label, from_side, to_side) in self.transitions:
            from_node = self.nodes[from_id]
            to_node = self.nodes[to_id]
            fx, fy = self.get_connector_point(from_node, from_side)
            tx, ty = self.get_connector_point(to_node, to_side)
            self.draw_arrow(fx, fy, tx, ty)

            label_x = (fx + tx) / 2
            label_y = (fy + ty) / 2 - 10
            key = (round(label_x), round(label_y))
            offset = label_offsets.get(key, 0)
            label_offsets[key] = offset + 12
            label_y += offset

            if label:
                self.canvas.create_text(label_x, label_y, text=label, font=("Arial", 8, "italic"), tags="arrow_label")

    def deactivate_all(self):
        for node in self.nodes.values():
            if not node.is_event:
                node.deactivate()

    def step(self, node_id):
        node = self.nodes[node_id]
        if node.is_event:
            return
        if node_id == "Task_1":
            self.visited_nodes = []
            self.deactivate_all()
            # Timer reset
            for k in self.current_timers.keys():
                self.current_timers[k] = self.timers[k]
                self.nodes[k].set_timer(self.current_timers[k])

        if node_id not in self.visited_nodes:
            self.visited_nodes.append(node_id)
            node.activate()
        self.current_state = node_id
        self.active_state_label.config(text=f"Active State: {node_id}")

    def decrement_timers(self):
        updated = False
        for key in self.current_timers:
            val = self.current_timers[key]
            if val is not None and val > 0:
                self.current_timers[key] -= 1
                self.nodes[key].set_timer(self.current_timers[key])
                updated = True
        return updated

    def run_state_machine(self):
        if not self.is_running:
            return

        # Sayaçları azalt
        self.decrement_timers()

        state = self.current_state

        if state == "Task_1":
            self.step("Task_1")
            self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Entry_A"))

        elif state == "Entry_A":
            self.step("Entry_A")
            self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("FSM_A"))

        elif state == "FSM_A":
            self.step("FSM_A")
            if self.a_input.get() == 1:
                self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Exit_A"))
            else:
                self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("ExitWithFlags"))

        elif state == "ExitWithFlags":
            self.step("ExitWithFlags")
            self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Exit1"))

        elif state == "Exit1":
            self.step("Exit1")
            # Timerı kontrol et, 0 ise devam et
            if self.current_timers["Exit1"] is None:
                self.current_timers["Exit1"] = self.timers["Exit1"]
                self.nodes["Exit1"].set_timer(self.current_timers["Exit1"])
            if self.current_timers["Exit1"] > 0:
                self.current_timers["Exit1"] -= 1
                self.nodes["Exit1"].set_timer(self.current_timers["Exit1"])
                self.run_loop_id = self.root.after(100, self.run_state_machine)
            else:
                self.current_timers["Exit1"] = None
                self.nodes["Exit1"].clear_timer()
                self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Task_1"))

        elif state == "Exit_A":
            self.step("Exit_A")
            self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Entry_B"))

        elif state == "Entry_B":
            self.step("Entry_B")
            self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("FSM_B"))

        elif state == "FSM_B":
            self.step("FSM_B")
            if self.b_input.get() == 1:
                self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Exit_B"))
            else:
                self.run_loop_id = self.root.after(self.delay, lambda: self.step_and_continue("Exit2"))

        elif state == "Exit2":
            self.step("Exit2")
            if self.current_timers["Exit2"] is None:
                self.current_timers["Exit2"] = self.timers["Exit2"]
                self.nodes["Exit2"].set_timer(self.current_timers["Exit2"])
            if self.current_timers["Exit2"] > 0:
                self.current_timers["Exit2"] -= 1
                self.nodes["Exit2"].set_timer(self.current_timers["Exit2"])
                self.run_loop_id = self.root.after(100, self.run_state_machine)
            else:
                self.current_timers["Exit2"] = None
                self.nodes["Exit2"].clear_timer()
                self.run_loop_id = self.root.after(100, lambda: self.step_and_continue("Task_1"))

        elif state == "Exit_B":
            self.step("Exit_B")

            if self.current_timers["Task_2"] is None:
                self.current_timers["Task_2"] = self.timers["Task_2"]
                self.nodes["Task_2"].set_timer(self.current_timers["Task_2"])
            if self.current_timers["Task_2"] > 0:
                self.current_timers["Task_2"] -= 1
                self.nodes["Task_2"].set_timer(self.current_timers["Task_2"])
                self.run_loop_id = self.root.after(100, self.run_state_machine)
            else:
                self.current_timers["Task_2"] = None
                self.nodes["Task_2"].clear_timer()
                self.run_loop_id = self.root.after(100, lambda: self.step_and_continue("Task_2"))

        elif state == "Task_2":
            self.step("Task_2")
            self.run_loop_id = self.root.after(100, lambda: self.step_and_continue("Task_1"))

    def step_and_continue(self, next_state):
        self.step(next_state)
        if self.is_running:
            self.run_loop_id = self.root.after(self.delay, self.run_state_machine)

    def create_nodes(self):
        self.create_node("Task_1", 100, 10, "Task_1_()", "oval", 80, 60)
        self.create_node("Entry_A", 150, 120, "prvEntryState_AEventCheck()", width=170)
        self.create_node("Exit_A", 150, 400, "prvExitState_AEventCheck()", width=170)
        self.create_node("Entry_B", 150, 490, "prvEntryState_BEventCheck()", width=170)
        self.create_node("Exit_B", 150, 730, "prvExitState_BEventCheck()", width=170)
        self.create_node("FSM_A", 100, 230, "prvStates_AEventCheck()", "diamond", 160, 100)
        self.create_node("FSM_B", 100, 580, "prvStates_BEventCheck()", "diamond", 160, 100)
        self.create_node("A_FAULT", 720, 160, "_EVENT_A_FAULT", is_event=True)
        self.create_node("ExitWithFlags", 600, 255, "prvExitFromTask()", width=140)
        self.create_node("Exit1", 1040, 265, "", "circle", 30, 30)
        self.create_node("A_DONE", 500, 300, "_EVENT_A_DONE", is_event=True)
        self.create_node("B_ACTIVE", 720, 430, "_EVENT_B_ACTIVE", is_event=True)
        self.create_node("Exit2", 1040, 615, "", "circle", 30, 30)
        self.create_node("B_PASSIVE", 500, 550, "_EVENT_B_PASSIVE", is_event=True)
        self.create_node("Task_2", 800, 730, "Task_2_()", width=120)

    def create_transitions(self):
        self.create_transition("Task_1", "Entry_A")
        self.create_transition("Entry_A", "FSM_A")
        self.create_transition("FSM_A", "Exit_A", "_EVENT_A_DONE")
        self.create_transition("Exit_A", "Entry_B")
        self.create_transition("FSM_A", "ExitWithFlags", "_EVENT_A_FAULT", "right", "left")
        self.create_transition("ExitWithFlags", "Exit1", "","right", "left")
        self.create_transition("Entry_B", "FSM_B")
        self.create_transition("FSM_B", "Exit2", "_EVENT_B_ACTIVE", "right", "left")
        self.create_transition("FSM_B", "Exit_B", "_EVENT_B_PASSIVE")
        self.create_transition("Exit_B", "Task_2", "","right", "left")
        self.create_transition("Exit2", "Exit1", "","top", "bottom")
        self.create_transition("Exit1", "Task_1", "", "top", "right")

if __name__ == "__main__":
    root = tk.Tk()
    app = StateMachineGUI(root)
    root.mainloop()
