from tkinter import *
from tkinter import messagebox
from Edit import encryption
from functools import partial
from turtle import *
import random
from sys import exit
from string import ascii_lowercase

global bgColor
bgColor = "#E8F4FF" #colour used for all label and application backgrounds
global password
password = "wordgames" #password used for the editing of words

class Player:
    __score = 0
    __name = ""

    def __init__(self, newName):
        self.setName(newName)
    def getName(self):
        return self.__name
    def setName(self, newName):
        self.__name = newName
    def getScore(self):
        return self.__score
    def addScore(self, newScore):
        self.__score += newScore

class PlayerName:
    def __init__(self, master):
        self.master = master
        self.master.title("Word Games: Enter your name!")
        self.master.geometry("400x180")
        self.master.configure(background=bgColor)
        self.master.resizable(width=FALSE, height=FALSE)

        nameLabel = Label(self.master, text = "Please enter your name!", font=("Helvetica", 16), justify=CENTER, background= bgColor)
        nameLabel.pack()
        nameLabel.place(x= 20, y= 20, height = 40, width = 360)

        self.nameBox = Entry(self.master, font=("Helvetica", 20))
        self.nameBox.pack()
        self.nameBox.place(x=20, y=60, height = 40, width = 360)
        self.nameBox.focus_set()

        nameSubmit = Button(self.master, text="Submit", command = lambda: self.createPlayer(self.nameBox.get()))
        nameSubmit.pack()
        nameSubmit.place(x = 150, y= 120, width = 100, height = 40)

    def createPlayer(self, name):
        if name.strip() == "":
            root = Tk()
            root.withdraw()
            messagebox.showwarning("You didn't input your name!", "Field was left blank. Please input your name")
            self.nameBox.delete(0, END)
            root.destroy()
        else:
            global player
            player = Player(name)
            self.master.destroy()
            self.master.quit()

class Menu:
    def __init__(self, master):
        self.master = master
        self.master.title("Word Games")
        self.master.geometry("500x500")
        self.master.resizable(width=FALSE, height=FALSE)
        self.master.configure(background=bgColor)

        playerLabel = Label(self.master, text = "Player: %s" % player.getName(), font=("Helvetica", 12), background=bgColor)
        playerLabel.pack()
        playerLabel.place(x = 20, y= 470, height = 20, width = 140)

        scoreLabel = Label(self.master, text = "Score: %i" % player.getScore(), font=("Helvetica", 12), background=bgColor)
        scoreLabel.pack()
        scoreLabel.place(x = 180, y= 470, height = 20, width = 100)

        menuTitle = Label(self.master, text = "WORD\nGAMES!", font=("Helvetica", 40), background=bgColor)
        menuTitle.pack()
        menuTitle.place(x = 100, y = 60, width =300, height = 120)

        #Conundrum button, opens Conundrum
        conundrum = Button(self.master, text="Conundrum", command=self.openConundrum)
        conundrum.pack()
        conundrum.place(x = 200, y = 240, height=40, width=100)

        #Hangman button, opens Hangman
        hangman = Button(self.master, text="Hangman", command=self.openHangman)
        hangman.pack()
        hangman.place(x = 200, y = 300, height=40, width=100)

        #Edit button, allows the user to add their own words or topics to the game
        edit = Button(self.master, text="Edit words", fg="blue", command=self.editWords)
        edit.pack()
        edit.place(x = 200, y = 360, height=40, width=100)

        #Quit button, destroys the window and exits the game when pressed
        quit = Button(self.master, text="Quit", fg="red", command=self.exit)
        quit.pack()
        quit.place(x = 200, y = 420, height=40, width=100)

    def editWords(self):
        root = Tk()
        editmenu = EditMenu(root)
        root.mainloop()

    def exit(self):
        self.master.destroy()
        self.master.quit()

    def openConundrum(self):
        root = Tk()
        global conundrumGame
        conundrumGame = ConundrumGame(root)
        root.mainloop()

    def openHangman(self):
        root = Tk()
        global hangmanGame
        hangmanGame = HangmanGame(root)
        root.mainloop()

