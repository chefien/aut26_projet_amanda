# Classes de Amanda


import customtkinter as ctk
from classes_Émilie import User, Catch, Timer
from classe_khadija import ImageConfig, Data, SavingSystem, GifImage
from PIL import Image, ImageEnhance
import sys

##Pour les stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##individuel
from amandaFinal import shopFrame, fishing



class TitleScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #image pour le background
        bg = ImageConfig(r"assets/mainMenu.jpeg", self.master.window_width,self.master.window_height)

        self.bg_label = ctk.CTkLabel(self, text = '', image = bg.getImage())
        self.bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        self.menu_card = ctk.CTkFrame(
            self, 
            fg_color="#f1e9c8",
            width=400
        )
        self.menu_card.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        self.title_label = ctk.CTkLabel(
            self.menu_card, 
            text="Fish le poisson", 
            font=("arial", 24, "bold"),
            text_color="#1f3323"
        )
        self.title_label.pack(pady=(25, 5), padx=25)

        subtitle = ctk.CTkLabel(
            self.menu_card, 
            text="Pêchez les tous!", 
            font=("arial", 16, "italic"),
            text_color="#52796f"
        )
        subtitle.pack(pady=(0, 20))

        # boutons
        btn_w = 200
        btn_h = 38
        btn_font = ("arial", 13, "bold")
        btn_rad = 10

        TEMP_btn = ctk.CTkButton(self.menu_card, text='QUICK PLAY', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#3d5a45", hover_color="#2c4232", command=self.TEMP_on_quick_play)
        TEMP_btn.pack(pady=5)
        
        if self.master.user.getUserName() is not None:
            self.play_btn = ctk.CTkButton(self.menu_card, text='Continuer', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#3d5a45", hover_color="#2c4232", command=self.on_play)
            self.play_btn.pack(pady=5)

            self.new_play_btn = ctk.CTkButton(self.menu_card, text='Nouvelle Partie', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#b12626", hover_color="#851c1c", command=self.on_new_play)
            self.new_play_btn.pack(pady=5)
        else:
            self.play_btn = ctk.CTkButton(self.menu_card, text='Nouvelle Partie', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#3d5a45", hover_color="#2c4232", command=self.on_new_play)
            self.play_btn.pack(pady=5)

        self.load_btn = ctk.CTkButton(self.menu_card, text='Charger', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#52796f", hover_color="#3d5a45", command=self.on_load)
        self.load_btn.pack(pady=5)

        self.credit_btn = ctk.CTkButton(self.menu_card, text='Crédits', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#52796f", hover_color="#3d5a45", command=self.credit_frame)
        self.credit_btn.pack(pady=5)

        self.quit_btn = ctk.CTkButton(self.menu_card, text='Quitter', font=btn_font, width=btn_w, height=btn_h, corner_radius=btn_rad, fg_color="#8b3a3a", hover_color="#632525", command=self.master.on_closing)    
        self.quit_btn.pack(pady=(5, 25))

    def TEMP_on_quick_play(self):
        self.master.user = User()
        self.master.user.setUserName("username")
        self.master.show_frame(GameScreen)

    def on_play(self):
        self.master.show_frame(GameScreen)
    def on_new_play(self):
        self.master.show_frame(newGameScreen)

    def on_load(self):
        path = ctk.filedialog.askopenfilename(initialdir="saves",filetypes=[("Fichiers CSV", "*.csv")])
        if path:
            saving = SavingSystem(self.master.user, path, self.master.data)
            if saving.loadingFromCsv(path):
                self.master.show_frame(GameScreen)

    def credit_frame(self):
        self.master.show_frame(CreditScreen)

    

class newGameScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


        self.configure(fg_color="#9fb498") 

        self.card = ctk.CTkFrame(self, fg_color="#dee6ed", corner_radius=15, width=500)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        title = ctk.CTkLabel(self.card, text="Bienvenue dans Fish le poisson !", font=("arial", 20, "bold"), text_color="#1f2937")
        title.pack(pady=(25,10), padx=30)

        # explication du jeu
        intro_text = (
            "Lancez votre ligne et surveillez l'étang.\n"
            "Cliquez vite dès que ça mord pour remonter la prise. \n"
            "Complétez votre carnet avec les poissons les plus rares!"
        )
        self.desc_label = ctk.CTkLabel(self.card, text=intro_text, font=("arial", 13), justify="left")
        self.desc_label.pack(pady=10, padx=30)

        # Demande du nom
        self.label = ctk.CTkLabel(self.card, text="Entrez votre nom de pêcheur :", font=("arial", 13, "bold"), text_color="#1f2937")
        self.label.pack(pady=(15, 5))

        self.entry = ctk.CTkEntry(self.card, placeholder_text="Écrire ici...", width=260, height=35, corner_radius=8)
        self.entry.pack(pady=5)

        # Bouton Jouer
        self.button = ctk.CTkButton(
            self.card, 
            text="Commencer à pêcher!", 
            font=("arial", 14, "bold"),
            command=self.on_next, 
            fg_color="#3d5a45", 
            hover_color="#2c4232", 
            corner_radius=10,
            height=40,
            width=260
        )
        self.button.pack(pady=(15, 25))

    def on_next(self):
        name = self.entry.get().strip()
        
        if name == "":
            self.label.configure(text = 'Veuillez entrer un nom valide !', text_color="#b12626")
        else:
            self.master.user = User()
            self.master.user.setUserName(name)
            self.master.show_frame(GameScreen)
            

class GameScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Création du la barre d'en haut (menu)
        self.create_top_bar()

        # Le frame qui contient les trois colonnes
        self.main_container = ctk.CTkFrame(self, fg_color="#9fb498")
        self.main_container.pack(expand=True, fill="both", padx=10, pady=5)

        # coniugaration des colonnes
        self.main_container.grid_columnconfigure(0, weight=2) #gauche
        self.main_container.grid_columnconfigure(1, weight=3) #centre
        self.main_container.grid_columnconfigure(2, weight=2) #droite
        self.main_container.grid_rowconfigure(0, weight=1)

        # création des 3 sections
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        

    ############################
    # La barre d'en haut (menu)#
    ############################
    def create_top_bar(self):
       self.top_menu = ctk.CTkFrame(self, bg_color = 'transparent')
       self.top_menu.pack(side="top", fill="x", padx=10, pady=(10, 5))

       ####Boutons#####
       self.option_menu = ctk.CTkOptionMenu(self.top_menu,
                                        values = ['Sauvegarder','Charger','Retourner au menu principal'],
                                        command = self.on_select,
                                        fg_color="#52796f",
                                        button_color="#3d5a45",
                                        button_hover_color="#314837"
                                        )
       self.option_menu.pack(padx = (0,10), side = 'left')
       self.option_menu.set('Options')

      #Bouton Jeu
       self.game_btn = ctk.CTkButton(self.top_menu, 
                                      text = 'Jeu', 
                                      command = self.on_return_game,
                                      fg_color="#55B953", 
                                      hover_color="#479c5a", 
                                      corner_radius=8, 
                                      text_color="#100f0f",
                                      font = ("arial", 15, 'bold'))
       
       self.game_btn.pack(padx = 5, side = 'left') 

       """
       NOUVEAUTÉ: BOUTON SHOP
       """ 
       #Bouton Magasin
       self.shop_btn = ctk.CTkButton(self.top_menu, 
                                     text = 'Magasin', 
                                     command = self.on_shop,
                                     fg_color="#30B2A1", 
                                     hover_color="#37a395", 
                                     corner_radius=8,
                                     font = ("arial", 15, 'bold'))
       self.shop_btn.pack(padx = 10, side = 'left')

       #Bouton Stats
       self.stats_btn = ctk.CTkButton(self.top_menu, text = 'Statistiques du jeu', command = self.on_stats,fg_color="#5297A8", hover_color="#3773a3", corner_radius=8)
       self.stats_btn.pack(padx = 10, side = 'left')

    def on_select(self, choice):
        if choice == 'Sauvegarder':
            self.on_save()
        elif choice == 'Charger':
            self.on_load()
        elif choice == 'Retourner au menu principal':
            self.on_return()
            return

        self.option_menu.set('Options')
       
       
    #####################################
    #Colonne gauche, joueur + inventaire#
    #####################################
    def create_left_panel(self):
        #Creation du l'écran de gauche
        self.left_panel = ctk.CTkFrame(self.main_container,fg_color="#9fb498")
        self.left_panel.grid(row = 0, column = 0, sticky = 'nsew', pady = 10, padx = 10)

        #--------------------------------------------
        #création du frame avec les info du joueur (nom, niveau, nmb de poissons,argent)
        self.user_info_frame = ctk.CTkFrame(self.left_panel, fg_color="#dee6ed")
        self.user_info_frame.pack(side="top", pady=(0, 10), fill="x")

        self.user_info_frame.grid_columnconfigure(0, weight=1)

        # --- côté gauche ---
        self.user_name_label = ctk.CTkLabel(
            self.user_info_frame,
            text=self.master.user.getUserName(),
            font=("arial", 21, "bold"),
            wraplength=200
        )
        self.user_name_label.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 2))

        self.user_money_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"{self.master.user.getUserMoney()} $"
        )
        self.user_money_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

        # --- côté droit ---
        self.user_level_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"Niveau : {self.master.user.getUserLevel()}"
        )
        self.user_level_label.grid(row=0, column=1, sticky="e", padx=20, pady=(10, 2))

        self.user_fish_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"Poissons : {self.master.user.getUserNbFish()}"
        )
        self.user_fish_label.grid(row=1, column=1, sticky="e", padx=20, pady=(0, 10))

        #--------------------------------------------
        ##création du frame avec la ''librairie'' de tous les poissons qui est scrollable
        self.gallery_frame_scroll = ctk.CTkScrollableFrame(self.left_panel,fg_color="#dee6ed")
        self.gallery_frame_scroll.pack(side = 'top', pady = 5, fill = 'both', expand = True)
        self.gallery_frame_scroll.grid_columnconfigure(0,weight = 1)
        self.gallery_frame_scroll.grid_columnconfigure(1,weight = 1)

        
        current_row = 0
        current_column = 0

        self.gallery_dict = dict()
        for i in self.master.data.getFishNameList():
            path = f"assets/{i}.png"
            current_fish_image = ImageConfig(path,100,100)
            current_button = ctk.CTkButton(self.gallery_frame_scroll,
                                           image=current_fish_image.getImage(),
                                             command = lambda i=i: self.selected_fish(i),
                                             border_color ="#66ce7f", 
                                             border_width=0,
                                             text = '',
                                             fg_color="#dee6ed",
                                             height=100,width=100,
                                             hover_color="#fcf8f8",
                                             corner_radius=0)
            current_button.grid(pady = 5,padx = 5,
                                row = current_row, 
                                column = current_column)
            
            if not any(catch.name == i for catch in self.master.user.getUserTotalInventory()) :
                original_img = Image.open(path)

                enhancer = ImageEnhance.Brightness(original_img)
                dark_img = enhancer.enhance(0.15)

                ctk_dark_img = ctk.CTkImage(light_image=dark_img, 
                                                dark_image=dark_img, 
                                                size=(100, 100))

                current_button.configure(image = ctk_dark_img)


            self.gallery_dict[i] = current_button

            if current_column == 0:
                current_column = 1
            else:
                current_column = 0
                current_row +=1

    





    ###############################################
    #Colonne milieu, etang, timer, lancer la ligne#
    ###############################################
    def create_center_panel(self):
        self.center_panel = ctk.CTkFrame(self.main_container,fg_color="#9fb498")
        self.center_panel.grid(row = 0, column = 1, sticky = 'nsew', pady = 5, padx = 5)

        ##header avec le nom de l'environnement
        self.header_frame = ctk.CTkFrame(self.center_panel, 
                                    fg_color= "#dee6ed",
                                    corner_radius=10)
        self.header_frame.pack(fill = 'both', pady = 10, padx = 15)
        environment_name_label = ctk.CTkLabel(self.header_frame, 
                                    text= "Étang de pêche", 
                                    font=('arial', 15, 'bold'))
        environment_name_label.pack(padx = 5, pady = 5,side = 'left')
        

        #NE FONCTIONNE PAS POUR L'INSTANT
        ##le gif de l'environnement
        #environment_gif = GifImage(self.center_panel,"assets/ocean.gif", 100, 100, 5)
        #environment_gif.pack(pady = 5, padx = 5)
        path = r"assets/Enviro.png"
        environment_img = ImageConfig(path,360,360)
        self.environment_label = ctk.CTkLabel(self.center_panel, image=environment_img.getImage(),text = '')
        self.environment_label.pack()
        ##bar de progression
        self.reel_bar = ctk.CTkProgressBar(
                                            self.center_panel, 
                                            width=220, 
                                            height=14, 
                                            corner_radius=0,
                                            fg_color="#dee6ed",         
                                            progress_color="#66ce7f"  
                                        )
        self.reel_bar.pack(padx = 10, 
                            pady = 10)
        self.reel_bar.set(0)
        ##bouton de pêche
        self.fish_button = ctk.CTkButton(self.center_panel, 
                                         text = 'Lancer la ligne', 
                                         font = ('ariel',13, 'bold'),
                                         command = self.on_fishing,
                                         height=45,
                                         width=220,
                                         corner_radius=20,
                                         fg_color="#dee6ed",
                                         text_color="#000000",
                                         text_color_disabled="#000000"
                                         )
        self.fish_button.pack(padx = 10, 
                              pady = 10,
                              expand = True, 
                              ipadx = 10, 
                              ipady = 10)
        self.fishing_timer = None

        self.reset_job = None
        self.wait_job = None

        
        


    #######################################
    #Colonne de droite, détails du poisson#
    #######################################
    def create_right_panel(self):
        self.right_panel = ctk.CTkFrame(self.main_container,fg_color="#dee6ed",corner_radius=10)
        self.right_panel.grid(row = 0, column = 2, sticky = 'nsew', pady = 10, padx = 10)

        label_selec = ctk.CTkLabel(self.right_panel, text = 'Sélection :')
        label_selec.pack(pady = 5)

        self.label_fish_name =ctk.CTkLabel(self.right_panel, text = "Aucun")
        self.label_fish_name.pack(pady = 5)

        self.frame_fish_image = ctk.CTkFrame(self.right_panel, 
                                             height=150, width=150, 
                                             border_color="#9fb498", 
                                             border_width=2,
                                             corner_radius=0)
        self.frame_fish_image.pack(pady = 5)
        self.frame_fish_image.pack_propagate(False)

        fish_image = ImageConfig(r"assets/NoSelection.jpg", 150,150)
        self.label_fish_image = ctk.CTkLabel(self.frame_fish_image, 
                                             image=fish_image.getImage(),
                                             text = '')
        self.label_fish_image.pack(anchor = 'center',padx = 2, pady = 2)

        self.label_rarity = ctk.CTkLabel(self.right_panel,text = 'N/A')
        self.label_rarity.pack(pady = 5)

        label_desc = ctk.CTkLabel(self.right_panel, text = 'Description')
        label_desc.pack(pady = 5)

        self.label_fish_desc = ctk.CTkLabel(self.right_panel,text = 'Aucun poisson de sélectionné!',wraplength = 180)
        self.label_fish_desc.pack(pady = 5)

        label_inventory = ctk.CTkLabel(self.right_panel,text = 'Inventaire :')
        label_inventory.pack(pady = 5,padx = 10, anchor = 'w')

        self.inventory_frame_scroll = ctk.CTkScrollableFrame(self.right_panel)
        self.inventory_frame_scroll.pack(pady=5, padx = 10, expand = True, fill = 'both')

        self.current_selected_name = None

    #Puisque la class StatsPlot n'est pas fonctionnelle et la remise est bientôt
    def create_stats_panel(self):
        #stats du joueur
        nb_fishes = self.master.user.getUserNbFish()
        nb_junk = self.master.user.getUserNbTrash()

        #liste des poissons différents attrapés
        found_fishes = []
        for x in self.master.user.getUserTotalInventory():
            if x.isFish and x.name not in found_fishes:
                found_fishes.append(x.name)

        total_fishes = len(self.master.data.getFishNameList())
        found = len(found_fishes)
        left = total_fishes-found

        #creation des graphiques
        fig = plt.figure(figsize=(7, 3.5), facecolor="#9fb498")

        # graphique 1 - Total des prises
        ax1 = plt.subplot(1, 2, 1)
        ax1.set_facecolor("#dee6ed")
        ax1.bar(["Poissons", "Déchets"], [nb_fishes, nb_junk], color=["#66ce7f", "#a0816c"])
        ax1.set_title("Total des prises")
        #force que ce soit des entiers pour l'axe des y
        ax1.yaxis.get_major_locator().set_params(integer=True)

        #graphique 2 -Carnet de pêche
        ax2 = plt.subplot(1, 2, 2)
        ax2.set_facecolor("#9fb498")
        if total_fishes > 0:
            ax2.pie([found, left], labels=["Trouvés", "Restants"], autopct="%1.0f%%", colors=["#66ce7f", "#dee6ed"], startangle=90)
            ax2.set_title("Carnet de pêche")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.stats_container)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

        


    #######################
    #Commandes des boutons#
    #######################
    def on_save(self):
        path = ctk.filedialog.asksaveasfilename(
            initialdir="saves", 
            initialfile="save.csv",
            defaultextension=".csv", 
            filetypes=[("Fichiers CSV", "*.csv")]
        )
        if path:
            saving = SavingSystem(self.master.user, path, self.master.data)
            saving.savingToFile()
            print("Partie sauvegardée dans", path)

    def on_load(self):
        path = ctk.filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")],
                                              initialdir="saves")
        if path:
            saving = SavingSystem(self.master.user, path, self.master.data)
            
            if saving.loadingFromCsv(path):
                self.refresh_after_load()   
                print("Partie chargée depuis", path)

    def refresh_after_load(self):
        #met a jour le ui
        self.user_name_label.configure(text = self.master.user.getUserName())
        self.user_level_label.configure(text = f'Niveau : {self.master.user.getUserLevel()}')
        self.user_fish_label.configure(text = f'Poissons : {self.master.user.getUserNbFish()}')
        self.user_money_label.configure(text = f"{self.master.user.getUserMoney()} $")

        # 2.revele les poissons
        caught_names = {catch.name for catch in self.master.user.total_inventory if catch.isFish}
        for fish_name, btn in self.gallery_dict.items():
          path = f"assets/{fish_name}.png"
          if fish_name in caught_names:
              img = ImageConfig(path, 100, 100).getImage()
          else:
              dark_img = ImageEnhance.Brightness(Image.open(path)).enhance(0.15)
              img = ctk.CTkImage(light_image=dark_img, dark_image=dark_img, size=(100, 100))
          btn.configure(image=img, border_width=0)

        self.current_selected_name = None
        self.label_fish_name.configure(text="Aucun")
        self.label_rarity.configure(text="N/A")
        self.label_fish_desc.configure(text="Aucun poisson de sélectionné!")
        no_sel = ImageConfig(r"assets/NoSelection.jpg", 150, 150)
        self.label_fish_image.configure(image=no_sel.getImage())
        for widget in self.inventory_frame_scroll.winfo_children():
            widget.destroy()

        self.switch_panel('main')
                    
    def on_stats(self):            
        self.switch_panel('stats')

    def on_shop(self):
        self.switch_panel('shop')

    def on_return_game(self):
        self.switch_panel('main')

    def on_return(self):
        
        #arrete le timer s'il roulait encore
        if self.fishing_timer is not None:
            self.fishing_timer.stop()
        #cancel tous les after    
        for job_attr in ('wait_job', 'escape_job', 'reset_job'):
          job = getattr(self, job_attr, None)
          if job is not None:
              self.after_cancel(job)
              setattr(self, job_attr, None)
        # Revient à l'écran titre
        self.master.show_frame(TitleScreen)

   
    def switch_panel(self, target_name):
        '''
        switch entre main, stats et le magasin
        '''
        plt.close('all')

        # Cacher tous les containers
        if hasattr(self, 'main_container') and self.main_container.winfo_exists():
            self.main_container.pack_forget()
        
        if hasattr(self, 'stats_container') and self.stats_container.winfo_exists():
            self.stats_container.pack_forget()
            self.stats_container.destroy() # le detruit pour que le graph se reset au besoin
            
        if hasattr(self, 'shop_container') and self.shop_container.winfo_exists():
            self.shop_container.pack_forget()
            self.shop_container.destroy() # reset pour le graph soit reset aussi

        # ouvre le container demandé
        if target_name == 'main':
            self.main_container.pack(expand=True, fill="both", padx=10, pady=5)
            self.updateInfo()

        elif target_name == 'stats':
            self.stats_container = ctk.CTkFrame(self, fg_color="#9fb498")
            self.stats_container.pack(expand=True, fill="both", padx=10, pady=5)
            self.create_stats_panel()

        elif target_name == 'shop':
            self.shop_container = shopFrame(self)
            self.shop_container.pack(expand=True, fill="both", padx=10, pady=5)


    def selected_fish(self,fish_name):

            self.current_selected_name = fish_name

            for i in self.gallery_dict.values():
                i.configure(border_width = 0)
            print(fish_name)
            #ajouter une bordure verte
            self.gallery_dict[fish_name].configure(border_width = 5)

            is_caught = any(catch.name == fish_name for catch in self.master.user.total_inventory)

            if is_caught:
                self.modify_desc_fish(fish_name)
                self.modify_inventory_list(fish_name)
            else:
                self.modify_desc_fish_hidden(fish_name)

    def modify_desc_fish_hidden(self, fish_name):

            self.label_fish_name.configure(text = "???")

            self.label_fish_desc.configure(text = "Vous n'avez pas encore attrapé ce poisson")

            self.label_rarity.configure(text = '???')

            path = f"assets/{fish_name}.png"
            original_img = Image.open(path)

            enhancer = ImageEnhance.Brightness(original_img)
            dark_img = enhancer.enhance(0.15)

            ctk_dark_img = ctk.CTkImage(light_image=dark_img, 
                                            dark_image=dark_img, 
                                            size=(150, 150))
            
            self.label_fish_image.configure(image = ctk_dark_img)

            for widget in self.inventory_frame_scroll.winfo_children():
                        widget.destroy()
            
    def modify_desc_fish(self, fish_name):

            self.label_fish_name.configure(text = fish_name)

            list_fish = self.master.data.getFishSpecificStatsList(fish_name)

            self.label_fish_desc.configure(text = list_fish[-2])

            self.label_rarity.configure(text = list_fish[-1])

            path = f"assets/{fish_name}.png"
            fish_image = ImageConfig(path, 150,150)
            self.label_fish_image.configure(image = fish_image.getImage())

    def modify_inventory_list(self, fish_name):

        #nettoie toute l'information qu'il y avait avant
        for widget in self.inventory_frame_scroll.winfo_children():
            widget.destroy()
        #on ajoute les bonnes informations (les poissons)
        for x in self.master.user.inventory:
                if x.name == fish_name:

                    #si le poid est petit, on le change en g
                    if x.weight < 1.0:
                        label = ctk.CTkLabel(self.inventory_frame_scroll, text = f"• {x.size:.1f} cm, {int(x.weight * 1000)} g")
                    else:
                        label = ctk.CTkLabel(self.inventory_frame_scroll, text = f"• {x.size:.1f} cm, {x.weight:.2f} kg")

                    label.pack(pady = 5, padx = 10, anchor = 'w')

    def on_fishing(self):
        self.fishing = fishing(self.master.data, self.master.user)

        self.fish_button.configure(text = "Patientez...", state = 'disabled')
        self.wait_job = self.after(self.fishing.wait_time, self.start_bite)


    def start_bite(self):
        
        self.fishing_timer = Timer(self.header_frame, self.fishing.getTimeToCatchSeconds())
        self.fishing_timer.updateTimerWithPrint()
        self.escape_job = self.after(self.fishing.getTimeToCatchMilli(), self.on_escaped)
        

        self.fish_button.configure(
            text = "Ça mord! Cliquez vite!", 
            state = 'normal',
            command = self.on_reel_click
        )


    def on_reel_click(self):

        isCaught = self.fishing.isCaught()
        if self.fishing.getRatio() > 0.5 :
            self.fish_button.configure(text = "Presque...")
        
        self.reel_bar.set(self.fishing.getRatio())  

        if isCaught:

            catch_name = self.fishing.getCatch().getName()

            self.fish_button.configure(command=None, state = "disabled")    
            if self.fishing_timer != None:
                self.fishing_timer.stop()
            self.after_cancel(self.escape_job)

            if self.fishing.getCatch().getIsFish():
                path = f"assets/{catch_name}.png"
                current_fish_image = ImageConfig(path, 100, 100)
                self.gallery_dict[catch_name].configure(image = current_fish_image.getImage())
                self.fish_button.configure(text = f"Poisson attrapé!\n{catch_name}", fg_color="#69F0C1")
                self.show_catched_fish(catch_name)
            else:
                self.fish_button.configure(text = f"Déchet repêché...\n{catch_name}", fg_color="#949A31")


            self.user_fish_label.configure(text = f'Poissons : {self.master.user.getUserNbFish()}')
            if self.master.user.isLeveledUp():
                self.user_level_label.configure(text = f'Niveau : {self.master.user.getUserLevel()}')

            if catch_name == self.current_selected_name:
                self.modify_inventory_list(catch_name)

            self.reset_job = self.after(3000, self.normal_fish_button)

    def on_escaped(self):
        if not self.fishing.getClicksLeft() >0:
            self.fish_button.configure(text = "Le poisson s'est échappé...", state = 'disabled')
            self.reset_job = self.after(3000, self.normal_fish_button)          

            
    def show_catched_fish(self, fish_name):
        show_fish_frame = ctk.CTkFrame(self.center_panel,
                                       height=200,width=200,
                                        border_color="#FFFFFF",
                                        border_width=5,
                                       corner_radius=0)
        
        show_fish_frame.place(relx=0.5, rely=0.42, anchor='center')

        path = f"assets/{fish_name}.png"
        current_fish_image = ImageConfig(path,200,200) 
        show_fish_label = ctk.CTkLabel(show_fish_frame,
                                       image = current_fish_image.getImage(),
                                       text = '')
        show_fish_label.pack(anchor = 'center', padx = 5, pady = 5)

        self.after(3*1000, show_fish_frame.destroy) 

            
    def normal_fish_button(self):
        self.fish_button.configure(text = 'Lancer la ligne', 
                                    font = ('ariel',13, 'bold'),
                                    command = self.on_fishing,
                                    state = 'normal',
                                    fg_color="#dee6ed")
        self.reel_bar.set(0)

    def updateInfo(self):
        self.user_money_label.configure(text = f"{self.master.user.getUserMoney()} $")
        self.user_fish_label.configure(text = f"Poissons : {self.master.user.getUserNbFish()}")

        if self.current_selected_name is not None:
            self.modify_inventory_list(self.current_selected_name)

        
                

    


