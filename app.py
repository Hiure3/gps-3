import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class WazePlusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Waze-Plus GPS - Windows")
        self.geometry("1000x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Painel Lateral
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.logo = ctk.CTkLabel(self.sidebar, text="🚀 Waze-Plus Simples", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo.pack(padx=20, pady=(20, 15))

        self.lbl_origem = ctk.CTkLabel(self.sidebar, text="Origem (Lat, Lon):")
        self.lbl_origem.pack(anchor="w", padx=20)
        self.txt_origem = ctk.CTkEntry(self.sidebar)
        self.txt_origem.insert(0, "-23.55052, -46.63330")
        self.txt_origem.pack(fill="x", padx=20, pady=(0, 10))

        self.lbl_destino = ctk.CTkLabel(self.sidebar, text="Destino (Lat, Lon):")
        self.lbl_destino.pack(anchor="w", padx=20)
        self.txt_destino = ctk.CTkEntry(self.sidebar)
        self.txt_destino.insert(0, "-22.90685, -43.17290")
        self.txt_destino.pack(fill="x", padx=20, pady=(0, 15))

        self.btn = ctk.CTkButton(self.sidebar, text="Calcular Rota", command=self.calcular_rota)
        self.btn.pack(fill="x", padx=20, pady=10)

        self.info = ctk.CTkTextbox(self.sidebar, height=100)
        self.info.pack(fill="x", padx=20, pady=15)
        self.info.insert("0.0", "Pronto para navegar...\n")

        # Mapa Central
        self.mapa = TkinterMapView(self, corner_radius=10)
        self.mapa.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.mapa.set_position(-23.55052, -46.63330)
        self.mapa.set_zoom(8)
        self.caminho_atual = None

    def calcular_rota(self):
        try:
            lat1, lon1 = map(float, self.txt_origem.get().split(","))
            lat2, lon2 = map(float, self.txt_destino.get().split(","))
        except ValueError:
            self.info.delete("1.0", "end")
            self.info.insert("1.0", "Erro: Use formato 'Lat, Lon'.")
            return

        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        
        try:
            res = requests.get(url, timeout=10).json()
            route = res["routes"][0]
            coords = [(c[1], c[0]) for c in route["geometry"]["coordinates"]]
            
            if self.caminho_atual:
                self.mapa.delete(self.caminho_atual)
            
            self.caminho_atual = self.mapa.set_path(coords, color="blue", width=5)
            self.mapa.set_marker(lat1, lon1, text="Origem")
            self.mapa.set_marker(lat2, lon2, text="Destino")

            dist = round(route["distance"] / 1000, 2)
            tempo = round(route["duration"] / 60, 1)
            
            self.info.delete("1.0", "end")
            self.info.insert("1.0", f"Sucesso!\nDistância: {dist} km\nTempo: {tempo} min")
        except Exception as e:
            self.info.delete("1.0", "end")
            self.info.insert("1.0", f"Erro na rota: {str(e)}")

if __name__ == "__main__":
    app = WazePlusApp()
    app.mainloop()