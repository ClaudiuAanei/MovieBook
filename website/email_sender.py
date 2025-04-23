import os
import smtplib
from random import choice, shuffle, randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText #
from dotenv import find_dotenv, load_dotenv

PATH = find_dotenv()
load_dotenv(PATH)

MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")

letters = list(chr(i) for i in range(ord('A'), ord('Z') + 1)) + list(chr(i) for i in range(ord('a'), ord('z') + 1))
numbers = list(str(i) for i in range(0, 10))

def generate_characters(char, num):
    return [choice(char) for _ in range(num)] if num > 0 else []

def generate_unique_code():
    password_list = (generate_characters(letters, randint(6,12)) +
                     generate_characters(numbers, randint(6,12)))

    shuffle(password_list)
    return "".join(password_list)

class Email:
    def __init__(self, name, mail, user_id, confirmation_code):
        self.name = name
        self.email = mail
        self.user_id = user_id
        self.confirmation_code = confirmation_code

    def create_email(self):
        with open("website/templates/confirmare.html", mode= 'r', encoding= "UTF-8") as file:
            text = file.read()
            new_mail = text.replace("[Nume solicitant]", self.name).replace(
                "[URL MOVIEBOOK]", f"{os.getenv('URL_CONFIRMARE')}{self.confirmation_code}&id={self.user_id}")
            return new_mail

    def send_email(self, mail_address):
        mail = self.create_email()
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user= MY_EMAIL, password= PASSWORD)
            msg = MIMEMultipart('alternative') # pentru format html
            html = MIMEText(mail, 'html') # pentru format html
            msg.attach(html) # pentru format html
            connection.sendmail(MY_EMAIL, mail_address, msg.as_string()) #msg.as_string()

