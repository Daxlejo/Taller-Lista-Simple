import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.next_task = None
        self.completed = False


class TaskList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_task(self, name, description):
        new_task = Task(name, description)
        if self.head is None:
            self.head = new_task
            self.tail = new_task
        else:
            self.tail.next_task = new_task
            self.tail = new_task

    def remove_task(self, name):
        current = self.head
        previous = None

        while current is not None:
            if current.name == name:
                if current == self.head:
                    self.head = current.next_task
                else:
                    previous.next_task = current.next_task
                
                if current == self.tail:
                    self.tail = previous
                return True  
            
            previous = current
            current = current.next_task
        
        return False  

    def complete_task(self, name):
        current = self.head
        while current is not None:
            if current.name == name:
                current.completed = True
                return True
            current = current.next_task
        
        return False
    

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current is not None:
            tasks.append({
                'name': current.name,
                'description': current.description,
                'completed': current.completed
            })
            current = current.next_task
        return tasks
    
    def modify_task(self, name, new_description):
        current = self.head
        while current is not None:
            if current.name == name:
                current.description = new_description
                return True
            current = current.next_task
        return False

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Tareas")
        self.geometry("1100x650")
        self.minsize(960, 580)
        self.configure(bg="#020617")

        self.task_list = TaskList()

        self._setup_style()
        self._build_layout()
        self._refresh_lists()

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg = "#020617"
        card = "#020617"
        border = "#1f2937"
        accent = "#6366f1"
        accent_soft = "#312e81"
        text = "#f9fafb"
        text_soft = "#9ca3af"

        self["bg"] = bg

        style.configure("TFrame", background=bg)
        style.configure(
            "Card.TFrame",
            background=card,
            bordercolor=border,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Title.TLabel",
            background=bg,
            foreground=text,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "SectionTitle.TLabel",
            background=bg,
            foreground=text,
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background=bg,
            foreground=text_soft,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Accent.TButton",
            background=accent,
            foreground=text,
            borderwidth=0,
            focusthickness=0,
            font=("Segoe UI", 10, "bold"),
            padding=6,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#4f46e5")],
        )
        style.configure(
            "Ghost.TButton",
            background=card,
            foreground=text_soft,
            borderwidth=0,
            font=("Segoe UI", 10),
            padding=4,
        )
        style.map("Ghost.TButton", background=[("active", "#111827")])

    def _build_layout(self):
        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True, padx=18, pady=18)

        main_card = ttk.Frame(container, style="Card.TFrame")
        main_card.pack(fill="both", expand=True)
        main_card.grid_columnconfigure(0, weight=3)
        main_card.grid_columnconfigure(1, weight=4)
        main_card.grid_columnconfigure(2, weight=3)
        main_card.grid_rowconfigure(1, weight=1)

        header = ttk.Frame(main_card, style="TFrame")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=24, pady=(16, 8))

        title = ttk.Label(
            header, text="Gestor de Tareas", style="Title.TLabel"
        )
        title.pack(side="left")

        subtitle = ttk.Label(
            header,
            text="Pendientes a la izquierda · Completadas a la derecha",
            style="Muted.TLabel",
        )
        subtitle.pack(side="left", padx=(10, 0))

        left_panel = ttk.Frame(main_card, style="TFrame")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(18, 9), pady=(8, 18))
        left_panel.grid_rowconfigure(1, weight=1)

        left_header = ttk.Frame(left_panel, style="TFrame")
        left_header.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        ttk.Label(
            left_header, text="Pendientes", style="SectionTitle.TLabel"
        ).pack(side="left")

        self.lbl_pending_count = ttk.Label(
            left_header, text="0 tareas", style="Muted.TLabel"
        )
        self.lbl_pending_count.pack(side="right")

        self.pending_list = self._create_listbox(left_panel)
        self.pending_list.grid(row=1, column=0, sticky="nsew")


        center_panel = ttk.Frame(main_card, style="TFrame")
        center_panel.grid(row=1, column=1, sticky="nsew", padx=9, pady=(8, 18))
        center_panel.grid_columnconfigure(0, weight=1)
        center_panel.grid_rowconfigure(2, weight=1)

        center_header = ttk.Frame(center_panel, style="TFrame")
        center_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(
            center_header, text="Detalle / Nueva tarea", style="SectionTitle.TLabel"
        ).pack(side="left")

        form_card = ttk.Frame(center_panel, style="Card.TFrame")
        form_card.grid(row=1, column=0, sticky="ew")

        form = ttk.Frame(form_card, style="TFrame")
        form.pack(fill="both", expand=True, padx=16, pady=14)
        form.grid_columnconfigure(0, weight=1)

        ttk.Label(form, text="Título").grid(row=0, column=0, sticky="w")
        self.entry_title = ttk.Entry(form)
        self.entry_title.grid(row=1, column=0, sticky="ew", pady=(2, 8))

        ttk.Label(form, text="Descripción").grid(row=2, column=0, sticky="w")
        self.text_description = tk.Text(
            form,
            height=6,
            bg="#020617",
            fg="#f9fafb",
            insertbackground="#f9fafb",
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2937",
            highlightcolor="#312e81",
            wrap="word",
        )
        self.text_description.grid(row=3, column=0, sticky="nsew", pady=(2, 8))
        form.grid_rowconfigure(3, weight=1)

        actions = ttk.Frame(form, style="TFrame")
        actions.grid(row=4, column=0, sticky="ew", pady=(6, 0))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        self.btn_add = ttk.Button(
            actions,
            text="Guardar / Agregar",
            style="Accent.TButton",
            command=self.on_add_task,
        )
        self.btn_add.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.btn_complete = ttk.Button(
            actions,
            text="Marcar como completada",
            style="Ghost.TButton",
            command=self.on_complete_task,
        )
        self.btn_complete.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        actions2 = ttk.Frame(form, style="TFrame")
        actions2.grid(row=5, column=0, sticky="ew", pady=(4, 0))
        actions2.grid_columnconfigure(0, weight=1)
        actions2.grid_columnconfigure(1, weight=1)

        self.btn_modify = ttk.Button(
            actions2,
            text="Modificar descripción",
            style="Ghost.TButton",
            command=self.on_modify_task,
        )
        self.btn_modify.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.btn_delete = ttk.Button(
            actions2,
            text="Eliminar tarea",
            style="Ghost.TButton",
            command=self.on_delete_task,
        )
        self.btn_delete.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        detail_card = ttk.Frame(center_panel, style="Card.TFrame")
        detail_card.grid(row=2, column=0, sticky="nsew", pady=(10, 0))

        detail = ttk.Frame(detail_card, style="TFrame")
        detail.pack(fill="both", expand=True, padx=16, pady=14)
        detail.grid_columnconfigure(0, weight=1)

        ttk.Label(detail, text="Resumen selección", style="Muted.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.lbl_detail_title = ttk.Label(
            detail, text="Sin tarea seleccionada", style="SectionTitle.TLabel"
        )
        self.lbl_detail_title.grid(row=1, column=0, sticky="w", pady=(2, 2))

        self.lbl_detail_status = ttk.Label(
            detail, text="", style="Muted.TLabel"
        )
        self.lbl_detail_status.grid(row=2, column=0, sticky="w")

        right_panel = ttk.Frame(main_card, style="TFrame")
        right_panel.grid(row=1, column=2, sticky="nsew", padx=(9, 18), pady=(8, 18))
        right_panel.grid_rowconfigure(1, weight=1)

        right_header = ttk.Frame(right_panel, style="TFrame")
        right_header.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        ttk.Label(
            right_header, text="Completadas", style="SectionTitle.TLabel"
        ).pack(side="left")

        self.lbl_completed_count = ttk.Label(
            right_header, text="0 tareas", style="Muted.TLabel"
        )
        self.lbl_completed_count.pack(side="right")

        self.completed_list = self._create_listbox(right_panel)
        self.completed_list.grid(row=1, column=0, sticky="nsew")

        self._get_listbox_widget(self.pending_list).bind(
            "<<ListboxSelect>>", self.on_select_pending
        )
        self._get_listbox_widget(self.completed_list).bind(
            "<<ListboxSelect>>", self.on_select_completed
        )

    def _create_listbox(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        lb = tk.Listbox(
            frame,
            bg="#020617",
            fg="#e5e7eb",
            selectbackground="#312e81",
            selectforeground="#f9fafb",
            activestyle="none",
            highlightthickness=0,
            bd=0,
            relief="flat",
            font=("Segoe UI", 10),
        )
        lb.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=lb.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        lb.configure(yscrollcommand=scroll.set)

        return frame

    def _get_listbox_widget(self, container):
        for child in container.winfo_children():
            if isinstance(child, tk.Listbox):
                return child
        return None

    def _refresh_lists(self):
        pending_lb = self._get_listbox_widget(self.pending_list)
        completed_lb = self._get_listbox_widget(self.completed_list)
        pending_lb.delete(0, "end")
        completed_lb.delete(0, "end")

        tasks = self.task_list.get_all_tasks()
        for t in tasks:
            if t["completed"]:
                completed_lb.insert("end", t["name"])
            else:
                pending_lb.insert("end", t["name"])

        pending_count = sum(1 for t in tasks if not t["completed"])
        completed_count = sum(1 for t in tasks if t["completed"])
        self.lbl_pending_count.config(text=f"{pending_count} tareas")
        self.lbl_completed_count.config(text=f"{completed_count} tareas")

    def _clear_form(self):
        self.entry_title.delete(0, "end")
        self.text_description.delete("1.0", "end")

    def _fill_form(self, name, description):
        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, name)
        self.text_description.delete("1.0", "end")
        self.text_description.insert("1.0", description)

    def _set_detail(self, name=None, completed=None):
        if name is None:
            self.lbl_detail_title.config(text="Sin tarea seleccionada")
            self.lbl_detail_status.config(text="")
            return
        estado = "Completada" if completed else "Pendiente"
        self.lbl_detail_title.config(text=name)
        self.lbl_detail_status.config(text=f"Estado: {estado}")

    def _find_task(self, name):
        for t in self.task_list.get_all_tasks():
            if t["name"] == name:
                return t
        return None

    def on_add_task(self):
        name = self.entry_title.get().strip()
        description = self.text_description.get("1.0", "end").strip()

        if not name:
            messagebox.showwarning("Validación", "El nombre de la tarea no puede estar vacío.")
            return

        existente = self._find_task(name)
        if existente:
            self.task_list.modify_task(name, description)
        else:
            self.task_list.add_task(name, description)

        self._clear_form()
        self._set_detail()
        self._refresh_lists()

    def on_complete_task(self):
        pending_lb = self._get_listbox_widget(self.pending_list)
        sel = pending_lb.curselection()
        if not sel:
            messagebox.showinfo("Información", "Selecciona una tarea pendiente para marcarla como completada.")
            return
        name = pending_lb.get(sel[0])

        ok = self.task_list.complete_task(name)
        if not ok:
            messagebox.showerror("Error", "No se encontró la tarea seleccionada.")
            return

        self._refresh_lists()
        t = self._find_task(name)
        if t:
            self._fill_form(t["name"], t["description"])
            self._set_detail(t["name"], t["completed"])
        else:
            self._clear_form()
            self._set_detail()

    def on_modify_task(self):
        name = self.entry_title.get().strip()
        description = self.text_description.get("1.0", "end").strip()

        if not name:
            messagebox.showwarning("Validación", "Escribe el nombre de la tarea que quieres modificar.")
            return

        ok = self.task_list.modify_task(name, description)
        if not ok:
            messagebox.showinfo("Información", "No se encontró una tarea con ese nombre.")
            return

        self._refresh_lists()
        t = self._find_task(name)
        if t:
            self._fill_form(t["name"], t["description"])
            self._set_detail(t["name"], t["completed"])

    def on_delete_task(self):
        name = self.entry_title.get().strip()
        if not name:
            messagebox.showwarning("Validación", "Escribe el nombre de la tarea a eliminar o selecciónala en la lista.")
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar la tarea '{name}'?"):
            return

        ok = self.task_list.remove_task(name)
        if not ok:
            messagebox.showinfo("Información", "No se encontró una tarea con ese nombre.")
            return

        self._clear_form()
        self._set_detail()
        self._refresh_lists()

    def on_select_pending(self, event=None):
        lb = self._get_listbox_widget(self.pending_list)
        sel = lb.curselection()
        if not sel:
            return
        name = lb.get(sel[0])
        t = self._find_task(name)
        if t:
            self._fill_form(t["name"], t["description"])
            self._set_detail(t["name"], t["completed"])

    def on_select_completed(self, event=None):
        lb = self._get_listbox_widget(self.completed_list)
        sel = lb.curselection()
        if not sel:
            return
        name = lb.get(sel[0])
        t = self._find_task(name)
        if t:
            self._fill_form(t["name"], t["description"])
            self._set_detail(t["name"], t["completed"])


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()

