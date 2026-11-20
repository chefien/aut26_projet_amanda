import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class shopFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#9fb498", corner_radius=0)
        self.master_app = master.master #MainApp (.user et .data)
        self.game_screen = master

        #### (Vente | Achats | Comparaison) ###

        self.nav_frame = ctk.CTkFrame(self, fg_color="#6e7a68", height=50, corner_radius=10)
        self.nav_frame.pack(fill="x", padx=20, pady=(15, 10))

        btn_font = ("arial", 14, "bold") #comme ca c'est pareil partout
        ##vente
        self.btn_vente = ctk.CTkButton(self.nav_frame, text="vente", font=btn_font, fg_color="#f1e9c8", text_color="#000000", hover_color="#e2dbc0", command=lambda: self.switch_shop_tab("vente"))
        self.btn_vente.pack(side="left", padx=20, pady=10)
        ##achat
        self.btn_shop = ctk.CTkButton(self.nav_frame, text="achats", font=btn_font, fg_color="#f1e9c8", text_color="#000000", hover_color="#e2dbc0", command=lambda: self.switch_shop_tab("achats"))
        self.btn_shop.pack(side="left", padx=20, pady=10)
        ##comparaison
        self.btn_comparaison = ctk.CTkButton(self.nav_frame, text="comparaison prix de ventes", font=btn_font, fg_color="#f1e9c8", text_color="#000000", hover_color="#e2dbc0", command=lambda: self.switch_shop_tab("comparaison"))
        self.btn_comparaison.pack(side="left", padx=20, pady=10)


        # le container pour tout
        self.content_container = ctk.CTkFrame(self, fg_color="#9fb498")
        self.content_container.pack(expand=True, fill="both", padx=20, pady=10)

        self.content_container.grid_columnconfigure(0, weight=3) # gauche
        self.content_container.grid_columnconfigure(1, weight=1) #droite (plus petit)
        self.content_container.grid_rowconfigure(0, weight=1)

        # le container de gauche
        self.left_view_container = ctk.CTkFrame(self.content_container, fg_color="#dee6ed", corner_radius=10)
        self.left_view_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # le container de droite 
        self.create_right_panel()

        # la vue de defaut est celui de vente
        self.switch_shop_tab("vente")


    def switch_shop_tab(self, tab_name):
        # detruit ce qui se trouve dans le left container
        for widget in self.left_view_container.winfo_children():
            widget.destroy()
        plt.close('all')

        if tab_name == "vente":
            self.create_vente_view()
        elif tab_name == "achats":
            self.create_shop_view()
        elif tab_name == "comparaison":
            self.create_comparaison_view()


    #############
    ####VENTE####
    #############
    def create_vente_view(self):
        self.left_view_container.grid_columnconfigure(0, weight=1, uniform="split")
        self.left_view_container.grid_columnconfigure(1, weight=1, uniform="split")
        self.left_view_container.grid_rowconfigure(0, weight=1)

        # inventaire des poissons
        self.inv_frame = ctk.CTkScrollableFrame(self.left_view_container, fg_color="#dee6ed")
        self.inv_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # A FAIRE: Implementer l'inventaire des poissons qui ont ete attrapé
        placeholder_label = ctk.CTkLabel(self.inv_frame, text="[ Inventaire / Options de poissons ici ]", font=("arial", 12))
        placeholder_label.pack(pady=20)

        # tous les poissons du poisson choisis
        self.selection_frame = ctk.CTkScrollableFrame(self.left_view_container, fg_color="#f5f2eb")
        self.selection_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        sel_title = ctk.CTkLabel(self.selection_frame, 
                                 text="Aucun poisson de selectionné", 
                                 font=("arial", 16, "bold"),
                                 wraplength=180,
                                 justify = "left")
        sel_title.pack(pady=10)
        
        # A FAIRE: la selection du poisson

    ##############    
    ####ACHATS####
    ##############
    def create_shop_view(self):
        self.left_view_container.grid_columnconfigure(0, weight=1)
        self.left_view_container.grid_rowconfigure(0, weight=1)

        self.shop_scroll = ctk.CTkScrollableFrame(self.left_view_container, fg_color="#dee6ed")
        self.shop_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.shop_scroll.grid_columnconfigure(0, weight=1)
        self.shop_scroll.grid_columnconfigure(1, weight=1)

        upgrade_data = [
            ("Augmente le temps de pêche de 0.5s", "250$", "#bce1f5","#6c9fb8"),
            ("Augmente le temps de pêche de 1s", "300$", "#a2e8c1","#63af85"),
            ("Multiplie ton nombre de clicks par x2", "1000$", "#f3d179","#c4a046"),
            ("Multiplie le prix de vente par x1.5", "1500$", "#f092e0","#bc5fac")
        ]

        row, col = 0, 0
        for text, price, color, h_color in upgrade_data:
            card_text = f"{text}\n\n{price}"
            
            card = ctk.CTkButton(
                self.shop_scroll, 
                text=card_text, 
                font=("arial", 13, "bold"),
                text_color="#000000",
                fg_color=color, 
                hover_color=h_color, 
                corner_radius=12,
                height=110,
                command=None
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            col += 1
            if col > 1:
                col = 0
                row += 1

    ##graphique
    def create_comparaison_view(self):
        graph_title = ctk.CTkLabel(self.left_view_container, text="Prix moyen par type de poisson", font=("arial", 18, "bold"))
        graph_title.pack(pady=(15, 5))

        # A FAIRE: graphique en ce moment vide
        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#dee6ed")
        ax.set_facecolor("#f5f2eb")
        
        # vide vide vide
        ax.set_ylabel("$")
        ax.set_ylim(0, 100)
        ax.axhline(20, color="#dddddd", linestyle="--", linewidth=0.8)
        ax.axhline(40, color="#dddddd", linestyle="--", linewidth=0.8)
        ax.axhline(60, color="#dddddd", linestyle="--", linewidth=0.8)
        ax.axhline(80, color="#dddddd", linestyle="--", linewidth=0.8)

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.left_view_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=15, pady=10)

    #######################################
    ####CONTAINER DE DROITE: LE VENDEUR####
    #######################################

    def create_right_panel(self):
        right_panel = ctk.CTkFrame(self.content_container, fg_color="#5f665a", corner_radius=10)
        right_panel.grid(row=0, column=1, sticky="nsew")

        # montre l'argent
        self.money_label = ctk.CTkLabel(right_panel, text="Poissonnier\nargent: 250 $", font=("arial", 16, "bold"), text_color="#ffffff")
        self.money_label.pack(pady=(20, 10))

        # A FAIRE: image du vendeur
        self.vendor_img_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b", width=180, height=180, corner_radius=0)
        self.vendor_img_frame.pack(pady=5)
        self.vendor_img_frame.pack_propagate(False)
        
        vendor_placeholder = ctk.CTkLabel(self.vendor_img_frame, text="[ Image Vendor TO DO ]", text_color="#ffffff")
        vendor_placeholder.pack(expand=True)

        #modifie dependant de ce qui se passe
        self.dialogue_lbl = ctk.CTkLabel(right_panel, text="- bienvenue ! ", font=("arial", 13, "italic"), text_color="#ffffff")
        self.dialogue_lbl.pack(pady=10)

        # bouton qui modifie selon le panel
        self.action_btn = ctk.CTkButton(
            right_panel, 
            text="Vendre x0\n(0$)", 
            font=("arial", 14, "bold"),
            fg_color="#ff6b6b", 
            hover_color="#fa5252",
            text_color="#000000",
            corner_radius=20,
            height=50,
            width=140,
            command=None # pas de commandes encore
        )
        self.action_btn.pack(side="bottom", pady=25)

    def shopScreen(self):
        return self

    def pricePerCatch(self, catch):
        factor = ((catch.weight / (catch.weight + 2.0)) + (catch.size / (catch.size + 40.0)))/2
        base_price = 8.0+(4*factor) #entre 8 et 12$

        return round(base_price*self.getRarityMult(catch.rarity),2)

    def getRarityMult(self, rarity):
        temp_dict_rarity_mult = {
            "common": 1.0,
            "uncommon": 1.5,
            "rare": 2.5,
            "epic": 4.5,
            "legendary": 7
        }
        return temp_dict_rarity_mult[rarity]