class Game:
    _difficulty = ""
    _topic=""
    _wordLength = 0
    _timeLimit = 0
    _topics = ""
    _word = ""
    _guess = ""

    def cancel(self):
        try:
            self.root.destroy()
        except AttributeError:
            pass
        try:
            hangman.root.destroy()
        except TclError:
            pass
        except NameError:
            pass
        except AttributeError:
            pass
        root = Tk()
        global menu
        menu = Menu(root)
        self.master.destroy()
        self.master.quit()

    def difficultyMenu(self, topic):
        self.difficultyMenuLabel = Label(self.master, text = "Select a difficulty!", font=("Helvetica", 20), background=bgColor)
        self.difficultyMenuLabel.pack()
        self.difficultyMenuLabel.place(x = 275, y = 100, height = 40, width= 250)

        self.easyButton = Button(self.master, text = "Easy (Up to 5 letters)", command=lambda: self.difficultyChosen(1, topic))
        self.easyButton.pack()
        self.easyButton.place(x = 325, y = 160, height = 40, width = 150)

        self.mediumButton = Button(self.master, text = "Medium (Up to 8 letters)", command=lambda: self.difficultyChosen(2, topic))
        self.mediumButton.pack()
        self.mediumButton.place(x = 325, y = 220, height = 40, width = 150)

        self.hardButton = Button(self.master, text = "Hard (Over 8 letters)", command=lambda: self.difficultyChosen(3, topic))
        self.hardButton.pack()
        self.hardButton.place(x = 325, y = 280, height = 40, width = 150)

        self.back = Button(self.master, text = "Back", command=lambda: self.difficultyChosen(-1,topic))
        self.back.pack()
        self.back.place(x = 325, y=340, height = 40, width = 60)

    def difficultyChosen(self, diff, topic):
        self.difficultyMenuLabel.destroy()
        self.easyButton.destroy()
        self.mediumButton.destroy()
        self.hardButton.destroy()
        self.back.destroy()
        if diff == -1:
            self.topicMenu()
        else:
            if diff == 1:
                self._difficulty = "Easy"
                self._wordLength = 6
                self._timeLimit = 15
            elif diff ==2:
                self._difficulty = "Medium"
                self._wordLength = 9
                self._timeLimit = 20
            elif diff ==3:
                self._difficulty = "Hard"
                self._wordLength = 9
                self._timeLimit = 30
            try:
                self.getWord(topic)
            except ValueError:
                root= Tk()
                root.withdraw()
                messagebox.showerror("No words available", "There are no %s words for topic: %s, please choose another difficulty or topic" % (self._difficulty, self._topic))
                root.destroy()
                self.difficultyMenu(topic)

    def topicMenu(self):
        self._topics = encryption.decrypt("Words")
        self._topics = self._topics.split(":")
        self._topics = self._topics[1:len(self._topics):2]

        self.topicMenuLabel = Label(self.master, text = "Select a topic!", font=("Helvetica", 20), background=bgColor)
        self.topicMenuLabel.pack()
        self.topicMenuLabel.place(x = 275, y = 100, height = 40, width= 250)

        self.topicList = Listbox(self.master)
        self.topicList.pack()
        self.topicList.place(x = 325, y = 160, height = 240, width = 150)

        for a in range(0,len(self._topics)):
            self._topics[a] = self._topics[a].replace("_"," ")
            self.topicList.insert(END, self._topics[a])

        self.confirm = Button(self.master, text = "Confirm", command=lambda: self.topicChosen(self.topicList.curselection()))
        self.confirm.pack()
        self.confirm.place(x = 415, y=440, height = 40, width = 60)

    def topicChosen(self, topic):
        self.topicMenuLabel.destroy()
        self.topicList.destroy()
        self.confirm.destroy()
        try:
            self._topic = self._topics[int(topic[0])]
            self.difficultyMenu(int(topic[0]))
        except IndexError:
            self.topicMenu()

    def getWord(self, topic):
        self._topics = encryption.decrypt("Words")
        self._topics = self._topics.split(":")
        words = self._topics[2:len(self._topics):2]
        words = words[topic]
        words = words.split(",")
        if words[-1] == "":
            words = words[1:-1]
        else:
            words = words[1:len(words)]
        tempWords = []
        hardWords = []
        for item in words:
            if len(item)<self._wordLength:
                tempWords.append(item)
            else:
                hardWords.append(item)
        if self._difficulty == "Hard":
            words = hardWords
        else:
            words = tempWords
        word = words[random.randint(0,len(words)-1)]
        newWord = word
        #Make sure that the word hasn't ended up in the right order
        while newWord == word:
            newWord = list(word)
            random.shuffle(newWord)
            newWord = ''.join(newWord)
        self.game(newWord, word)

    def keyBoard(self, xcoord, ycoord):
        buttonFrame = LabelFrame(self.master, text="LETTERS", bd=3, background=bgColor)
        buttonFrame.pack(padx=10, pady=10)
        buttonFrame.place(x = xcoord, y=ycoord, height=125, width = 322)
        self.buttonList = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        r = 1
        c = 0
        a = 0
        self.buttons = list(range(len(self.buttonList)))
        for item in self.buttonList:
            command = partial(self.input, item)
            self.buttons[a] = Button(buttonFrame, text=item, width=5, command = command)
            self.buttons[a].grid(row=r, column=c)
            a += 1
            c += 1
            if c > 6:
                c = 0
                r += 1
    def clearButtons(self):
        for a in range (0, len(self.buttonList)):
            try:
                self.buttons[a].destroy()
            except:
                pass
        self.cancelButton.destroy()
        if self.__class__.__name__ == "ConundrumGame":
            self.submitButton.destroy()
            self.backButton.destroy()


