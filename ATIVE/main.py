from gtts import gTTS as gt
import speech_recognition as sr
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import nltk
import random
import string
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pygame
from pygame import mixer
import pygame.mixer as m
import sys
import  time

#pygame
pygame.init()
mixer.init()
screen = pygame.display.set_mode((500, 500))
m.music.load('intro1.mp3')
m.music.set_volume(1)
m.music.play(1)
m.stop()
time.sleep(1.5)
#bg and music
BG=pygame.image.load('img.png')
pygame.display.set_caption("ATIVE")
m.music.load('intro3.mp3')
m.music.set_volume(1)
m.music.play(1)
m.stop()


pos=()
run=True
st_t = pygame.font.Font('freesansbold.ttf', 23)
st_o = pygame.font.Font('freesansbold.ttf', 14)
a=""

#bot
user_response=""
robo_response=""
f=open('data.txt','r',errors='ignore')
raw=f.read()
raw=raw.lower()
#nltk.download('punkt')
#nltk.download('wordnet')
sent_tokens=nltk.sent_tokenize(raw)
word_tokens=nltk.word_tokenize(raw)
botreply=""
#lemetising
lemmer = nltk.stem.WordNetLemmatizer()
flag=False
print("---------------------active activated------------------")
print("Hey I'm Ative")
y=30
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punkt_dict= dict((ord(punkt),None) for punkt in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punkt_dict)))
#GREETINGS
greet_in=["hi","hello","atvie","hey"]
greet_out=["hey","how can i help u","hiii","I'm glad to help u"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greet_in:
            return random.choice(greet_out)
#Response
def response(user_response):
    try:
        global robo_response
        robo_response=""
        sent_tokens.append(user_response)
        TfidfVec =TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf= TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1],tfidf)
        idx=vals.argsort()[0][-2]
        flat= vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            robo_response= robo_response+"sorry i am not able to understand"
            return robo_response
        else:
            robo_response= robo_response+sent_tokens[idx]
            return robo_response
    except:
        return robo_response+"CAN U MIND REPEATING"
def speech():

    global user_response,flag,botreply,ser,rep
    flag=True
    txt = "VOICE ACTIVATED"
    LANG = "en"
    output = gt(text=txt, lang=LANG, slow=False)
    output.save("output1.mp3")
    m.music.stop()
    m.music.load('output1.mp3')
    m.music.set_volume(1)
    m.music.play(1)
    m.stop()



    user_response=" "
    botreply = "VOICE ACTIVATED"
    while (flag == True):

        flag=False
        r = sr.Recognizer()
        print("speak....")
        with sr.Microphone() as source:
            botreply = "listening...."
            print("listening....")

            r.adjust_for_ambient_noise(source, duration=.5)
            audio = r.listen(source)
            try:
                botreply = "recognizing...."
                print("recognizing....")

                user_response = r.recognize_google(audio)
                print("me  :", user_response)

                user_response = user_response.lower()
                if (user_response == "movie"):
                    botreply = "movie name?"
                    print("bot:movie name:")

                    botreply = "listening"

                    print("listening....")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source)
                    try:
                        botreply = "recognizing"
                        print("recognizing....")

                        user_response = r.recognize_google(audio)
                        user_response = user_response.lower()
                        movie()

                    except:
                        botreply = "sorry voice not recognized"

                        print("sorry voice not recognized")
                        botreply = "Try again by saying movie"

                        print("Try again by saying movie")
                if (user_response == "youtube" or user_response == "utube"):
                    Y = True
                    botreply = "PRESS ENTER"
                if (user_response != "bye"):
                    if (user_response == "thanks" or user_response == "thankyou" or user_response == "thank you"):
                        flag = False
                        botreply = "thnaku"
                        print("thanku")
                        break


                    else:
                        if (greeting(user_response) != None):
                            try:
                                botreply = str(greeting(user_response))
                                print("bot: " + greeting(user_response))
                            except:
                                break
                        else:
                            try:
                                print("bot: ", end="")
                                print(response(user_response))
                                botreply = str(response(user_response))
                                sent_tokens.remove(user_response)
                            except:
                                break
                else:

                    flag = False
                    user_response = " "
                    botreply = "thanku"
                    print("thanku")
                    break


            except:
                user_response=" "
                botreply = "sorry voice not recognized"
                print("sorry voice not recognized")
    m.music.unload()
    os.remove("output1.mp3")
    flag=False
    rep=True
    print(2, flag)

seq=""
def movie():
    global botreply,user_response

    try:
        global flag,botreply,user_response

        botreply = "getting ur movie torrent wait min"
        a=user_response
        a = a.lower()
        ul="https://yts.mx/browse-movies/"+a
        options = Options()
        options.add_argument("--user-data-dir=C:\\Users\\Nithesh R\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

        web=webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=options)
        web.get(ul)
        user_response = " "
        print("TORRENT DOWNLOADED")
    except:
        print("network error")
