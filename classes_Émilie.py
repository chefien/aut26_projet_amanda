'''Classes par Émilie'''


import customtkinter as ctk
import random
import time


class User():
    '''Joueur et ses informations'''

    def __init__(self):

        #initialement None, on demandera le nom par la suite
        self.name = None

        #augmentera selon le nombre de poissons attrappés
        self.level = 0

        #contiendra tout ce qui sera attrappé
        self.inventory = []
        self.total_inventory = []

        #argent du joueur
        self.money = 0

        #seront mis à jour lors de chaque prise
        self.nbFish = 0
        self.nbTrash = 0
        self.nbCatch = 0

        #upgrades du magasin
        self.bonus_time = 0.0
        self.sell_mult = 1
        self.click_mult = 1

        self.purchased_upgrades = []



    #setters
    #après avoir demander le nom
    def setUserName(self, name):
        self.name = name

    def setUserLevel(self, level):
        self.level = level

    def setUserInventory(self, inventory):
        self.inventory = inventory
    def setUserTotalInventory(self, inventory):
        self.total_inventory = inventory

    def setUserNbFish(self, nbFish):
        self.nbFish = nbFish

    def setUserNbTrash(self, nbTrash):
        self.nbTrash = nbTrash

    def setUserNbCatch(self, nbCatch):
            self.nbCatch = nbCatch
            
    def setUserMoney(self,earnings):
        self.money= int(earnings)


    #getters
    def getUserName(self):
        return self.name

    def getUserLevel(self):
        return self.level

    def getUserInventory(self):
        return self.inventory
    
    def getUserTotalInventory(self):
        return self.total_inventory

    def getUserNbFish(self):
        return self.nbFish

    def getUserNbTrash(self):
        return self.nbTrash

    def getUserNbCatch(self):
        return self.nbCatch
    
    def getUserMoney(self):
        return self.money

    def getBonusTime(self):
        return self.bonus_time
    def setBonusTime(self, bonus_time):
        self.bonus_time = bonus_time

    def getSellMult(self):
        return self.sell_mult
    def setSellMult(self, sell_mult):
        self.sell_mult = sell_mult

    def getClickMult(self):
        return self.click_mult
    def setClickMult(self, click_mult):
        self.click_mult = click_mult

    def getPurchasedUpgrades(self):
        return self.purchased_upgrades
    
    def setPurchasedUpgrades(self, purchased_upgrades):
        self.purchased_upgrades = purchased_upgrades

    def addUserMoney(self, amount):
        new_total = int(self.getUserMoney()+amount)
        self.setUserMoney(new_total)


    #met à jour l'inventaire, le total de poissons, de déchets et les deux ensemble
    def updateInventory(self, catch):
        self.total_inventory.append(catch)
        self.nbCatch += 1

        self.inventory.append(catch)

        if catch.isFish:
            self.nbFish += 1
        else:
            self.nbTrash += 1


    #met à jour le niveau avec une condition
    #si la condition est remplie on change le niveau et on retourne vrai, sinon on retourne faux 
    def isLeveledUp(self):
        leveled_up = False
        while self.nbFish >= max(1, self.level + (sum(range(1, self.level + 1))) * 2):
            self.level += 1
            leveled_up = True
        return leveled_up




