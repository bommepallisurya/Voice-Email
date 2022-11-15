import speech_recognition as sr
import smtplib
import ssl
import csv
# import pyaudio
# import platform
# import sys
from bs4 import BeautifulSoup
import email
import pyttsx3 as pyttsx
import imaplib
from gtts import gTTS
import pyglet
import os, time

engine = pyttsx.init()
engine.setProperty('rate', 200)
r = sr.Recognizer()

dataBase = open("VoiceEmailDB.csv", "w+")
LOGGED_MAIL = ""
LOGGED_EMAIL =""
LOGGED_PASSWORD = ""
def speakIt(sentence):
    print(sentence)
    engine.say(sentence)
def recordUser():
    
    i=0
    while True:
        with sr.Microphone() as source:
            print("listening...")
            engine.runAndWait()
            r.adjust_for_ambient_noise(source)
            audio=r.listen(source)
            print ("ok done!!")

        try:
            text=r.recognize_google(audio)
            speakIt("You said, "+text)
            return text;
        
        except sr.UnknownValueError:
            i=i+1
            if i>3:
                engine.say("Sorry I am unable to understand you, You have reached maximum tries. Please re-start the program")
                exit()
            print("Google Speech Recognition could not understand audio.")
            engine.say("Sorry I didn't get you please repeat")
            continue;
         
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
            engine.say("Sorry Some Error Occured, Please re-start, Bye Bye")
            exit()
            
            
def signUp():
    speakIt("Please say your full name")
    fullName = recordUser()
    speakIt("Please spell your email")
    email = recordUser()
    email = email.lower()
    email = email.replace(" ","")
    email=email.replace("dot",".")
    email=email.replace("attherate","@")
    email=email.replace("adtherate","@")
    email=email.replace("atrate","@")
    email=email.replace("therate","@")
    speakIt("Your email is "+email)
    speakIt("Please say your password")
    password = recordUser()
    password = password.strip()
    #with open('employee_birthday.txt') as csv_file:
    speakIt("Do you wish to submit or reset, Say 1 to submit Say 2 to reset signup form")
    confirmation = recordUser()
    confirmation = confirmation.lower()
    if confirmation=="two" or confirmation=="2" or confirmation=='to' or confirmation=='tu':
        speakIt("Please wait re-setting the form")
        signUp()
        return;
    with open('VoiceEmailDB.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row[1]==email:
                speakIt("Account Already exists, Returning back to main menu")
                MainMenu()
                return;
    with open("VoiceEmailDB.csv", 'w') as csvfile: 
        csvwriter = csv.writer(csvfile)
        newRecord=[str(fullName), str(email), str(password)]
        csvwriter.writerow(newRecord) 
        
    speakIt("Account registered successfully, Returning back to main menu")
    MainMenu()
            


def login():
    global LOGGED_EMAIL
    global LOGGED_PASSWORD
    speakIt("Please spell your email")
    email = recordUser()
    email = email.lower()
    email = email.replace(" ","")
    email=email.replace("dot",".")
    email=email.replace("attherate","@")
    email=email.replace("adtherate","@")
    email=email.replace("atrate","@")
    email=email.replace("therate","@")
    speakIt("Your email is "+email)
    speakIt("Please say your password")
    
    password = recordUser()
    password = password.strip()
    speakIt("Please wait logging in")
    isFound=False
    with open('VoiceEmailDB.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row[1]==email:
                isFound = True
                return; 
    isFound=True
    if not isFound :
        speakIt("Account not found, Please Sign Up")
        MainMenu()
        return;
    speakIt("Do you wish to submit or reset, Say 1 to submit Say 2 to reset login form")
    confirmation = recordUser()
    confirmation = confirmation.lower()
    if confirmation=="two" or confirmation=="2" or confirmation=='to' or confirmation=='tu':
        speakIt("Please wait re-setting the form")
        login()
        return;
    
    LOGGED_EMAIL="rajeswarreddy.meka@gmail.com"
    LOGGED_PASSWORD="Raj#mail9010503069"
    
    
    connectToGmail()

def connectToGmail():
    global LOGGED_MAIL
    try:
        LOGGED_MAIL = imaplib.IMAP4_SSL("imap.gmail.com",993)
        #LOGGED_MAIL.ehlo()                                                                             #Hostname to send for this command defaults to the FQDN of the local host.
        #LOGGED_MAIL.starttls()     
        LOGGED_MAIL.login(LOGGED_EMAIL,LOGGED_PASSWORD)
        speakIt("Login Successful")
        gmailMenu()
    except Exception as e: 
        print(str(e))
        speakIt("Cannot connect to gmail, Check your credentials")
        MainMenu()

def gmailMenu():
    speakIt("Option 1. Send Email, Option 2. Read Inbox, Option 3. Log Out, Please say your option number")
    userChoice = recordUser()
    
    userChoice = userChoice.lower()
    if userChoice == '1' or userChoice == 'option 1' or userChoice == 'one'  or userChoice == 'option one':
        sendEmail()
    elif userChoice == '2' or userChoice == 'option 2' or userChoice == 'two' or userChoice=='to' or userChoice=='tu' or userChoice == 'option two' or userChoice == 'option tu' or userChoice == 'option to':
        readInbox()
    elif userChoice == '3' or userChoice == 'option 3' or userChoice == 'three':
        MainMenu()
    else :
        speakIt("Sorry, Try again")
        gmailMenu()
        return

def sendEmail():
    speakIt("spell receiver email")
    email = recordUser()
    email = email.replace(" ","")
    email=email.replace("dot",".")
    email=email.replace("attherate","@")
    email=email.replace("adtherate","@")
    email=email.replace("atrate","@")
    email=email.replace("therate","@")
    speakIt("Receiver email is "+email)
    speakIt("What is the subject of email")
    subject = recordUser()
    speakIt("What is the body of email")
    
    msg = recordUser()
    message = """\
    Subject: """+subject+"""

    """+msg
    speakIt("Do you wish to send or cancel, Say 1 to send Say 2 to reset ")
    confirmation = recordUser()
    confirmation = confirmation.lower()
    if confirmation=="two" or confirmation=="2" or confirmation=='to' or confirmation=='tu':
        speakIt("Please wait re-setting the mail")
        gmailMenu()
        return;
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(LOGGED_EMAIL, LOGGED_PASSWORD)
        server.sendmail(LOGGED_EMAIL,"rajeshwarreddy.meka@gmail.com",message)
    speakIt("Email Sent successfully, Returning back to menu")
    gmailMenu()
    

def readInbox():
    try:
        speakIt("Please wait fetching mails, This might take few minutes")
        LOGGED_MAIL.select('inbox')

        data = LOGGED_MAIL.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = LOGGED_MAIL.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    speakIt('From : ' + email_from + '\n')
                    speakIt('Subject : ' + email_subject + '\n')

    except Exception as e:
       
        print(str(e))
        speakIt("Cannot read emails try again")
    gmailMenu()
    
def MainMenu():
    speakIt("Option 1. Sign Up, Option 2. Login, Please say your option number")
    userChoice = recordUser()
    
    userChoice = userChoice.lower()
    #choices details
    if userChoice == '1' or userChoice == 'option 1' or userChoice == 'one'  or userChoice == 'option one':
        signUp()
    elif userChoice == '2' or userChoice == 'option 2' or userChoice == 'two' or userChoice=='to' or userChoice=='tu' or userChoice == 'option two' or userChoice == 'option tu' or userChoice == 'option to':
        login()
    else :
        speakIt("Sorry, Try again")
        MainMenu()
        return
        
speakIt("Hello Welcome to voice based Email System")
MainMenu()


