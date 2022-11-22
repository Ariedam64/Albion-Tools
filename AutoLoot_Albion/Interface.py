import tkinter
import tkinter.messagebox
from turtle import width
import customtkinter
import AutoLoot_Albion
import time
import threading
import pyautogui
import pynput.keyboard as kb

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

textboxTempsReel = None
textboxAppuieClic = None
textboxRelacheClic = None


class App(customtkinter.CTk):

    WIDTH = 300
    HEIGHT = 415

    def __init__(self):
        super().__init__()

        self.title("Albion Tools")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.attributes('-toolwindow', True)
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        self.switch_varEnable = customtkinter.StringVar(0)
        self.switch_varEnable.set("off")
        self.switch_varTestMode = customtkinter.StringVar(0)
        self.switch_varTestMode.set("off")
        self.switch_varDetectionAutoConfig = customtkinter.StringVar(0)
        self.switch_varDetectionAutoConfig.set("off")
        self.switch_varDetectionAuto = customtkinter.StringVar(0)
        self.switch_varDetectionAuto.set("off")

        self.textbox_varMouseDown = customtkinter.StringVar(0)
        self.textbox_varMouseDown.set(AutoLoot_Albion.timeMouseDown)
        self.textbox_varMouseDown.trace("w", lambda name, index, mode,sv=self.textbox_varMouseDown: self.updateTheoriqueTime())

        self.textbox_varMouseUp = customtkinter.StringVar(0)
        self.textbox_varMouseUp.set(AutoLoot_Albion.timeMouseUp)
        self.textbox_varMouseUp.trace("w", lambda name, index, mode,sv=self.textbox_varMouseUp: self.updateTheoriqueTime())

        self.textbox_varMousePosition1 = customtkinter.StringVar(0)
        self.textbox_varMousePosition1.set(AutoLoot_Albion.timeDeplacementSouris1)
        self.textbox_varMousePosition1.trace("w", lambda name, index, mode,sv=self.textbox_varMousePosition1: self.updateTheoriqueTime())

        self.textbox_varMousePosition2 = customtkinter.StringVar(0)
        self.textbox_varMousePosition2.set(AutoLoot_Albion.timeDeplacementSouris2)
        self.textbox_varMousePosition2.trace("w", lambda name, index, mode,sv=self.textbox_varMousePosition2: self.updateTheoriqueTime())

        self.textbox_varScrollTime = customtkinter.StringVar(0)
        self.textbox_varScrollTime.set(AutoLoot_Albion.delaiScroll)
        self.textbox_varScrollTime.trace("w", lambda name, index, mode,sv=self.textbox_varScrollTime: self.updateTheoriqueTime())

        self.textbox_varScrollRange = customtkinter.StringVar(0)
        self.textbox_varScrollRange.set(AutoLoot_Albion.DistanceScroll)

        self.textbox_varNbColonne = customtkinter.StringVar(0)
        self.textbox_varNbColonne.set(AutoLoot_Albion.nbColonne)
        self.textbox_varNbColonne.trace("w", lambda name, index, mode,sv=self.textbox_varNbColonne: self.updateTheoriqueTime())

        self.textbox_varNbLigne = customtkinter.StringVar(0)
        self.textbox_varNbLigne.set(AutoLoot_Albion.nbLigne)
        self.textbox_varNbLigne.trace("w", lambda name, index, mode,sv=self.textbox_varNbLigne: self.updateTheoriqueTime())

        self.switch_varCommencement = "le debut"

        self.radio_varMode = customtkinter.IntVar(0)

        self.label_mode = customtkinter.CTkLabel(master=self, text="AutoLoot by Ariedam v1.0",
                                                                text_font=('Times, 16'),
                                                                width = 120,
                                                                text_color="#11B384")
        self.label_mode.grid(row=1, column=0, pady=10, padx=30, sticky = "w")

        self.switch_enable = customtkinter.CTkSwitch(master=self,
                                                text="Inactif",
                                                command=self.switch_eventEnable,
                                                variable=self.switch_varEnable,
                                                onvalue="on", 
                                                offvalue="off")
        self.switch_enable.grid(row=2, column=0, pady=10, padx=30, sticky="w")

        self.switch_testMode = customtkinter.CTkSwitch(master=self,
                                                text="ConfigMode",
                                                state="disabled",
                                                command=self.switch_eventTestMode,
                                                variable=self.switch_varTestMode,
                                                onvalue="on", 
                                                offvalue="off")
        self.switch_testMode.grid(row=2, column=0, pady=10, padx=160, sticky="w")

        self.label_skip = customtkinter.CTkLabel(master=self, text="______________________________",
                                                                text_font=('Times, 12'),
                                                                text_color="#11B384",
                                                                state="disabled")
        self.label_skip.grid(row=3, column=0, padx=12, sticky="w")

        #########################################################################################################################

        self.label_Multiplier = customtkinter.CTkLabel(master=self, text="Multiplicateur clic : x1",
                                                                text_font=('Times, 10'),
                                                                state="disabled")
        self.label_Multiplier.grid(row=4, column=0,columnspan=1, padx=62, sticky="w")

        self.multiplier = customtkinter.CTkSlider(master=self,
                                                    from_=1.5,
                                                    to=0.5,
                                                    number_of_steps=100,
                                                    command=self.slider_eventMultiplier,
                                                    state="disabled")
        self.multiplier.grid(row=5, column=0, padx=50, sticky="w")

        self.multiplier.set(1)

        self.label_skip2 = customtkinter.CTkLabel(master=self, text="______________________________",
                                                                text_font=('Times, 12'),
                                                                text_color="#11B384",
                                                                state="disabled")
        self.label_skip2.grid(row=6, column=0, padx=12, sticky="w")

        #########################################################################################################################

        self.label_LootingMode = customtkinter.CTkLabel(master=self, text="Detection de looting :",
                                                                text_font=('Times, 11'),
                                                                state="disabled")
        self.label_LootingMode.grid(row=7, column=0,columnspan=2, padx=20, sticky="w")

        self.radiobutton_1 = customtkinter.CTkRadioButton(master=self, text="Automatique",
                                                variable= self.radio_varMode, value=1, state="disabled")
        self.radiobutton_1.grid(row=8, column=0,columnspan=2,pady=5, padx=20, sticky="w")

        self.radiobutton_2 = customtkinter.CTkRadioButton(master=self, text="Touche du clavier enfoncee",
                                                   variable= self.radio_varMode, value=2, state="disabled")
        self.radiobutton_2.grid(row=9, column=0,columnspan=2,pady=5, padx=20, sticky="w")

        self.radio_varMode.set(2)

        self.labelCommencement = customtkinter.CTkLabel(master=self, text="Commencer a loot par : ",
                                                                text_font=('Times, 11'),
                                                                state="disabled")
        self.labelCommencement.grid(row=10, column=0,pady=5,padx=20, sticky = "w")

        self.comboboxCommencement = customtkinter.CTkOptionMenu(master=self,
                                       values=["le debut", "la fin"],
                                       command=self.optionmenu_callback,
                                       state="disabled")
        self.comboboxCommencement.grid(row=11, column=0, padx=80, sticky = "w")
        self.comboboxCommencement.set("le debut")

        self.label_skip3 = customtkinter.CTkLabel(master=self, text="______________________________",
                                                                text_font=('Times, 12'),
                                                                text_color="#11B384",
                                                                state="disabled")
        self.label_skip3.grid(row=12, column=0, padx=12, sticky ="w")

        #########################################################################################################################

        self.switch_DetectionAutoItem = customtkinter.CTkSwitch(master=self,
                                                text="Recuperer que les items visibles",
                                                state="disabled",
                                                variable=self.switch_varDetectionAuto,
                                                onvalue="on", 
                                                offvalue="off")
        self.switch_DetectionAutoItem.grid(row=13, column=0,pady=10, padx=20, sticky="w")

    def frame_TestMode(self):
        self.window = customtkinter.CTkToplevel(self)
        self.window.geometry("360x700")
        self.window.title("Config Mode")
        self.window.attributes('-toolwindow', True)
        self.window.maxsize(360,700)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closingConfig)  # call .on_closing() when app gets closed

        self.label_MultiplierConfig = customtkinter.CTkLabel(master=self.window, text="Multiplicateur vitesse : x1",
                                                                text_font=('Times, 11'))
        self.label_MultiplierConfig.grid(row=0, column=0,columnspan=1, padx=88,pady=10, sticky="w")

        self.multiplierConfig = customtkinter.CTkSlider(master=self.window,
                                                    from_=1.5,
                                                    to=0.5,
                                                    number_of_steps=100,
                                                    width=300,
                                                    command=self.slider_eventMultiplierConfig)
        self.multiplierConfig.grid(row=1, column=0, padx=28, sticky="w")

        self.multiplierConfig.set(1)

        self.label_skipConfig1 = customtkinter.CTkLabel(master=self.window, text="________Souris________________________",
                                                            text_font=('Times, 12'),
                                                            text_color="#11B384")
        self.label_skipConfig1.grid(row=2, column=0, padx=13, pady=10, sticky ="w")

        self.textboxAppuieClic = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varMouseDown,
                                           validate="key",
                                           validatecommand=(self.register(self.validateFloat), '%P'),
                                           height=15)
        self.textboxAppuieClic.grid(row=3, column=0, padx= 10, sticky="ws")


        self.labelAppuieClic = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Appuie clic gauche")
        self.labelAppuieClic.grid(row=3, column=0,padx=70, sticky="w")

        self.textboxRelacheClic = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varMouseUp,
                                           validate="key",
                                           validatecommand=(self.register(self.validateFloat), '%P'),
                                           height=15)
        self.textboxRelacheClic.grid(row=4, column=0, padx= 10, pady=10, sticky="w")


        self.labelRelacheClic = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Relache clic gauche")
        self.labelRelacheClic.grid(row=4, column=0, pady=10,padx=70, sticky="w")

        self.textboxDeplacementSouris = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varMousePosition1,
                                           validate="key",
                                           validatecommand=(self.register(self.validateFloat), '%P'),
                                           height=15)
        self.textboxDeplacementSouris.grid(row=5, column=0,padx=10, sticky="w")


        self.labelDeplacementSourisTiret = customtkinter.CTkLabel(self.window,
                                                 text="-",
                                                 width=10,
                                                 height=10)
        self.labelDeplacementSourisTiret.grid(row=5, column=0,padx=62,sticky="w")

        self.textboxDeplacementSouris2 = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varMousePosition2,
                                           validate="key",
                                           validatecommand=(self.register(self.validateFloat), '%P'),
                                           height=15)
        self.textboxDeplacementSouris2.grid(row=5, column=0,padx=75, sticky="w")

        self.labelDeplacementSouris2 = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Valeur aleatoire deplacement souris")
        self.labelDeplacementSouris2.grid(row=5, column=0,padx=135, sticky="w")

        self.textboxDelaiScroll = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varScrollTime,
                                           validate="key",
                                           validatecommand=(self.register(self.validateFloat), '%P'),
                                           height=15)
        self.textboxDelaiScroll.grid(row=6, column=0, padx= 10, pady=10, sticky="w")


        self.labelDelaiScroll = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Delai scroll")
        self.labelDelaiScroll.grid(row=6, column=0, pady=10,padx=63, sticky="w")

        self.textboxDistanceScroll = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varScrollRange,
                                           validate="key",
                                           validatecommand=(self.register(self.validateFloat), '%P'),
                                           height=15)
        self.textboxDistanceScroll.grid(row=7, column=0, padx= 10, sticky="w")


        self.labelDistanceScroll = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Distance scroll")
        self.labelDistanceScroll.grid(row=7, column=0,padx=70, sticky="w")

        self.label_skipConfig2 = customtkinter.CTkLabel(master=self.window, text="________Position items__________________",
                                                            text_font=('Times, 12'),
                                                            text_color="#11B384")
        self.label_skipConfig2.grid(row=8, column=0, padx=12,pady=10, sticky ="w")


        self.textboxColonne = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varNbColonne,
                                           validate="key",
                                           validatecommand=(self.register(self.validateInt), '%P'),
                                           height=15)
        self.textboxColonne.grid(row=9, column=0,padx=10, pady=15, sticky="w")


        self.labelTableauTiret = customtkinter.CTkLabel(self.window,
                                                 text="x",
                                                 width=10,
                                                 height=10)
        self.labelTableauTiret.grid(row=9, column=0, pady=15,padx=62,sticky="w")

        self.textboxLigne = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           textvariable=self.textbox_varNbLigne,
                                           validate="key",
                                           validatecommand=(self.register(self.validateInt), '%P'),
                                           height=15)
        self.textboxLigne.grid(row=9, column=0, pady=15,padx=75, sticky="w")


        self.labelTableau = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Tableau Colonne x Ligne")
        self.labelTableau.grid(row=9, column=0,padx=135, pady=15, sticky = "w")


        self.textbox_X = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           validate="key",
                                           validatecommand=(self.register(self.validateInt), '%P'),
                                           height=15)
        self.textbox_X.grid(row=10, column=0,padx=10, sticky="w")

        self.textbox_X.insert(0, str(AutoLoot_Albion.coord_XTest))

        self.labelCoord = customtkinter.CTkLabel(self.window,
                                                 text="x",
                                                 width=10,
                                                 height=10)
        self.labelCoord.grid(row=10, column=0,padx=62,sticky="w")

        self.textbox_Y = customtkinter.CTkEntry(self.window,
                                           width=50,
                                           validate="key",
                                           validatecommand=(self.register(self.validateInt), '%P'),
                                           height=15)
        self.textbox_Y.grid(row=10, column=0,padx=75, sticky="w")

        self.textbox_Y.insert(0, str(AutoLoot_Albion.coord_YTest))

        self.labelTousCoord = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Coordonnees premier item")
        self.labelTousCoord.grid(row=10, column=0,padx=135, sticky = "w")
       

        self.label_skipConfig4 = customtkinter.CTkLabel(master=self.window, text="________Options_______________________",
                                                            text_font=('Times, 12'),
                                                            text_color="#11B384")
        self.label_skipConfig4.grid(row=11, column=0, padx=12,pady=10, sticky ="w")

        self.labelCommencementConfig = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Loot par ")
        self.labelCommencementConfig.grid(row=12, column=0, sticky="w")

        self.comboboxCommencementConfig = customtkinter.CTkOptionMenu(master=self.window,
                                       values=["le debut", "la fin"],
                                       command=self.optionmenu_callbackConfig)
        self.comboboxCommencementConfig.grid(row=12, column=0, padx=70,pady=15, sticky = "w")
        self.comboboxCommencementConfig.set("le debut")

        self.switch_DetectionAutoItemConfig = customtkinter.CTkSwitch(master=self.window,
                                                text="Recuperer uniquement les items visibles",
                                                command=self.updateTheoriqueTime,
                                                variable=self.switch_varDetectionAutoConfig,
                                                onvalue="on", 
                                                offvalue="off")
        self.switch_DetectionAutoItemConfig.grid(row=13, column=0,padx=15, sticky="w")
    

        self.label_skipConfig4 = customtkinter.CTkLabel(master=self.window, text="________Calculs_______________________",
                                                            text_font=('Times, 12'),
                                                            text_color="#11B384")
        self.label_skipConfig4.grid(row=14, column=0, padx=12,pady=10, sticky ="w")



        self.labelTempsTheorique = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Temps theorique: ")
        self.labelTempsTheorique.grid(row=15, column=0,padx=14, pady=10, sticky = "w")

        self.textboxTempsTheorique = customtkinter.CTkEntry(self.window,
                                           width=80,
                                           height=15)
        self.textboxTempsTheorique.grid(row=15, column=0, pady=10,padx=120, sticky="w")

        self.textboxTempsTheorique.insert(0, str(self.calculTheoriqueTime()) + "s")
        self.textboxTempsTheorique.configure(state="disabled")

        self.labelTempsReel = customtkinter.CTkLabel(self.window,
                                                 width=80,
                                                 height=10,
                                                 text="Temps reel: ")
        self.labelTempsReel.grid(row=16, column=0,padx=10, sticky = "w")

        self.textboxTempsReel = customtkinter.CTkEntry(self.window,
                                           width=70,
                                           height=15)
        self.textboxTempsReel.grid(row=16, column=0,padx=90, sticky="w")

        self.textboxTempsReel.insert(0, "Touche K")
        self.textboxTempsReel.configure(state="disabled")

        self.label_skipConfig4 = customtkinter.CTkLabel(master=self.window, text="_________________",
                                                            text_font=('Times, 12'),
                                                            text_color="#11B384")
        self.label_skipConfig4.grid(row=17, column=0, padx=100, sticky ="w")

        self.SaveButton = customtkinter.CTkButton(master=self.window,
                                                  width=310,
                                                  height= 32,
                                                  corner_radius=5,
                                                  text="Sauvegarder la configuration",
                                                  command=self.saveConfig)

        self.SaveButton.grid(row=18, column=0,padx=20,pady=10, sticky="w")

    def validateFloat(self, value):
        try:
            myFloat = float(value)
            return True
        except:
            return False

    def validateInt(self, value):
        try:
            myFloat = int(value)
            return True
        except:
            return False
        
    def updateTheoriqueTime(self):
        self.textboxTempsTheorique.configure(state="normal")
        self.textboxTempsTheorique.delete(0, tkinter.END)
        self.textboxTempsTheorique.insert(0, str(self.calculTheoriqueTime()) + "s")
        self.textboxTempsTheorique.configure(state="disabled")

    def switch_eventEnable(self):
        if self.switch_varEnable.get() == "on":
            self.switch_enable.configure(text="Actif")
            self.enableAll()
            self.switch_varTestMode.set("off")
            threading.Thread(target=self.startLooting).start()
        else:
            self.switch_enable.configure(text="Inactif")
            self.disableAll()

    def switch_eventTestMode(self):
        if self.switch_varTestMode.get() == "on":
            self.label_Multiplier.configure(state="disabled")
            self.multiplier.configure(state="disabled")
            self.frame_TestMode()
            threading.Thread(target=self.startKeyboardListener).start()
            self.disableAll()
            self.switch_enable.configure(state="disabled")
        else:
            self.label_Multiplier.configure(state="normal")
            self.multiplier.configure(state="normal")

    def optionmenu_callback(self, choice):
        self.switch_varCommencement = choice

    def optionmenu_callbackConfig(self, choice):
        print("appuyer")

    def slider_eventMultiplier(self,value):
        AutoLoot_Albion.multiplier = value
        self.label_Multiplier.configure(text="Multiplicateur vitesse clic : x" + str("{0:.2f}".format(value)))

    def slider_eventMultiplierConfig(self,value):
        AutoLoot_Albion.multiplier = value
        self.multiplier.set(value)
        self.label_MultiplierConfig.configure(text="Multiplicateur vitesse clic : x" + str("{0:.2f}".format(value)))
        self.label_Multiplier.configure(text="Multiplicateur vitesse clic : x" + str("{0:.2f}".format(value)))
        self.textboxTempsTheorique.configure(state="normal")
        self.textboxTempsTheorique.delete(0, tkinter.END)
        self.textboxTempsTheorique.insert(0, str(self.calculTheoriqueTime()) + "s")
        self.textboxTempsTheorique.configure(state="disabled")

    def enableAll(self):
        self.switch_testMode.configure(state="normal")
        self.label_skip.configure(state="normal")
        self.comboboxCommencement.configure(state="normal")
        self.labelCommencement.configure(state="normal")
        self.label_Multiplier.configure(state="normal")
        self.multiplier.configure(state="normal")
        self.label_skip2.configure(state="normal")
        self.label_LootingMode.configure(state="normal")
        self.radiobutton_1.configure(state="normal")
        self.radiobutton_2.configure(state="normal")
        self.label_skip3.configure(state="normal")
        self.switch_DetectionAutoItem.configure(state="normal")

    def disableAll(self):
        self.switch_testMode.configure(state="disabled")
        self.label_skip.configure(state="disabled")
        self.comboboxCommencement.configure(state="disabled")
        self.labelCommencement.configure(state="disabled")
        self.label_Multiplier.configure(state="disabled")
        self.multiplier.configure(state="disabled")
        self.label_skip2.configure(state="disabled")
        self.label_LootingMode.configure(state="disabled")
        self.radiobutton_1.configure(state="disabled")
        self.radiobutton_2.configure(state="disabled")
        self.label_skip3.configure(state="disabled")
        self.switch_DetectionAutoItem.configure(state="disabled")

    def on_closing(self, event=0):
        self.destroy()

    def on_closingConfig(self, event=0):
        self.window.destroy()
        self.enableAll()
        self.switch_testMode.deselect()
        self.switch_enable.configure(state="normal")
        

    def startKeyboardListener(self):
        with kb.Listener(on_press=self.checkAutolootKeyStartTest) as listener:
            listener.join()

    def checkAutolootKeyStartTest(self,key):
        if self.switch_varTestMode.get() == "on":
            if 'char' in dir(key):
                if key.char == "k" or key.char == "K":
                    AutoLoot_Albion.nbColonne = self.textboxColonne.get()
                    AutoLoot_Albion.nbLigne = self.textboxLigne.get()
                    self.textboxTempsTheorique.configure(state="normal")
                    self.textboxTempsTheorique.delete(0, tkinter.END)
                    self.textboxTempsTheorique.insert(0, str(self.calculTheoriqueTime()) + "s")
                    self.textboxTempsTheorique.configure(state="disabled")
                    self.textboxTempsReel.configure(state="normal")
                    self.textboxTempsReel.delete(0, tkinter.END)
                    self.textboxTempsReel.insert(0, "En cours...")
                    self.textboxTempsReel.configure(state="disabled")
                    AutoLoot_Albion.configCollectItems(self.textbox_X.get(),self.textbox_Y.get(), self.textboxColonne.get(),self.textboxLigne.get(),self.textboxDeplacementSouris.get(),self.textboxDeplacementSouris2.get(),self.textboxAppuieClic.get(),self.textboxRelacheClic.get(),self.textboxDelaiScroll.get(),self.textboxDistanceScroll.get(),self.switch_varDetectionAuto.get(),None)
                    self.textboxTempsReel.configure(state="normal")
                    self.textboxTempsReel.delete(0, tkinter.END)
                    self.textboxTempsReel.insert(0, AutoLoot_Albion.tempsTotal + "s")
                    self.textboxTempsReel.configure(state="disabled")


    def calculTheoriqueTime(self):
        MousePosition1 = ((float(self.textboxDeplacementSouris.get()) *AutoLoot_Albion.multiplier) * (int(AutoLoot_Albion.nbLigne)*int(AutoLoot_Albion.nbColonne)))
        MousePosition2 = ((float(self.textboxDeplacementSouris2.get())*AutoLoot_Albion.multiplier) * (int(AutoLoot_Albion.nbLigne)*int(AutoLoot_Albion.nbColonne)))
        TotalPositionTime = MousePosition1 + MousePosition2 / 2
        MouseDownTime = (float(self.textboxAppuieClic.get()) * AutoLoot_Albion.multiplier) * (int(AutoLoot_Albion.nbLigne)*int(AutoLoot_Albion.nbColonne))
        MouseUpTime = (float(self.textboxRelacheClic.get()) * AutoLoot_Albion.multiplier) * (int(AutoLoot_Albion.nbLigne)*int(AutoLoot_Albion.nbColonne))
        ScrollDelai = (float(self.textboxDelaiScroll.get()) * AutoLoot_Albion.multiplier)
        if self.switch_varDetectionAuto.get() == "on":
            DetectItemDelai = 0.050 * (int(AutoLoot_Albion.nbColonne) * int(AutoLoot_Albion.nbLigne))
        else:
            DetectItemDelai = 0


        return "{0:.2f}".format((TotalPositionTime + MouseDownTime + MouseUpTime + ScrollDelai + DetectItemDelai)*0.95)

    def saveConfig(self):
        self.comboboxCommencement.set(self.comboboxCommencementConfig.get())
        self.switch_varDetectionAuto.set(self.switch_varDetectionAutoConfig.get())
        AutoLoot_Albion.coord_XTest = self.textbox_X.get()
        AutoLoot_Albion.coord_YTest = self.textbox_Y.get()
        AutoLoot_Albion.nbColonne = self.textboxColonne.get()
        AutoLoot_Albion.nbLigne = self.textboxLigne.get()
        AutoLoot_Albion.timeDeplacementSouris1 = self.textboxDeplacementSouris.get()
        AutoLoot_Albion.timeDeplacementSouris2 = self.textboxDeplacementSouris2.get()
        AutoLoot_Albion.timeMouseDown = self.textboxAppuieClic.get()
        AutoLoot_Albion.timeMouseUp = self.textboxRelacheClic.get()
        AutoLoot_Albion.delaiScroll = self.textboxDelaiScroll.get()
        AutoLoot_Albion.DistanceScroll = self.textboxDistanceScroll.get()
        self.window.destroy()
        self.enableAll()
        self.switch_enable.configure(state="normal")
        self.switch_testMode.deselect()
        

    def startLooting(self):
         while True:
            if self.switch_varEnable.get() == "on":
                if self.switch_varTestMode.get() == "off":
                    if self.radio_varMode.get() == 1: #Detection automatique
                        if pyautogui.locateOnScreen(AutoLoot_Albion.openInventaire, region=(1140,250,9,15), grayscale=True) != None:
                           AutoLoot_Albion.collectItemsAuto()
                           print("trouve")
                    else: #Detection par touche enfoncee
                        if AutoLoot_Albion.estActif:
                            AutoLoot_Albion.collectItems()             
            else:
                break
            time.sleep(0.1)


        
