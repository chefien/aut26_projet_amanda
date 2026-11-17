##L’ajout d’un magasin

import customtkinter as ctk

class shopFrame(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master, fg_color="#9fb498", corner_radius=10)
        self.master = master

    def shopScreen(self):
            return self