def utube():
    global botreply,user_response
    try:

        ul="https://youtube.com"
        options = Options()
        options.add_argument("--user-data-dir=C:\\Users\\Nithesh R\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        web=webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=options)
        web.get(ul)
        user_response = " "
        botreply="OPENED"
        print("opened")
    except:
        print("network error")

def search():
    global botreply,user_response
    try:
        a=seq
        a=a.lower()
        botreply = "U GOT wat ur looking for"
        ul="https://www.google.com"
        options = Options()
        options.add_argument("--user-data-dir=C:\\Users\\Nithesh R\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        web=webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe", options=options)
        web.get(ul)
        web.find_element_by_name("q").send_keys(a)
        web.find_element_by_name("q").send_keys(Keys.ENTER)


        print("U GOT wat ur looking for")
        user_response=" "
        botreply="DONE"
    except:
        botreply="network error"
        print("network error")
b=""
def process():
    global  pos,start,r,b
    pygame.draw.rect(screen, (255, 255, 255), (390, 450, 90, 40), 4)
    t = st_t.render('VOICE ', True, (255, 255, 255))
    screen.blit(t, (400, 460))
    if r:
        t = st_o.render("me:" + user_response, True, (255, 255, 255))
        screen.blit(t, (10, 460))
    if len(pos) > 0 and not start:
        for i in range(390, 480):
            for j in range(450, 490):
                if pos[0] == i and pos[1] == j:
                    pygame.draw.rect(screen, (0, 0, 29), (390, 450, 90, 40))
                    pygame.draw.rect(screen, (255, 255, 255), (390, 450, 90, 40), 4)
                    t = st_t.render('VOICE ', True, (255, 255, 255))
                    screen.blit(t, (400, 460))
    if len(pos) > 0 and not start:
        for i in range(0, 370):
            for j in range(450, 490):
                if pos[0] == i and pos[1] == j:
                    pygame.draw.rect(screen, (0, 0, 50), (0, 450, 370, 40))
                    pygame.draw.rect(screen, (255, 255, 255), (0, 450, 370, 40), 4)
                    t = st_t.render('TYPE HERE', True, (255, 255, 255))
                    screen.blit(t, (150, 460))
    if len(pos) > 0 and start:
        for i in range(0, 370):
            for j in range(450, 490):
                if pos[0] == i and pos[1] == j:
                    print(2)

                    start = False
    if len(pos) > 0 and  start:
        for i in range(390, 480):
            for j in range(450, 490):
                if pos[0] == i and pos[1] == j:
                    print(1)
                    speech()
                    start=False
def boom():
    global  st_o

    t = st_o.render("---------------------active activated------------------", True, (255, 255, 255))
    screen.blit(t, (10,10 ))
    t = st_o.render("Hey I'm Ative ", True, (255, 255, 255))
    screen.blit(t, (10,30))
    pygame.draw.rect(screen, (255, 255, 255), (0, 450, 370, 40), 4)

def reply():

    global so,b,c
    c=b
    t = st_o.render("me:"+str(c), True, (255, 255, 255))
    screen.blit(t, (10, 50))

def botrep():
    global  so,botreply,flag,d
    d=botreply
    t = st_o.render("bot:" + str(d), True, (255, 255, 255))
    screen.blit(t, (10, 70))


ser=False
M=False
S=False
Y=False


query=False
start=False
r=False
rep=False
so=False

while run:


    screen.blit(BG, (0,10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                pos = pygame.mouse.get_pos()
                start=True
        if event.type == pygame.MOUSEMOTION:

            pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN :
            if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE :
                user_response+=event.unicode
                r=True
            if event.key == pygame.K_RETURN and r:
                 b = ""
                 botreply = ""

                 b=user_response
                 reply()
                 rep=True
                 so=True
                 flag=True
                 if query:
                     seq = user_response

                 if M:
                     movie()
                     M=False
                 if Y:
                     utube()
                     Y = False

                 if S:
                     S=False
                     search()


            if event.key == pygame.K_BACKSPACE:
                 c=len(user_response)
                 user_response=user_response[0:c-1]
                 b=user_response

    if flag and not ser:
        print("r")
        user_response=user_response.lower()
        print(user_response)
        if user_response==" " :
            flag=False
        if(user_response=="movie"):
            print("bot:movie name:",end="")
            botreply="movie name:"


            print("bot:getting ur movie torrent wait min")
            M=True
            flag = False
            query=True


        if(user_response=="youtube" or user_response=="utube" ):
            Y=True
            botreply="PRESS ENTER"
            flag = False
        if(user_response=="search"):
            botreply="bot wat do u wanna search :"
            print("bot wat do u wanna search :",end="")
            print("bot:")
            S=True
            flag = False
            query = True

        if(user_response!="bye") and flag:
         if(user_response == "thanks" or user_response == "thankyou"):
             flag=False
             botreply = "thanks"
             print("thanku")
             break

         else:
             print("r1")
             if(greeting(user_response)!=None):
                botreply = str(greeting(user_response))
                print("bot: "+greeting(user_response))
                flag = False
             else:#if(greeting(user_response)==None or u== ""):
                    try:
                        print("r2")
                        print("bot: ",end="")
                        botreply = str(response(user_response))
                        sent_tokens.remove(user_response)
                        flag = False
                    except:
                        print()
                        flag = False
        elif user_response=="bye":
            flag=False
            botreply = "thanks"
            print("thanku")

        user_response = ""

    process()
    boom()

    if rep:
        reply()
        botrep()
    pygame.display.update()
    flag=False