class ConundrumGame(Game):
    __feedback = ""
    __pointer = 0

    def __init__(self, master):
        menu.master.destroy()
        menu.master.quit()
        self.master = master
        self.master.title("Word Games: Conundrum")
        self.master.geometry("800x500")
        self.master.configure(background=bgColor)
        self.master.resizable(width=FALSE, height=FALSE)
        self.cancelButton = Button(self.master, text="Cancel", command=self.cancel)
        self.cancelButton.pack()
        self.cancelButton.place(x=700, y = 440, height = 40, width = 80)
        playerLabel = Label(self.master, text = "Player: %s" % player.getName(), font=("Helvetica", 12), background=bgColor)
        playerLabel.pack()
        playerLabel.place(x = 20, y= 470, height = 20, width = 140)
        scoreLabel = Label(self.master, text = "Score: %i" % player.getScore(), font=("Helvetica", 12), background=bgColor)
        scoreLabel.pack()
        scoreLabel.place(x = 180, y= 470, height = 20, width = 100)
        self.topicMenu()

    def game(self, word, target):
        self._word = target
        self._guess = "_ "*len(word)
        self.__feedback = "_ "*len(word)
        self.__pointer = 0

        wordLabel = Label(self.master, text = word, font=("Helvetica", 20), foreground="blue", justify=CENTER, background=bgColor)
        wordLabel.pack()
        wordLabel.place(x = 275, y = 100, height = 30, width = 250)

        topicLabel = Label(self.master, text = self._topic, font=("Helvetica", 16), justify=LEFT, background=bgColor)
        topicLabel.pack()
        topicLabel.place(x = 20, y = 20, height = 30, width = 200)

        difficultyLabel = Label(self.master, text = self._difficulty, font=("Helvetica", 12),justify=LEFT, background=bgColor)
        difficultyLabel.pack()
        difficultyLabel.place(x = 20, y= 50, height = 20, width = 200)

        self.playerGuess=Label(self.master, text = self._guess, font=("Helvetica", 18), background =bgColor)
        self.playerGuess.pack()
        self.playerGuess.place(x = 275, y= 160, height = 30, width = 250)

        self.submitButton = Button(self.master, text = "Submit guess", command = self.submit)
        self.submitButton.pack()
        self.submitButton.place(x = 410, y = 200, height = 40, width = 100)

        self.backButton = Button(self.master, text = "Back", command = self.deleteInput)
        self.backButton.pack()
        self.backButton.place(x = 290, y= 200, height = 40, width = 100)

        self.keyBoard(275, 260)
        self.timerRoot = Toplevel(self.master)
        timer = Timer(self.timerRoot, self._timeLimit)
        self.timerRoot.withdraw()

    def input(self, keyPressed):
        if self.__pointer == len(self._word):
            root = Tk()
            root.withdraw()
            messagebox.showwarning("Out of space", "You cannot input any more letters!")
            root.destroy()
        else:
            self._guess = list(self._guess)
            self._guess[self.__pointer*2] = keyPressed
            self._guess = ''.join(self._guess)
            self.__pointer +=1
            self.playerGuess.config(text=self._guess)

    def deleteInput(self):
        if self.__pointer <= 0:
            root = Tk()
            root.withdraw()
            messagebox.showwarning("Nothing to remove!", "The input is empty, there is nothing to remove!")
            root.destroy()
        else:
            self._guess = list(self._guess)
            self._guess[(self.__pointer-1)*2] = "_"
            self._guess = ''.join(self._guess)
            self.__pointer -=1
            self.playerGuess.config(text = self._guess)

    def submit(self):
        if self.__pointer == len(self._word):
            if self._guess[::2] == self._word:
                self.clearButtons()
                root = Tk()
                root.withdraw()
                messagebox.showinfo("You win!", "Good job, %s, you won! The word was %s" % (player.getName(), self._word))
                root.destroy()
                player.addScore(1)
                self.cancel()
            else:
                for a in range (0, len(self._word)):
                    self.__feedback = list(self.__feedback)
                    if self._guess[a*2] == self._word[a]:
                        self.__feedback[a*2] = self._word[a]
                    else:
                        self.__feedback[a*2] = "_"
                    self.__feedback = ''.join(self.__feedback)
                root = Tk()
                root.withdraw()
                messagebox.showwarning("Wrong answer!", "Your guess was wrong. Heres the letters you got in the right order: \n%s" % self.__feedback)
                root.destroy()
                self._guess = "_ " * len(self._word)
                self.playerGuess.config(text=self._guess)
                self.__pointer = 0
        else:
            root = Tk()
            root.withdraw()
            messagebox.showwarning("Submit too early", "Input the entire word before submitting!")
            root.destroy()

    def outOfTime(self):
        try:
            self.timerRoot.destroy()
        except TclError:
            pass
        self.clearButtons()
        root = Tk()
        root.withdraw()
        messagebox.showerror("Times up!", "You're out of time, you lose! The word was %s" % self._word)
        root.destroy()
        player.addScore(-1)
        self.cancel()


