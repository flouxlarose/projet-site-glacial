import tkinter as tk
from Modele import SimulationModel
from Vue import SimulationView

class SimulationController:
    def __init__(self, seed=1742):
        self.root = tk.Tk()
        self.model = SimulationModel(seed=seed)
        self.view = SimulationView(self.root, self)
        
        self.running = True
        self.tick_delay_ms = 1000  # Vitesse de la simulation (1 tick/s)
        
        # Lancement des deux boucles distinctes
        self.schedule_render_loop()
        self.schedule_simulation_tick()

    def toggle_pause(self):
        self.running = not self.running
        self.view.btn_pause.config(text="Jouer" if not self.running else "Pause")

    def step_once(self):
        self.model.update()
        self.view.draw(self.model)

    def set_speed(self, delay_ms):
        self.tick_delay_ms = delay_ms
        self.running = True
        self.view.btn_pause.config(text="Pause")

    def render_loop(self):
        """Boucle d'affichage haute fréquence (60 FPS) pour un déplacement fluide."""
        camera_moved = self.view.update_camera_position()
        if camera_moved:
            self.view.draw(self.model)
        self.schedule_render_loop()

    def simulation_loop(self):
        """Boucle logique du Modèle qui avance selon le pas de temps défini."""
        if self.running:
            self.model.update()
            self.view.draw(self.model)
        self.schedule_simulation_tick()

    def schedule_render_loop(self):
        # ~60 FPS (16 ms)
        self.root.after(16, self.render_loop)

    def schedule_simulation_tick(self):
        self.root.after(self.tick_delay_ms, self.simulation_loop)

    def request_immediate_redraw(self):
        """Redessine immédiatement la vue lors d'un déplacement à la souris."""
        self.view.draw(self.model)

    def run(self):
        self.view.draw(self.model)
        self.root.mainloop()

if __name__ == "__main__":
    app = SimulationController(seed=1742)
    app.run()