class Catch():
    '''Poisson ou déchet possible de pêcher'''

    #doit être créé avant la pêche car le temps d'attente, le temps de pêche et le nombre de clics pour la pêche sont fait ici
    def __init__(self, data):

        #on choisit la rareté du catch, et ensuite on choisis le catch ayant la meme rareté
        rarity = random.choices(data.getRarityList(), weights=data.getRarityWeights())[0]
        catchs_with_rarity = data.dataFrame[data.dataFrame['rarity']==rarity]['name'].tolist()

        self.name = random.choice(catchs_with_rarity)

        # pour les poissons
        if self.name in data.getFishNameList():
            info = data.getFishSpecific(self.name)
            self.isFish = True
        # pour les déchets
        else:
            info = data.getTrashSpecific(self.name)
            self.isFish = False

        self.weight = round(random.uniform(float(info["startWeight"]), float(info["finishWeight"])), 3)
        self.size = round(random.uniform(float(info["startSize"]), float(info["finishSize"])), 3)
        self.isSold = False
        self.description = info["description"]
        self.rarity = str(info["rarity"]).strip().lower()

        # temps maximal pour atteindre le nombre de clics requis (en sec)
        self.timeFishing = 10

        # temps d'attente et nombre de clics chargés depuis rarities.csv
        if self.rarity in data.rarities:
            self.timeWaiting = data.getRarityTimeWaiting(self.rarity)
            self.clicks = data.getRarityClicks(self.rarity)
        else:
            self.timeWaiting = 0
            self.clicks = 0


    #setters
    def setName(self, name):
        self.name = name

    def setWeight(self, weight):
        self.weight = weight

    def setSize(self, size):
        self.size = size

    def setIsFish(self, isFish):
        self.isFish = isFish

    def setIsSold (self, isSold):
        self.isSold = isSold

    def setDescription(self, description):
        self.description = description

    def setRarity(self, rarity):
        self.rarity = rarity

    def setTimeWaiting(self, timeWaiting):
        self.timeWaiting = timeWaiting

    def setTimeFishing(self, timeFishing):
        self.timeFishing = timeFishing

    def setNbClicks(self, nbClicks):
        self.clicks = nbClicks


        
    #getters
    def getName(self):
        return self.name
    
    def getWeight(self):
        return self.weight
    
    def getSize(self):
        return self.size
    
    def getIsFish(self):
        return self.isFish

    def getIsSold(self):
        return self.isSold
    
    def getDescription(self):
        return self.description
    
    def getRarity(self):
        return self.rarity
    
    def getTimeWaiting(self):
        return self.timeWaiting

    def getTimeFishing(self):
        return self.timeFishing

    def getNbClicks(self):
        return self.clicks







class Timer(): 
    '''Compte-à-rebours'''

    def __init__(self, master, seconds):

        #temps inital du timer
        self.seconds = int(seconds)
        self.milliseconds = int((seconds-self.seconds)*100)

        #servira principalement à savoir si le timer a déjà été détruit (autoDestruct)
        self.isFinished = False

        #l'application elle-même pour le label
        self.master = master

        #le visuel du compte-à-rebours, ne sera pas afficher pour le timer sans affichage
        self.label = ctk.CTkLabel(self.master, text=f"{self.seconds:02d}.{self.milliseconds:02d} sec", font=("Arial", 15, "bold"), text_color="#B10E0E")
        self.label.pack(side="right", padx=10)

        #correspond au moment où le timer sera considéré comme terminé
        self.end = time.time() + self.seconds

        #afin de pouvoir annuler le after
        self.after_id = None


    #timer avec affichage du compte-à-rebours
    def updateTimerWithPrint(self):
        currentTime = time.time()

        #si la légende n'a pas encore été détruit (autoDestruct) et on n'est pas encore rendu à la fin
        if not self.isFinished and currentTime < self.end:

            #mettre à jour le temps restant avant la fin du compte-à-rebours
            timeLeft = self.end - currentTime

            #séparer les secondes et les millisecondes
            secondsLeft = int(timeLeft)

            #prendre la partie après la virgule et on la multiplie par 100 car on l'utilise comme un entier
            millisecondsLeft = int((timeLeft - secondsLeft) * 100)

            #mettre à jour la légende (le 02d c'est pour 2 décimales)
            self.label.configure(text=f"{secondsLeft:02d}.{millisecondsLeft:02d} sec")
                                
            #rafraîchir toutes les 10 ms pour que le défilement soit fluide
            self.after_id = self.master.after(10, self.updateTimerWithPrint)
            

        #si c'est terminé
        else:
            if self.label is not None and self.label.winfo_exists():
                self.label.configure(text="00.00 sec")
            self.isFinished = True
            self.after_id = self.master.after(3000, self.autoDestruct)

            


    #getter pour savoir si le compte-à-rebours est terminé
    def getIsFinished(self):
        return self.isFinished

    #détruit la légende
    def autoDestruct(self):
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        if self.label is not None and self.label.winfo_exists():
            self.label.destroy()

    #met la légende à 00 si la légende a déjà été créé et qu'il existe encore
    def stop(self):
        self.isFinished = True
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        if self.label is not None and self.label.winfo_exists():
            self.label.configure(text="00.00 sec")
            self.after_id = self.master.after(3000, self.autoDestruct)

