#classe de khadija: Data(), Fishing(), savingSystem(), csv files + folder for assetz, stats()
import pandas as pd
import customtkinter as ctk
from PIL import Image  # cest une librairie qui manipule les images png, jpg etc



class Data():
    def __init__(self,file):
        self.file = str(file) #file lien/nom
        self.dataFrame = self.readFile() # cest le dataframe soit le tableau en version pandas

        if self.dataFrame is not None:
            #print(self.dataFrame)
            self.fishEncyclopedia = self.initFishDict() # executer direct apres init + cest un dictionnaire
            self.trash = self.initTrashList() #cest un dictionnaire
            
        
    def readFile(self): #transporter le csv à un dataFrame
        try:
            df = pd.read_csv(self.file, delimiter = ';')
            df = pd.DataFrame(df) #conversion au dataframe/ tableau plus beau
        except Exception as e:
            print(e)
            return None
                    
        return df
    
    def initFishDict(self): # initialiser la liste du poisson item
        fishDict = {}
        for i in range(len(self.dataFrame)):
            if self.dataFrame.at[i,"isFish"] == True: #seulement les poissons
                name = self.dataFrame.iloc[i, 0]
                value = self.dataFrame.iloc[i, 1:].to_dict() # dict dans un dict
                fishDict[name] = value # exemple: poisson rouge : weight: 23 size: 4 etcetc il n ya pas le nom du poisson dans le dict, lmk si cela pose des problemes
                '''
                exemple: poissondict:
                clownfish: 
                {'weight': 23, 'size': 4, 'rarity': 2, 'isFish': True} <- dictionnaire 
                '''
        return fishDict

    def initTrashList(self):
        trashDict = {}
        for i in range(len(self.dataFrame)):
            if self.dataFrame.at[i,"isFish"] == False: #seulement les dechets
                name = self.dataFrame.iloc[i, 0]
                value = self.dataFrame.iloc[i, 1:].to_dict() # dict dans un dict
                trashDict[name] = value 
        return trashDict



    #les getters si jamais
    #aussi si vous voulez des setters lmk!!
    def getFishEncyclopedia(self):
        return self.fishEncyclopedia # retourne un dictionnaire le gros truc
    
    def getTrash(self):
        return self.trash # retourne un dictionnaire le gros truc
    def getFishNameList(self):
        fishNames = [name for name in self.fishEncyclopedia.keys()]
        return fishNames #retourne la liste de tous les noms des poisssons
    def getTrashNameList(self):
        trashNames = [name for name in self.trash.keys()]
        return trashNames #retourne la liste de tous les noms des déchets
    def getAllNamesList(self):
            all = []
            all.extend(self.getTrashNameList())
            all.extend(self.getFishNameList())
            return all # retourne tous les noms des objets
    def getFishAllStatsList(self): #tres specifique:elle prend les stats du dict et les met dans une list exemple de l'affichage list(1,23,hello,1212)
        fishStats = [value for dictio in self.fishEncyclopedia.values() for value in dictio.values()] # rentre dans le premier dict, et puis dans le deuxiemeet extrait les stats du dict 2
        return fishStats # retourne TOUS les valeurs et les mets dans une liste
    def getFishSpecificStatsList(self, name): #tres specifique: au lieu de retourner les valeurs du poisson dans un dict, elle le fait liste style
       valueDict = self.fishEncyclopedia[name] #retourne le dictionnaire des stats du poisson
       fishNameStats = [value for value in valueDict.values()]
       return fishNameStats
    def getFishSpecific(self, name):
        return self.fishEncyclopedia[name] # retourne les stats du poissons (dans un dictionnaire)
    def getTrashSpecific(self,name):
        return self.trash[name] #retourne les stats du dechets dans un dictionnaire
    
        
