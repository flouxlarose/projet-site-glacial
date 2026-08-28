import tkinter as tk

class SimulationView:
    def __init__(self, root, controller, width=968, height=720):
        self.root = root
        self.controller = controller
        self.width = width
        self.height = height

        # 1. Configuration de la fenêtre principale
        self.root.title("Simulateur d'environnement — site glacial")
        self.root.geometry("1280x800")
        
        # Position du viseur et paramètres de mouvement fluide
        self.cam_x = 1840.0
        self.cam_y = 1120.0
        self.cam_w = 968
        self.cam_h = 720
        self.cam_speed = 15.0
        self.keys_pressed = {"Left": False, "Right": False, "Up": False, "Down": False}

        # Position initiale du curseur pour le glisser-déplacer (drag & drop)
        self.drag_start_x = 0
        self.drag_start_y = 0

        # 2. Barre de Menu supérieure
        self.menubar = tk.Menu(self.root)
        for menu_name in ["Fichier", "Édition", "Simulation", "Vue", "Aide"]:
            self.menubar.add_cascade(label=menu_name, menu=tk.Menu(self.menubar, tearoff=0))
        self.root.config(menu=self.menubar)
        
        # 3. En-tête avec Seed
        self.header_frame = tk.Frame(self.root, bg="#e8e8e8")
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(self.header_frame, text="Simulateur d'environnement — site glacial", font=("Arial", 11, "bold"), bg="#e8e8e8").pack(side=tk.LEFT, padx=10, pady=2)
        self.lbl_seed = tk.Label(self.header_frame, text="seed 1742", font=("Arial", 10), bg="#e8e8e8")
        self.lbl_seed.pack(side=tk.LEFT, padx=150)

        # 4. Zone principale & Création des composants UI
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Création du Canvas principal
        self.canvas = tk.Canvas(self.main_container, width=self.width, height=self.height, bg="#2b323b")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Création du Panneau Latéral Droit
        self.sidebar = tk.Frame(self.main_container, width=280, bg="#f4f5f7", relief=tk.RIDGE, bd=1)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        self._build_sidebar()

        # 5. Liaisons d'événements Souris (exécuté APRÈS la création de self.canvas)
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        
        # 6. Liaisons d'événements Clavier
        self.root.bind("<KeyPress-Left>", lambda e: self._set_key("Left", True))
        self.root.bind("<KeyRelease-Left>", lambda e: self._set_key("Left", False))
        self.root.bind("<KeyPress-Right>", lambda e: self._set_key("Right", True))
        self.root.bind("<KeyRelease-Right>", lambda e: self._set_key("Right", False))
        self.root.bind("<KeyPress-Up>", lambda e: self._set_key("Up", True))
        self.root.bind("<KeyRelease-Up>", lambda e: self._set_key("Up", False))
        self.root.bind("<KeyPress-Down>", lambda e: self._set_key("Down", True))
        self.root.bind("<KeyRelease-Down>", lambda e: self._set_key("Down", False))

    def _on_drag_start(self, event):
        """Enregistre le point de départ du clic de la souris."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_drag_motion(self, event):
        """Calcule le décalage et déplace le viseur au fur et à mesure du glissement."""
        dx = self.drag_start_x - event.x
        dy = self.drag_start_y - event.y

        self.cam_x = max(0.0, min(4000.0 - self.cam_w, self.cam_x + dx))
        self.cam_y = max(0.0, min(4000.0 - self.cam_h, self.cam_y + dy))

        self.drag_start_x = event.x
        self.drag_start_y = event.y

        self.controller.request_immediate_redraw()

    def _set_key(self, key, is_pressed):
        self.keys_pressed[key] = is_pressed

    def update_camera_position(self):
        """Mise à jour fluide de la position de la caméra basée sur les touches actives."""
        dx = 0
        dy = 0
        if self.keys_pressed["Left"]:  dx -= self.cam_speed
        if self.keys_pressed["Right"]: dx += self.cam_speed
        if self.keys_pressed["Up"]:    dy -= self.cam_speed
        if self.keys_pressed["Down"]:  dy += self.cam_speed

        if dx != 0 or dy != 0:
            self.cam_x = max(0.0, min(4000.0 - self.cam_w, self.cam_x + dx))
            self.cam_y = max(0.0, min(4000.0 - self.cam_h, self.cam_y + dy))
            return True
        return False

    def _build_sidebar(self):
        tk.Label(self.sidebar, text="Contrôle", font=("Arial", 12, "bold"), bg="#f4f5f7", anchor="w").pack(fill=tk.X, padx=10, pady=(10, 5))
        tk.Label(self.sidebar, text="Défilement temporel", font=("Arial", 9, "bold"), fg="#334155", bg="#f4f5f7", anchor="w").pack(fill=tk.X, padx=10, pady=(5, 2))
        
        f_btns1 = tk.Frame(self.sidebar, bg="#f4f5f7")
        f_btns1.pack(fill=tk.X, padx=10, pady=2)
        self.btn_pause = tk.Button(f_btns1, text="Pause", width=10, command=self.controller.toggle_pause)
        self.btn_pause.pack(side=tk.LEFT, padx=2)
        self.btn_step = tk.Button(f_btns1, text="Pas", width=10, command=self.controller.step_once)
        self.btn_step.pack(side=tk.RIGHT, padx=2)
        
        f_btns2 = tk.Frame(self.sidebar, bg="#f4f5f7")
        f_btns2.pack(fill=tk.X, padx=10, pady=2)
        tk.Button(f_btns2, text="1 tick/s", width=10, command=lambda: self.controller.set_speed(1000)).pack(side=tk.LEFT, padx=2)
        tk.Button(f_btns2, text="4 tick/s", width=10, command=lambda: self.controller.set_speed(250)).pack(side=tk.RIGHT, padx=2)
        
        tk.Button(self.sidebar, text="Saison (rapide)", command=lambda: self.controller.set_speed(50)).pack(fill=tk.X, padx=12, pady=4)
        
        tk.Label(self.sidebar, text="État", font=("Arial", 10, "bold"), bg="#f4f5f7", anchor="w").pack(fill=tk.X, padx=10, pady=(15, 2))
        
        self.lbl_tick = self._add_stat_row("Tick", "47")
        self.lbl_day = self._add_stat_row("Jour local", "12")
        self.lbl_temp = self._add_stat_row("T viseur", "-4.1 °C")
        self.lbl_opacity = self._add_stat_row("Opacité ceinture", "0.12")
        self.lbl_pools = self._add_stat_row("Flaques ouvertes", "3")
        
        tk.Label(self.sidebar, text="Carte 4000 × 4000", font=("Arial", 10, "bold"), bg="#f4f5f7", anchor="w").pack(fill=tk.X, padx=10, pady=(15, 2))
        tk.Label(self.sidebar, text="Clic : déplacer le viseur", font=("Arial", 8), fg="#666", bg="#f4f5f7", anchor="w").pack(fill=tk.X, padx=10)
        
        self.minimap = tk.Canvas(self.sidebar, width=220, height=220, bg="#a0b4c8", highlightthickness=1, highlightbackground="#ccc")
        self.minimap.pack(padx=10, pady=5)
        self.minimap.bind("<Button-1>", self._on_minimap_click)

    def _add_stat_row(self, label, default_val):
        row = tk.Frame(self.sidebar, bg="#f4f5f7")
        row.pack(fill=tk.X, padx=10, pady=1)
        tk.Label(row, text=label, font=("Arial", 9), bg="#f4f5f7", anchor="w").pack(side=tk.LEFT)
        lbl_val = tk.Label(row, text=default_val, font=("Arial", 9), bg="#f4f5f7", anchor="e")
        lbl_val.pack(side=tk.RIGHT)
        return lbl_val

    def _on_minimap_click(self, event):
        scale = 4000 / 220
        self.cam_x = max(0.0, min(4000.0 - self.cam_w, event.x * scale - self.cam_w / 2))
        self.cam_y = max(0.0, min(4000.0 - self.cam_h, event.y * scale - self.cam_h / 2))
        self.controller.request_immediate_redraw()

    def world_to_screen(self, x, y):
        return x - self.cam_x, y - self.cam_y

    def draw(self, model):
        self.canvas.delete("all")
        
        # 1. Rendu du terrain
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#cce0ee", outline="")

        # Dalles de basalte
        for bx, by, bw, bh in [(1000, 800, 2200, 2000), (800, 1500, 2400, 1500)]:
            sx, sy = self.world_to_screen(bx, by)
            self.canvas.create_rectangle(sx, sy, sx+bw, sy+bh, fill="#34383d", outline="#1a1c1e", width=2)

        # Île ocre
        ox1, oy1, ox2, oy2 = model.ocre_zone
        sx1, sy1 = self.world_to_screen(ox1, oy1)
        sx2, sy2 = self.world_to_screen(ox2, oy2)
        self.canvas.create_oval(sx1, sy1, sx2, sy2, fill="#b5834a", outline="#7a5229", width=3)

        # Flaque
        fx, fy = self.world_to_screen(2300, 2100)
        self.canvas.create_oval(fx-60, fy-30, fx+60, fy+30, fill="#2b5c6e", outline="#4fa3a8", width=2)

        # 2. Veines
        for vein in model.veins:
            pts_screen = []
            for vx, vy in vein.points:
                pts_screen.extend(self.world_to_screen(vx, vy))
            if len(pts_screen) >= 4:
                self.canvas.create_line(pts_screen, fill="#d9381e", width=5, smooth=True)

        # 3. Station
        st_x, st_y = self.world_to_screen(2000, 1600)
        self.canvas.create_rectangle(st_x-80, st_y-50, st_x+40, st_y+40, fill="#4a5a6a", outline="#1e2630", width=2)
        self.canvas.create_arc(st_x-80, st_y-50, st_x-20, st_y+30, start=0, extent=180, fill="#7da3a1", outline="#1e2630")
        self.canvas.create_rectangle(st_x+40, st_y-30, st_x+90, st_y+30, fill="#3a4856", outline="#1e2630", width=2)

        # 4. Flore
        for col in model.columns:
            cx, cy = self.world_to_screen(col.x, col.y)
            self.canvas.create_oval(cx-col.radius-5, cy-8, cx+col.radius+5, cy+8, fill="#4d6134", outline="")
            self.canvas.create_polygon(cx-col.radius, cy, cx+col.radius, cy, cx, cy-col.height, fill="#9e8e78", outline="#5e5243", width=2)

        # 5. Faune
        for ax, ay in model.arthropods:
            sx, sy = self.world_to_screen(ax, ay)
            self.canvas.create_oval(sx-3, sy-3, sx+3, sy+3, fill="#111111", outline="#555555")

        for amx, amy in model.amphibians:
            sx, sy = self.world_to_screen(amx, amy)
            self.canvas.create_oval(sx-5, sy-4, sx+5, sy+4, fill="#2e7d32", outline="#81c784")

        # 6. Overlay Viseur
        cam_info = f"VISEUR x {int(self.cam_x)}-{int(self.cam_x+self.cam_w)}  y {int(self.cam_y)}-{int(self.cam_y+self.cam_h)}   {self.cam_w}x{self.cam_h} u"
        self.canvas.create_rectangle(10, 10, 270, 32, fill="#111111", outline="")
        self.canvas.create_text(15, 21, text=cam_info, fill="#ffffff", font=("Consolas", 8), anchor="w")

        k = 20
        self.canvas.create_line(5, k, 5, 5, k, 5, fill="#ffffff", width=2)
        self.canvas.create_line(self.width-k, 5, self.width-5, 5, self.width-5, k, fill="#ffffff", width=2)
        self.canvas.create_line(5, self.height-k, 5, self.height-5, k, self.height-5, fill="#ffffff", width=2)
        self.canvas.create_line(self.width-k, self.height-5, self.width-5, self.height-5, self.width-5, self.height-k, fill="#ffffff", width=2)

        # 7. Sidebar stats
        c = model.current_climate
        self.lbl_tick.config(text=str(model.clock.tick))
        self.lbl_day.config(text=str(model.clock.day))
        self.lbl_temp.config(text=f"{c['temperature']:.1f} °C")
        self.lbl_opacity.config(text=f"{c['opacity']:.2f}")
        
        self.draw_minimap(model)

    def draw_minimap(self, model):
        self.minimap.delete("all")
        scale = 220 / 4000
        
        self.minimap.create_rectangle(0, 0, 220, 220, fill="#a0b4c8", outline="")
        self.minimap.create_rectangle(50, 40, 180, 180, fill="#34383d", outline="")
        
        ox1, oy1, ox2, oy2 = model.ocre_zone
        self.minimap.create_polygon(
            ox1*scale, (oy1+300)*scale, 
            (ox2-200)*scale, oy1*scale, 
            ox2*scale, (oy2-200)*scale, 
            ox1*scale, oy2*scale, 
            fill="#b5834a", outline=""
        )
        
        for vein in model.veins:
            pts = [(x * scale, y * scale) for x, y in vein.points]
            flat_pts = [coord for pt in pts for coord in pt]
            if len(flat_pts) >= 4:
                self.minimap.create_line(flat_pts, fill="#d9381e", width=2)
                
        vx1, vy1 = self.cam_x * scale, self.cam_y * scale
        vx2, vy2 = (self.cam_x + self.cam_w) * scale, (self.cam_y + self.cam_h) * scale
        self.minimap.create_rectangle(vx1, vy1, vx2, vy2, outline="#ffd700", width=2)