class CreditScreen(ctk.CTkFrame):
    def __init__(self,master):

        super().__init__(master)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(expand = True, fill = 'both')

        self.label = ctk.CTkLabel(self.scroll_frame, text = 'Crédits', font = ('ariel', 24, 'bold'))
        self.label.pack(pady = 20)

        
        by_label = ctk.CTkLabel(
            self.scroll_frame, 
            text="Projet créé par :", 
            font=("arial", 16, 'bold')
        )
        by_label.pack(pady=10)

        self.names = ctk.CTkLabel(
            self.scroll_frame, 
            text="Amanda Lidia Pulache,\nKhadija Abid et\nÉmilie Ouellet", 
            font=("arial", 16)
        )
        self.names.pack(pady=10)
        context_label = ctk.CTkLabel(
            self.scroll_frame, 
            text="Dans le contexte du cours", 
            font=("arial", 16, 'bold')
        )
        context_label.pack(pady=10)

        context_info_label = ctk.CTkLabel(
            self.scroll_frame, 
            text="420-SF3-RE\nDÉVELOPPEMENT D'APPLICATIONS DANS\nUN ENVIRONNEMENT GRAPHIQUE\ngroupe 02231", 
            font=("arial", 16)
        )
        context_info_label.pack(pady=10)

        due_label = ctk.CTkLabel(
            self.scroll_frame, 
            text="Pour", 
            font=("arial", 16, 'bold')
        )
        due_label.pack(pady=10)

        due_info_label = ctk.CTkLabel(
            self.scroll_frame, 
            text="Ala Antabli\n16 novembre 2026", 
            font=("arial", 16)
        )
        due_info_label.pack(pady=10)

        source_label = ctk.CTkLabel(
            self.scroll_frame, 
            text=". . .\n\nSources bibliographiques & techniques :", 
            font=("arial", 18, 'bold')
        )
        source_label.pack(pady=(15, 10))

        sources_text = (
            "\n• Gouvernement de l'Ontario (Guides et fiches fauniques)\n"
            "  - Guide de pêche : https://files.ontario.ca/environment-and-energy/fishing/198234.pdf\n"
            "  - Grand brochet : https://www.ontario.ca/fr/page/grand-brochet\n"
            "  - Achigan à petite bouche : https://www.ontario.ca/fr/page/achigan-petite-bouche\n"
            "  - Perchaude : https://www.ontario.ca/fr/page/perchaude\n"
            "  - Crapet arlequin : https://www.ontario.ca/fr/page/crapet-arlequin\n"
            "  - Crapet de roche : https://www.ontario.ca/fr/page/crapet-de-roche\n\n"
            "• Gouvernement du Québec (Faune et ressources naturelles)\n"
            "  - Doré jaune : https://www.quebec.ca/agriculture-environnement-et-ressources-naturelles/faune/animaux-sauvages-quebec/fiches-especes-fauniques/dore-jaune\n"
            "  - Crapet-soleil : https://www.quebec.ca/agriculture-environnement-et-ressources-naturelles/faune/animaux-sauvages-quebec/fiches-especes-fauniques/crapet-soleil\n\n"
            "• Gouvernement du Canada (Pêches et Océans)\n"
            "  - Profil du grand brochet : https://www.dfo-mpo.gc.ca/species-especes/profiles-profils/northernpike-grandbrochet-fra.html\n\n"
            "• Fishipedia (Encyclopédie des poissons d'eau douce)\n"
            "  - Poissons de lac : https://www.fishipedia.fr/fr/poissons/biotopes/lac?pg=4\n\n"
            "• Aquareap\n"
            "  - Acapoeta tanganicae : https://aquareap.com/fish/acapoeta-tanganicae\n\n"
            "• Wikipedia\n"
            "  - Catfish : https://en.wikipedia.org/wiki/Catfish\n\n"
            "• Outils de génération & Références de code\n"
            "  - Random Object Generator : https://perchance.org/object\n"
            "  - GeeksforGeeks (Intégration Matplotlib Tkinter) : https://www.geeksforgeeks.org/python/how-to-embed-matplotlib-charts-in-tkinter-gui/"
        )

        sources_name_label = ctk.CTkLabel(
            self.scroll_frame, 
            text=sources_text, 
            font=("arial", 12),
            justify="left",
            wraplength=850
        )
        sources_name_label.pack(pady=10, padx=20)

        

        # Bouton pour revenir au menu principal
        self.back_btn = ctk.CTkButton(self.scroll_frame, text="Retour", command=self.back)
        self.back_btn.pack(pady=20)

    def back(self):
        self.master.show_frame(TitleScreen)




        


class MainApp(ctk.CTk):
    def __init__(self):
        #j'initialise mes attributs et je créer la fenêtre
        super().__init__()
        ctk.set_appearance_mode("Light")

        self.window_width = 1000
        self.window_height = 600
        self.center_window()

        self.title("Fish le poisson")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.user = User()
        self.data = Data(r"assets/fishData.csv")
        
        self.current_frame = None
        self.show_frame(TitleScreen)

    def center_window(self):
        #permet que la fenêtre se trouve exactement au milieu de l'écran

        #taille de l'écran de l'utilisateur
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        #trouver les coordos de la position du centre de l'écran
        x = int((screen_width-self.window_width)/2)
        y = int((screen_height-self.window_height)/2)

        #on créer le fenetre avec les bonnes informations!
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        #afin que ses dimensions restent les memes
        self.resizable(False, False)


    def show_frame(self, frame_class):
        #Méthode pour changer d'écran facilement

        #si l'écran est toujours existant
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(master = self)
        self.current_frame.pack(expand = True, fill = 'both')

    def on_closing(self):
        plt.close('all')
        self.destroy()
        sys.exit(0)


    