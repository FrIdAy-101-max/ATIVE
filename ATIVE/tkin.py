from tkinter import  *
from tkinter import font
from PIL import ImageTk,Image
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import nltk
import random
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
root=Tk()
root.title("ATIVE")
#root.iconbitmap("img.png")
root.geometry("600x400")
fontf=font.Font(family="Helvetica",size=15,weight="bold")
fontv=font.Font(family="Helvetica",size=10)
#declarartion

robo_response = ""

flag = True
print("---------------------active activated------------------")
print("Vanakam da mapala computer la irrundhu")
print("Hey I'm Ative")

f = open('data.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()
# nltk.download('punkt')
# nltk.download('wordnet')
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)


#tk starting
im=ImageTk.PhotoImage(Image.open("img.png"))
i=Label(root,image=im)
i.pack(side="bottom",fill="both",expand="yes")
e=Entry(root,width=60,bd=8,)
e.place(relx=0.65, rely=0.98, anchor=SE,height=40)

lab1=Label(i,text="ATIVE AT YOUR SERVICE",bg="black",fg="white",font=fontf)
lab1.place(x=0,y=0,anchor=NW)

user_response=""
X1=10
X2=20
def myclick():
    speech()
    return
def myclick1():
    global user_response,robo_response,flag
    lab1 = Label(i, text="ATIVE AT YOUR SERVICE", bg="black", fg="white",font=fontf )
    lab1.place(x=0, y=0, anchor=NW)
    user_response = e.get()
    while (flag == True):

        # user_response = input("me :")
        user_response = user_response.lower()
        if (user_response == "movie"):
            print("bot:movie name:", end="")

            robo_response="getting ur movie torrent wait min"
            print("bot:getting ur movie torrent wait min")
            user_response = askstring('Name', 'What is the  name ot he movie?')
            showinfo('movie', 'done')
            movie()

            break

        if (user_response == "voice"):
            print("voice chat activated")
            robo_response="voice chat activated"
            speech()
        if (user_response == "youtube" or user_response == "utube"):
            utube()
            break
        if (user_response == "google"):
            print("bot wat do u wanna search :")
            robo_response="wat do u wanna search"
            user_response = askstring('Name', 'What do u want to search')
            showinfo('', 'done')

            search()
            break
        if (user_response != "bye"):
            if (user_response == "thanks" or user_response == "thankyou"):
                flag = False
                robo_response="thanku"
                print("thanku")
                break

            else:
                if (greeting(user_response) != None):
                    robo_response=greeting(user_response)
                    print("bot: " + robo_response)
                    break
                else:  # if(greeting(user_response)==None or u== ""):
                    try:
                        print("bot: ", end="")
                        robo_response=response(user_response)
                        print(response(user_response))
                        sent_tokens.remove(user_response)
                    except:
                        break
        else:
            flag = False
            robo_response="thanku"
            print("thanku")
            break

    lab1 = Label(i, text="ME:     " + user_response, bg="black", fg="white",font=fontv )
    lab1.place(x=0, y=40, anchor=NW)
    lab1 = Label(i, text="BOT:    "+robo_response, bg="black", fg="white",font=fontv )
    lab1.place(x=0, y=70, anchor=NW)
    return
myButton=Button(root,text="VOICE", command=myclick,width=10,height=2)
myButton.place(relx=0.95, rely=0.98, anchor=SE)
myButton=Button(root,text="ENTER", command=myclick1,width=10,height=2)
myButton.place(relx=0.80, rely=0.98, anchor=SE)

from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo


#MAIN CODE


# lemetising
lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punkt_dict = dict((ord(punkt), None) for punkt in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punkt_dict)))


# GREETINGS
greet_in = ["hi", "hello", "atvie", "hey"]
greet_out = ["hey", "how can i help u", "hiii", "I'm glad to help u"]


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greet_in:
            return random.choice(greet_out)


# Response
def response(user_response):
    global robo_response

    try:
        robo_response = ""
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            robo_response = robo_response + "sorry i am not able to understand"
            return robo_response
        else:
            robo_response = robo_response + sent_tokens[idx]
            return robo_response
    except:
        return robo_response + "CAN U MIND REPEATING"


def speech():
    global user_response, flag,robo_response
    while (flag == True):
        r = sr.Recognizer()
        print("speak....")
        with sr.Microphone() as source:

            print("listening....")
            r.adjust_for_ambient_noise(source, duration=.5)
            audio = r.listen(source)
            try:
                print("recognizing....")
                user_response = r.recognize_google(audio)
                print("me  :", user_response)
                user_response = user_response.lower()
                if (user_response == "movie"):
                    print("bot:movie name:")
                    print("listening....")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source)
                    try:
                        print("recognizing....")
                        user_response = r.recognize_google(audio)
                        user_response = user_response.lower()
                        movie()
                        break
                    except:
                        print("sorry voice not recognized")
                        print("Try again by saying movie")
                if (user_response == "youtube" or user_response == "utube"):
                    utube()
                    break
                if (user_response == "google"):
                    print("listening....")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source)
                    try:
                        print("recognizing....")
                        user_response = r.recognize_google(audio)
                        user_response = user_response.lower()
                        search()
                        break
                    except:
                        print("sorry voice not recognized")
                        print("Try again by saying")

                if (user_response != "bye"):
                    if (user_response == "thanks" or user_response == "thankyou" or user_response == "thank you"):
                        flag = False
                        robo_response="thanku"
                        print("thanku")
                        break


                    else:
                        if (greeting(user_response) != None):
                            try:
                                robo_response=greeting(user_response)
                                print("bot: " + greeting(user_response))
                            except:
                                break
                        else:
                            try:
                                print("bot: ", end="")
                                robo_response=response(user_response)
                                print(response(user_response))
                                sent_tokens.remove(user_response)
                            except:
                                break
                else:

                    flag = False
                    robo_response="thanku"
                    print("thanku")
                    break


            except:
                robo_response="sorry voice not recognized"
                print("sorry voice not recognized")


def movie():
    global flag, robo_response,user_response
    try:

        a = user_response
        b = "https://yts.mx/browse-movies/" + a
        options = Options()
        options.add_argument("--user-data-dir=C:\\Users\\Nithesh R\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

        web = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=options)
        web.get(b)
        robo_response='TORRENT DOWNLOADED'
        print("TORRENT DOWNLOADED")
    except:
        robo_response="network error"
        print("network error")


def utube():
    global  user_response,robo_response
    try:
        a = user_response
        b = "https://youtube.com"
        options = Options()
        options.add_argument("--user-data-dir=C:\\Users\\Nithesh R\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        web = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=options)
        web.get(b)
        robo_response="opened"
        print("opened")
    except:
        robo_response="network error"
        print("network error")


def search():
    global user_response,robo_response
    try:
        a = user_response
        b = "https://www.google.com"
        options = Options()
        options.add_argument("--user-data-dir=C:\\Users\\Nithesh R\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        web = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=options)
        web.get(b)
        web.find_element_by_name("q").send_keys(a)
        web.find_element_by_name("q").send_keys(Keys.ENTER)
        robo_response="U GOT wat ur looking for"
        print("U GOT wat ur looking for")
    except:
        robo_response="network error"
        print("network error")



user_response=""
robo_response=""
root.mainloop()








