import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from classe_khadija import ImageConfig, GifImage

class shopFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#9fb498", corner_radius=0)
        self.master_app = master.master #MainApp (.user et .data)
        self.game_screen = master

        #### (Vente | Achats | Comparaison) ###

        self.nav_frame = ctk.CTkFrame(self, fg_color="#9fb498", height=50, corner_radius=10)
        self.nav_frame.pack(fill="x", padx=20, pady=(5,0))

        self.current_fishes_sale = []

        btn_font = ("arial", 14, "bold") #comme ca c'est pareil partout
        ##vente
        self.btn_vente = ctk.CTkButton(self.nav_frame, text="vente", font=btn_font, fg_color="#f1e9c8", text_color="#000000", hover_color="#e2dbc0", command=lambda: self.switch_shop_tab("vente"))
        self.btn_vente.pack(side="left", padx=20)
        ##achat
        self.btn_shop = ctk.CTkButton(self.nav_frame, text="achats", font=btn_font, fg_color="#f1e9c8", text_color="#000000", hover_color="#e2dbc0", command=lambda: self.switch_shop_tab("achats"))
        self.btn_shop.pack(side="left", padx=20)
        self.card_shop_dict = dict()
        ##comparaison
        self.btn_comparaison = ctk.CTkButton(self.nav_frame, text="comparaison prix de ventes", font=btn_font, fg_color="#f1e9c8", text_color="#000000", hover_color="#e2dbc0", command=lambda: self.switch_shop_tab("comparaison"))
        self.btn_comparaison.pack(side="left", padx=20)


        # le container pour tout
        self.content_container = ctk.CTkFrame(self, fg_color="#9fb498")
        self.content_container.pack(expand=True, fill="both", padx=20, pady=(5,10))

        self.content_container.grid_columnconfigure(0, weight=3) # gauche
        self.content_container.grid_columnconfigure(1, weight=1) #droite (plus petit)
        self.content_container.grid_rowconfigure(0, weight=1)

        # le container de gauche
        self.left_view_container = ctk.CTkFrame(self.content_container, fg_color="#dee6ed", corner_radius=10)
        self.left_view_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # le container de droite 
        self.create_right_panel()

        # la vue de defaut est celui de vente

        self.switch_shop_tab('vente')


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

        self.reset_vendor_ui(tab_name)

    def reset_vendor_ui(self,tab_name):
        self.current_fishes_sale = []
        
        if tab_name == "vente":
            self.action_btn.pack(side="bottom", pady=25)
            self.action_btn.configure(text="Vendre x0\n(0$)", command = None)

        elif tab_name == "achats":
            self.action_btn.pack(side="bottom", pady=25)
            self.action_btn.configure(text="Acheter\n(0$)", command = None)
        
        elif tab_name == "comparaison":
            self.action_btn.configure(command = None)            
            self.action_btn.pack_forget()


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
        

        # tous les poissons du poisson choisis
        self.selection_frame = ctk.CTkScrollableFrame(self.left_view_container, fg_color="#f5f2eb")
        self.selection_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.sel_title = ctk.CTkLabel(self.selection_frame, 
                                 text="Aucun poisson de selectionné", 
                                 font=("arial", 16, "bold"),
                                 wraplength=180)
        self.sel_title.pack(pady=10)
        
        self.place_inventory_grid()
    
    def place_inventory_grid(self):
        #nmb de poissons attrapés
        #qui sont les poissons
        #placer image bouton

        ##dimensions image

        height = 120
        width = height

        current_row = 0
        current_column = 0

        self.inventory_dict = dict()

        seen_names = set()

        for catch in self.master_app.user.getUserInventory():
            name = catch.getName()
            if name not in seen_names and catch.getIsFish():
                seen_names.add(name)

                path = f"assets/{name}.png"
                current_fish_image = ImageConfig(path,height,width)
                current_button = ctk.CTkButton(self.inv_frame,
                                            image=current_fish_image.getImage(),
                                                command = lambda n=name: self.selected_fish(n),
                                                border_color ="#66ce7f", 
                                                border_width=0,
                                                text = '',
                                                fg_color="#dee6ed",
                                                height=height,width=width,
                                                hover_color="#fcf8f8",
                                                corner_radius=0)
                current_button.grid(pady = 5,padx = 5,
                                    row = current_row, 
                                    column = current_column)
                

                self.inventory_dict[name] = current_button

                if current_column == 0:
                    current_column = 1
                else:
                    current_column = 0
                    current_row +=1

    def selected_fish(self, fish_name):
        self.current_selected_name = fish_name
        self.current_fishes_sale = [] #reset la liste quand on change de poissons

        for btn in self.inventory_dict.values():
            btn.configure(border_width = 0)
        print(fish_name)
        #ajouter une bordure verte
        self.inventory_dict[fish_name].configure(border_width = 2)

        #modifie le label de selection
        self.sel_title.configure(text=fish_name)
        self.show_list_selection(fish_name)
        self.update_sale_button()

    def show_list_selection(self,fish_name):
        #nmb of fishes
        self.selection_inv_dict = dict()

        list_selection = [
            f for f in self.master_app.user.getUserInventory()
            if f.getName() == fish_name
        ]

        self.sel_title.configure(text = f'Sélection : {fish_name}')

        for widget in self.selection_frame.winfo_children():
            if widget != self.sel_title:
                widget.destroy()

        for i in list_selection:

            if i.weight < 1.0:
                text = f"• {i.size:.1f} cm, {int(i.weight * 1000)} g"
            else:
                text = f"• {i.size:.1f} cm, {i.weight:.2f} kg"
        
            button = ctk.CTkButton(self.selection_frame, 
                                   fg_color="#e8e6dd", 
                                   hover_color="#cbc7b6",
                                   command = lambda i=i: self.add_selected_list_fish(i),
                                   text= text,
                                   text_color='black'
                                   )
            button.pack(padx = 5, pady = 5, fill = 'x')

            self.selection_inv_dict[i] = button

    def add_selected_list_fish(self, fish):
        #change button to deselect
        #add it to a self.list

        self.selection_inv_dict[fish].configure(fg_color = "#cbc7b6", 
                                                command = lambda i=fish: self.remove_selected_list_fish(i))
        self.current_fishes_sale.append(fish)
        self.update_sale_button()
    
    def remove_selected_list_fish(self,fish):
        self.selection_inv_dict[fish].configure(fg_color="#e8e6dd", 
                                                hover_color="#cbc7b6", 
                                                command = lambda i=fish: self.add_selected_list_fish(i))
        self.current_fishes_sale.remove(fish)
        self.update_sale_button()

    def confirm_sale(self):
        #add money
        #remove fishes from inventory

        self.master_app.user.addUserMoney(self.get_sale_amount())

        newInventory = [fish for fish in self.master_app.user.getUserInventory() if fish not in self.current_fishes_sale]

        newTotalInventory = []
        for sold in self.master_app.user.getUserTotalInventory():
            if sold in self.current_fishes_sale:    
                sold.setIsSold(True)
            newTotalInventory.append(sold)
        
        self.current_fishes_sale = []
        self.update_sale_button()
        
        self.master_app.user.setUserInventory(newInventory.copy())
        self.master_app.user.setUserTotalInventory(newTotalInventory.copy())
        self.reset_ui_after_buy()

    

    def get_sale_amount(self):
        total = 0
        for i in self.current_fishes_sale:
            total += self.pricePerCatch(i)
        return total


    def update_sale_button(self):
        count = len(self.current_fishes_sale)
        total = self.get_sale_amount()

        self.action_btn.configure(text=f"Vendre x{count}\n({total}$)",
                                  command=self.confirm_sale if count > 0 else None)

    def reset_ui_after_buy(self):

        for widget in self.inv_frame.winfo_children():
            widget.destroy()

        self.place_inventory_grid()
        if hasattr(self, "current_selected_name") and self.current_selected_name in self.inventory_dict:
            self.selected_fish(self.current_selected_name)
        else:
            for widget in self.selection_frame.winfo_children():
                if widget != self.sel_title:
                    widget.destroy()
            self.sel_title.configure(text="Aucun poisson de selectionné")


        self.money_label.configure(text=f"Poissonnier\nargent: {self.master_app.user.getUserMoney()} $")



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

        self.card_shop_dict = dict()
        self.selected_card_id = None
        purchased = self.master_app.user.getPurchasedUpgrades()

        row, col = 0, 0
        for id_num, info in self.master_app.data.getUpgrades().items():
            if id_num in purchased:
                card_text = f"{info['text']}\n\nAcheté !"
                state = "disabled"
            else:
                card_text = f"{info['text']}\n\n{int(info['price'])}$"
                state = "normal"

            card = ctk.CTkButton(
                self.shop_scroll,
                text=card_text,
                font=("arial", 13, "bold"),
                text_color="#000000",
                fg_color=info["color"],
                hover_color=info["hover_color"],
                border_color="#66ce7f",
                border_width=0,
                corner_radius=12,
                height=110,
                state=state,
                command=lambda i=id_num: self.selected_card(i)
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            self.card_shop_dict[id_num] = card

            col += 1
            if col > 1:
                col = 0
                row += 1

    def selected_card(self, card_id):
        self.selected_card_id = card_id

        for btn in self.card_shop_dict.values():
            btn.configure(border_width=0)
        self.card_shop_dict[card_id].configure(border_width=3)

        info = self.master_app.data.getUpgrades()[card_id]
        price = int(info["price"])

        if self.master_app.user.getUserMoney() >= price:
            self.action_btn.configure(text=f"Acheter\n({price}$)", command=self.confirm_purchase)
        else:
            self.action_btn.configure(text=f"Manque{price-self.master_app.user.getUserMoney()} $\n({price}$)", command=None)

    def confirm_purchase(self):
        if self.selected_card_id is None:
            return

        info = self.master_app.data.getUpgrades()[self.selected_card_id]
        price = int(info["price"])
        user = self.master_app.user

        if user.getUserMoney() < price or self.selected_card_id in user.getPurchasedUpgrades():
            return

        user.addUserMoney(-price)
        user.getPurchasedUpgrades().append(self.selected_card_id)

        stat = info["stat"]
        amount = info["amount"]
        if stat == "bonus_time":
            user.setBonusTime(user.getBonusTime() + float(amount))
        elif stat == "sell_mult":
            user.setSellMult(user.getSellMult() * float(amount))
        elif stat == "click_mult":
            user.setClickMult(user.getClickMult() * int(amount))

        self.money_label.configure(text=f"Poissonnier\nargent: {user.getUserMoney()} $")
        self.dialogue_lbl.configure(text="- merci pour ton achat !")
        self.switch_shop_tab("achats")



    ##graphique
    def create_comparaison_view(self):
        graph_title = ctk.CTkLabel(self.left_view_container, text="Prix moyen par type de poisson", font=("arial", 18, "bold"))
        graph_title.pack(pady=(15, 5))

        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#dee6ed",)
        ax.set_facecolor("#f5f2eb")
        
        self.create_graph()

        ax.set_ylabel("$")

        plt.tight_layout()

        plt.subplots_adjust(left=0.05, bottom=0.3, top = 1)

        self.canvas = FigureCanvasTkAgg(fig, master=self.left_view_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=15, pady=10)
        


    ##matplotlib graph##

    def create_graph(self):
        ##read file

        #types de poissons
        catch_list = self.master_app.data.getFishNameList()    
        x = np.array(catch_list)

        average_price_list = list()
        rarity_color_list = list()

        rarities = {
                "common": "#ea9898",
                "uncommon": "#f6e15dff",
                "rare": "#83d978",
                "epic": "#82dce4",
                "legendary": "#c064f5",
                }

        for catch_name in catch_list:
            current_catch = self.master_app.data.getFishSpecific(catch_name)
            current_catch_mean_weight = (current_catch["finishWeight"]+current_catch["startWeight"])/2.0
            current_catch_mean_size = (current_catch["finishSize"]+current_catch["startSize"])/2.0
            current_catch_rarity = current_catch["rarity"]
            average_price_list.append(self.pricePerCatch(catchweight=current_catch_mean_weight, 
                                                         catchsize= current_catch_mean_size, 
                                                         rarity=current_catch_rarity))
            
            rarity_color_list.append(self.master_app.data.getRarityColor(current_catch_rarity))
        
        #je créer des fausses bars afin de créer une legende custom

        for rarity_name in self.master_app.data.rarities:
            color = self.master_app.data.getRarityColor(rarity_name)
            plt.bar(0, 0, color=color, label=rarity_name)

        plt.legend()    
        
        y = np.array(average_price_list)

        plt.grid(axis = 'y',linewidth = "1.4", linestyle = 'dotted', zorder = 1) 
        
        bars = plt.bar(x, y, color=rarity_color_list, zorder=3)

        plt.bar_label(
            bars,         
            padding=6, 
            fmt='%.0f$',        
            fontsize=9,         
            color="#353433",
        )
        
        plt.tick_params('x', rotation = 45, rotation_mode = 'xtick')

        plt.ylim(0, max(y) * 1.12)  
             
        
        
    
    #######################################
    ####CONTAINER DE DROITE: LE VENDEUR####
    #######################################

    def create_right_panel(self):
        right_panel = ctk.CTkFrame(self.content_container, fg_color="#5f665a", corner_radius=10)
        right_panel.grid(row=0, column=1, sticky="nsew")

        # montre l'argent
        self.money_label = ctk.CTkLabel(right_panel, text=f"Poissonnier\nargent: {self.master_app.user.getUserMoney()} $", font=("arial", 16, "bold"), text_color="#ffffff")
        self.money_label.pack(pady=(20, 10))

        self.vendor_img_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b", width=210, height=252, corner_radius=0)
        self.vendor_img_frame.pack(pady=5)
        self.vendor_img_frame.pack_propagate(False)
        
        self.vendor_gif = GifImage(self.vendor_img_frame, r"assets\cat_vendor.gif",210,252,40)
        self.vendor_gif.pack(expand=True, fill="both")

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

    def pricePerCatch(self, catch = None, catchweight = None, catchsize = None, rarity = None):

        if catch is not None:
            factor = ((catch.weight / (catch.weight + 2.0)) + (catch.size / (catch.size + 40.0))) / 2
            base_price = 8.0 + (4 * factor) #entre 8 et 12$

            return int(round(base_price * self.master_app.data.getRarityMult(catch.rarity) * self.master_app.user.getSellMult(), 2))

        if catchsize is not None and catchweight is not None and rarity is not None:
            factor = ((catchweight / (catchweight + 2.0)) + (catchsize / (catchsize + 40.0))) / 2
            base_price = 8.0 + (4 * factor) #entre 8 et 12$

            return int(round(base_price * self.master_app.data.getRarityMult(rarity) * self.master_app.user.getSellMult(), 2))

        return 0
        