class SavingSystem():
    def __init__(self, user,file,data):
        
     # à revoir faut mettre tous les attributs to save! (for loading/ pour chaque partie)
        #on save ca pour la premiere fois
        self.inventory = user.getUserInventory()
        self.username = user.getUserName()
        self.level = user.getUserLevel()
        self.playedBefore = False
        self.file = file
        self.user = user
        self.data = data
        
        
        #on a besoin de getters et setters:
        # getters so we can be able to read the info after
    def getInv(self):
        return self.inventory
    def getUsername(self):
        return self.username
    def getLevel(self):
        return self.level
    def getPlayedBefore(self):
        return self.playedBefore
    
        # setters so we can be able to save stuff
    
    def setInv(self,newInventory):
        self.inventory = newInventory
        self.user.setUserInventory(self.inventory)
    def setUsername(self, newUsername):
        self.username = newUsername
        self.user.setUserName(self.username)
    def setLevel(self, newLevel):
        self.level = newLevel
        self.user.setUserLevel(self.level)
    def setPlayedBefore(self,status):
        self.playedBefore = status

    def loadingFromCsv(self, file):
            from classes_Émilie import Catch
            try:
                df = pd.read_csv(file)
            except Exception as e:
                print(e)
                return False

            tempInv = []
            for i in range(len(df)):
                # si c'était une partie avec 0 catch
                if df.loc[i, "Name"] == "None":
                    continue

                catchTemp = Catch(self.data)
                catchTemp.setName(df.loc[i,"Name"])
                catchTemp.setWeight(float(df.loc[i,"Weight"]))
                catchTemp.setSize(float(df.loc[i,"Size"]))
                catchTemp.setIsFish(bool(df.loc[i,"IsFish"]))
                catchTemp.setDescription(df.loc[i,"Description"])
                catchTemp.setRarity(df.loc[i,"Rarity"])
                catchTemp.setTimeFishing(df.loc[i,"TimeFishing"])
                tempInv.append(catchTemp)

            self.inventory = tempInv      
            self.user.setUserInventory(self.inventory)
            
            # met à jour les compteurs de poissons et déchets
            nb_fish = sum(1 for item in tempInv if item.isFish)
            self.user.setUserNbFish(nb_fish)
            self.user.setUserNbTrash(len(tempInv) - nb_fish)
            if hasattr(self.user, 'setUserNbCatch'):
                self.user.setUserNbCatch(len(tempInv))

            #nom et niveau
            if len(df) > 0:
                self.username = str(df.loc[0,"Username"])
                self.level = int(df.loc[0,"Level"])
                self.playedBefore = df.loc[0,"Status"]
                self.user.setUserName(self.username)
                self.user.setUserLevel(self.level)

            return True

    def savingToFile(self):
    # si l'inventaire est vide, ligne placeholder pour garder le nom et le niveau
        if len(self.getInv()) == 0:
            data = {
                "Name" : ["None"],
                "Weight" : [0.0],
                "Size" : [0.0],
                "IsFish" : [False],
                "Description" : ["None"],
                "Rarity" : ["None"],
                "TimeFishing" : [0],
                "Username" : [self.getUsername()],
                "Level" : [self.getLevel()],
                "Status" : [self.getPlayedBefore()]
            }
        else:
            data = {
                "Name" : [i.getName() for i in self.getInv()],
                "Weight" : [i.getWeight() for i in self.getInv()],
                "Size" : [i.getSize() for i in self.getInv()],
                "IsFish" : [i.getIsFish() for i in self.getInv()],
                "Description" : [i.getDescription() for i in self.getInv()],
                "Rarity" : [i.getRarity() for i in self.getInv()],
                "TimeFishing" : [i.getTimeFishing() for i in self.getInv()],
                "Username" : [self.getUsername()] * len(self.getInv()),
                "Level" : [self.getLevel()] * len(self.getInv()),
                "Status" : [self.getPlayedBefore()] * len(self.getInv())
            }

        df = pd.DataFrame(data)
        df.to_csv(self.file, index = False)
        return 'sauvegardement du fichier'
        
class ImageConfig():
    def __init__(self,fileLight,fileDark,x,y):
        
        temp = self.readFile(fileLight,fileDark)
        if temp is not None:
            self.fileLight,self.fileDark = temp
            self.x = x
            self.y = y
            self.myImg = self.createImage()

    def readFile(self,file1, file2): 
        try:
           Image.open(file1)
           Image.open(file2)
        except Exception as e:
            print(e)
            return None
                        
        return file1,file2
    def createImage(self):
        img = ctk.CTkImage(light_image=Image.open(self.fileLight),dark_image=Image.open(self.fileDark),size=(self.x,self.y))
        return img
    def getImage(self):
        return self.myImg

class GifImage(ctk.CTkFrame): #OPTIONELLE A REVOIR ET TESTER SI CA FONCTIONNE
    def __init__(self,master, file, x, y, width, height, wait):
        super().__init__(master)
        if self.checkFile(file) != None:
            self.file = file # cest comme si jai fait au fond self.file= file
            self.x = x
            self.y = y 
            self.width = width
            self.height = height
            self.wait = wait
            self.showAnimation()
        

    def checkFile(self,file): #avant meme de commencer on check si l'image n'a pas de probleme
        try:
            Image.open(file)
        except Exception as e:
            print(e)
            return None
        return file
    
    def showAnimation(self):
        openImg = Image.open(self.file)
        self.showAnim = None
        frames = openImg.n_frames #n_frames indique le nb d'image qui se trouve dans ce gif
        img = []

        for i in range(frames):
            openImg.seek(i)
            img.append(ctk.CTkImage(light_image= openImg.copy(), size=(self.width, self.height)))
        gifLabel = ctk.CTkLabel(self.master, text = "",width = self.width, height = self.height) # on revient avec ctk pour que ca soit compatible
        gifLabel.place(x = self.x, y = self.y) # ou le placer
                 
        def animation(count):
            newImg = img[count] # on commence avec ce frame precis
            gifLabel.configure(image = newImg) # on prend le label et on le transforme en img
            count += 1 # prochaine img

            if count == frames: # si on arrive a la fin
                count = 0 # on reset le compte pour qu'on puisse loop apres
            self.showAnim = self.master.after(self.wait, lambda: animation(count) ) # on attend self.wait de seconde avant de refaire la fonction: de plus lambda fais que la fct ne s'eexecute pas immediatement, et d'attendre jusqu'a ce que la condition soit satisfaite
        animation(0) # on fait demarer lanimation le zero cest le debut soit le count 0

#app = ctk.CTk()
#app.geometry("800x400")
#img1 = ImageConfig("assets/mainMenu.jpeg","assets/mainMenu.jpeg",800,400)
#my_label = ctk.CTkLabel(app, text="", image=img1.getImage())
#my_label.pack(pady=10)
#fishimg = GifImage(app,"assets/ocean.gif",150, 25, 100, 25, 50) # to fix the sizing
#app.mainloop()





#data1 = Data("assets/fishEncylopedia3.csv") #jsp honestly
#print(data1.getFishEncyclopedia())

#le lien du fichier ne fonctionne pas correctement, faut voir cest quoi le probleme avec le fichier
#wshhh