class Hangman:
    def __init__(self, canvas):
        self.root=Tk()
        self.root.withdraw()
        self.t = RawTurtle(canvas)
        self.t.hideturtle()
        self.t.speed(0)
        self.t.pu()
        self.t.fd(50)
        self.t.lt(90)
        self.t.fd(100)
        self.t.pd()
        self.t.fd(25)
        self.t.lt(90)
        self.t.fd(100)
        self.t.lt(90)
        self.t.fd(200)
        self.t.lt(90)
        self.t.bk(25)
        self.t.fd(175)
        self.t.bk(50)
        self.t.lt(90)
        self.t.pu()
        self.t.fd(125)
        self.t.rt(90)
        self.t.pd()

    def update(self, attempts):
        if attempts == 5:
            self.t.circle(25)
            self.t.rt(90)
        elif attempts == 4:
            self.t.fd(100)
            self.t.bk(75)
        elif attempts == 3:
            self.t.rt(45)
            self.t.fd(25)
            self.t.bk(25)
            self.t.lt(45)
        elif attempts == 2:
            self.t.lt(45)
            self.t.fd(25)
            self.t.bk(25)
            self.t.rt(45)
            self.t.fd(75)
        elif attempts == 1:
            self.t.rt(45)
            self.t.fd(25)
            self.t.bk(25)
            self.t.lt(45)
        else:
            self.t.lt(45)
            self.t.fd(25)
            hangmanGame.clearButtons()
            messagebox.showerror("Loser", "You just lost the game. The word was %s" % hangmanGame.getTargetWord())
            player.addScore(-1)
            self.root.destroy()
            hangmanGame.cancel()

class HangmanGame(Game):
    __guesses = 6
    __correct = False

    def __init__(self, master):
        menu.master.destroy()
        menu.master.quit()
        self.master = master
        self.master.title("Word Games: Hangman")
        self.master.geometry("800x500")
        self.master.configure(background=bgColor)
        self.master.resizable(width=FALSE, height=FALSE)
        self.cancelButton = Button(self.master, text="Cancel", command=self.cancel)
        self.cancelButton.pack()
        self.cancelButton.place(x=700, y = 440, height = 40, width = 80)
        playerLabel = Label(self.master, text = "Player: %s" % player.getName(), font=("Helvetica", 12), background=bgColor)
        playerLabel.pack()
        playerLabel.place(x = 20, y= 470, height = 20, width = 140)
        scoreLabel = Label(self.master, text = "Score: %i" % player.getScore(), font=("Helvetica", 12), background=bgColor)
        scoreLabel.pack()
        scoreLabel.place(x = 180, y= 470, height = 20, width = 100)
        self.topicMenu()

    def input(self, keyPressed):
        self.__correct = False
        self.buttons[ord(keyPressed)-97].destroy()
        for a in range (0, len(self._word)):
            if self._word[a] == keyPressed:
                self._guess = list(self._guess)
                self._guess[a*2] =keyPressed
                self._guess = ''.join(self._guess)
                self.wordBlanks.config(text= self._guess)
                self.__correct = True
        if self._guess[0:len(self._guess):2]== self._word:
            self.clearButtons()
            messagebox.showinfo("Winner!","Well done, " + player.getName() + ", You just won the game! The word was %s!" % self._word)
            player.addScore(1)
            self.cancel()
        if self.__correct == False:
            self.__guesses-=1
            hangman.update(self.__guesses)

    def game(self, temp, word):
        self._guess = "_ " * len(word)
        self._word = word
        self.wordBlanks = Label(self.master, text = self._guess, font=("Helvetica", 20), justify=LEFT, background=bgColor)
        self.wordBlanks.pack()
        self.wordBlanks.place(x = 100, y = 160, height = 30)

        hangmanCanvas = Canvas(self.master)
        hangmanCanvas.pack()
        hangmanCanvas.place(x = 480, y=20, width = 300,height = 300)
        global hangman
        hangman=Hangman(hangmanCanvas)

        topicLabel = Label(self.master, text = self._topic, font=("Helvetica", 16), justify=LEFT, background=bgColor)
        topicLabel.pack()
        topicLabel.place(x = 20, y = 20, height = 30, width = 200)

        difficultyLabel = Label(self.master, text = self._difficulty, font=("Helvetica", 12),justify=LEFT, background=bgColor)
        difficultyLabel.pack()
        difficultyLabel.place(x = 20, y= 50, height = 20, width = 200)

        self.keyBoard(100, 200)

    def getTargetWord(self):
        return self._word

class Timer:
    def __init__(self, master, timeLimit):
        master.after(timeLimit*1000, conundrumGame.outOfTime)

class EditMenu:
    attempts= 3

    def __init__(self, master):
        menu.master.destroy()
        menu.master.quit()
        self.master = master
        self.master.title("Word Games: Edit Words")
        self.master.geometry("800x500")
        self.master.configure(background=bgColor)
        self.master.resizable(width=FALSE, height=FALSE)
        cancelButton = Button(self.master, text="Quit", command=self.cancel)
        cancelButton.pack()
        cancelButton.place(x=700, y = 440, height = 40, width = 80)

        self.passwordLabel = Label (self.master, text="Please enter the password", font=("Helvetica", 18), background = bgColor, justify = CENTER)
        self.passwordLabel.pack()
        self.passwordLabel.place(x= 250, y=170, height = 40, width = 300)
        self.passwordInput = Entry(self.master, font=("Helvetica", 20), show="*")
        self.passwordInput.pack()
        self.passwordInput.place(x=275, y=210, height = 40, width = 250)
        self.passwordInput.focus_set()

        self.submit = Button(self.master, text = "Submit", command=lambda: self.login(self.passwordInput.get()))
        self.submit.pack()
        self.submit.place(x= 400, y=270, height = 40, width = 125)

    def cancel(self):
        try:
            self.root.destroy()
        except AttributeError:
            pass
        root = Tk()
        global menu
        menu = Menu(root)
        self.master.destroy()
        self.master.quit()

    def login(self,passW):
        if passW == password:
            self.passwordLabel.destroy()
            self.passwordInput.destroy()
            self.submit.destroy()
            self.editMenu()
        else:
            self.attempts -=1
            root = Tk()
            root.withdraw()
            messagebox.showerror("Invalid Password", "Wrong password entered, %i attempts remaining" % self.attempts)
            root.destroy()
            self.passwordInput.delete(0,END)
            if self.attempts == 0:
                self.cancel()

    def getWords(self):
        self.allWords = {}
        topicID = 0
        self.topics = encryption.decrypt("Words")
        self.topics = self.topics.split(":")
        words = self.topics[2:len(self.topics):2]
        self.topics = self.topics[1:len(self.topics):2]
        for item in self.topics:
            self.allWords[item] = words[topicID]
            self.allWords[item] = self.allWords[item].split(",")
            if self.allWords[item][-1] == "":
                self.allWords[item] =self.allWords[item][1:-1]
            else:
                self.allWords[item] = self.allWords[item][1:len(self.allWords[item])]
            topicID+=1
        for item in self.topics:
            self.topicList.insert(END, item.replace("_", " "))

    def selectTopic(self, topic):
        self.wordList.delete(0, END)
        try:
            words = self.topics[int(topic[0])]
            words = self.allWords.get(words)
            self.selectedTopic = self.topics[int(topic[0])]
            for item in words:
                self.wordList.insert(END,item)
        except IndexError:
            root= Tk()
            root.withdraw()
            messagebox.showinfo("No topic selected", "Please select a topic!")
            root.destroy()

    def removeTopic(self, topicID):
        self.wordList.delete(0, END)
        self.selectedTopic=""
        try:
            del self.allWords[self.topics[int(topicID[0])]]
            self.topics.remove(self.topics[int(topicID[0])])
            self.topicList.delete(0,END)
            for item in self.topics:
                self.topicList.insert(END, item.replace("_", " "))
        except IndexError:
            root= Tk()
            root.withdraw()
            messagebox.showinfo("No topic selected", "Please select a topic!")
            root.destroy()

    def addTopic(self):
        createTopic=Toplevel(self.master)
        createTopic.title("Add a topic!")
        createTopic.geometry("160x100")
        topicName = Entry(createTopic)
        topicName.pack()
        topicName.place(x = 20, y=20, height = 20, width = 120)
        submitName = Button(createTopic, text="Submit", command= lambda: submit(topicName.get()))
        submitName.pack()
        submitName.place(x = 50, y = 60, width = 60, height = 20)
        def submit(name):
            flag = False
            same = False
            createTopic.destroy()

            if name.strip() =="":
                root = Tk()
                root.withdraw()
                messagebox.showwarning("Bad input", "Nothing was input!")
                root.destroy()
                self.addWord()
            else:
                for letter in name.lower():
                    if letter not in ascii_lowercase:
                        if letter != " ":
                            flag = True
                for item in self.topics:
                    if item.lower() == name.lower():
                        same = True

                if flag ==True:
                    root = Tk()
                    root.withdraw()
                    messagebox.showwarning("Bad input", "Please input only characters and spaces")
                    root.destroy()
                    self.addTopic()
                elif same == True:
                    root = Tk()
                    root.withdraw()
                    messagebox.showwarning("Bad input", "This topic already exists!")
                    root.destroy()
                    self.addTopic()
                else:
                    self.allWords[name.replace(" ","_")] = []
                    self.topics.append(name.replace(" ","_"))
                    self.topicList.delete(0,END)
                    for item in self.topics:
                        self.topicList.insert(END, item.replace("_", " "))

    def addWordValidate(self):
        if self.selectedTopic=="":
            root = Tk()
            root.withdraw()
            messagebox.showwarning("Bad input", "Select a topic first!")
            root.destroy()
        else:
            self.addWord()

    def addWord(self):
        createWord=Toplevel(self.master)
        createWord.title("Add a word!")
        createWord.geometry("160x100")
        wordName = Entry(createWord)
        wordName.pack()
        wordName.place(x = 20, y=20, height = 20, width = 120)
        submitName = Button(createWord, text="Submit", command= lambda: submit(wordName.get()))
        submitName.pack()
        submitName.place(x = 50, y = 60, width = 60, height = 20)
        def submit(name):
            flag = False
            same = False
            createWord.destroy()


            if name.strip() =="":
                root = Tk()
                root.withdraw()
                messagebox.showwarning("Bad input", "Nothing was input!")
                root.destroy()
                self.addWord()
            else:
                for letter in name.lower():
                    if letter not in ascii_lowercase:
                        flag = True
                if name.lower() in self.allWords[self.selectedTopic]:
                    same = True

                if flag ==True:
                    root = Tk()
                    root.withdraw()
                    messagebox.showwarning("Bad input", "Please input only characters without spaces, only 1 word is allowed.")
                    root.destroy()
                    self.addWord()
                elif same == True:
                    root = Tk()
                    root.withdraw()
                    messagebox.showwarning("Bad input", "This word already exists!")
                    root.destroy()
                    self.addWord()
                else:
                    self.allWords[self.selectedTopic].append(name.lower())
                    self.wordList.delete(0,END)

    def removeWord(self, word):
        self.wordList.delete(0, END)
        try:
            self.allWords[self.selectedTopic].remove(self.allWords[self.selectedTopic][int(word[0])])
            self.selectedTopic=""
        except IndexError:
            root= Tk()
            root.withdraw()
            messagebox.showinfo("No word selected", "Please select a word and topic!")
            root.destroy()

    def editMenu(self):
        self.selectedTopic=""
        topicLabel = Label(self.master, text = "Choose a topic to edit!", font=("Helvetica", 16), background = bgColor, justify=LEFT)
        topicLabel.pack()
        topicLabel.place(x = 20, y = 60, height =40, width = 300)

        wordLabel = Label(self.master, text = "Add or remove words!", font=("Helvetica", 16), background = bgColor, justify=LEFT)
        wordLabel.pack()
        wordLabel.place(x = 340, y = 60, height =40, width = 300)

        self.topicList = Listbox(self.master)
        self.topicList.pack()
        self.topicList.place(x = 70, y = 120, height = 300, width = 200)

        self.wordList = Listbox(self.master)
        self.wordList.pack()
        self.wordList.place(x = 390, y = 120, height = 300, width = 200)

        self.getWords()

        topicSelect = Button(self.master, text = "Select topic", command= lambda: self.selectTopic(self.topicList.curselection()))
        topicSelect.pack()
        topicSelect.place(x =290, y = 120, height = 40, width = 80)

        topicAdd = Button(self.master, text = "Add topic", command = self.addTopic)
        topicAdd.pack()
        topicAdd.place(x =290, y = 180, height = 40, width = 80)

        topicRemove = Button(self.master, text = "Remove topic", command= lambda: self.removeTopic(self.topicList.curselection()))
        topicRemove.pack()
        topicRemove.place(x =290, y = 240, height = 40, width = 80)

        wordAdd = Button(self.master, text = "Add word", command= self.addWordValidate)
        wordAdd.pack()
        wordAdd.place(x =610, y = 120, height = 40, width = 80)

        wordRemove = Button(self.master, text = "Remove word", command= lambda: self.removeWord(self.wordList.curselection()))
        wordRemove.pack()
        wordRemove.place(x =610, y = 180, height = 40, width = 80)

        defaultButton = Button(self.master, text= "Restore", command = self.restoreDefaults)
        defaultButton.pack()
        defaultButton.place(x = 700, y = 320, height = 40, width =80)

        saveButton = Button(self.master, text = "Save changes", command= self.save)
        saveButton.pack()
        saveButton.place(x=700, y = 380, height = 40, width = 80)

    def restoreDefaults(self):
        root =Tk()
        root.withdraw()
        if messagebox.askokcancel("Restore default topics?", "Are you sure you wish to reset all words and topics? Any words added will be removed and the default topics & words will be restored"):
            self.wordList.delete(0, END)
            self.topicList.delete(0, END)
            file = open("Default.txt", "r")
            defaults= file.read()
            file.close()
            file= open("Words.txt", "w")
            file.write(defaults)
            file.close()
            self.getWords()
        root.destroy()

    def save(self):
        text = ""
        for item in self.allWords.keys():
            text = text + ":" + item + ":,"
            for word in self.allWords[item]:
                text = text + word + ","
        encryption.encrypt(text, "Words")
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Save successful!", "All topics and words saved to file, they can now be used in-game")
        root.destroy()

def main():
    root = Tk()
    playername = PlayerName(root)
    root.mainloop()
    try:
        if player.getName() =="":
            try:
                root.destroy()
            except TclError:
                pass
            sys.exit()
    except NameError: #If the user closes the PlayerName class before a name is entered
        sys.exit()

    root = Tk()
    global menu
    menu = Menu(root)
    root.mainloop() #Have our program 'listen' for events

if __name__ == "__main__":
    main()