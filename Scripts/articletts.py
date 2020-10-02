from os import system
from time import sleep

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound

another_article = ""
while another_article != "n":
    system("clear")
    url = input("Enter article url: ")
    page = requests.get(url).text
    soup = BeautifulSoup(page, features="lxml")

    title = soup.find("h1").get_text()

    p_tags = soup.find_all("p")
    p_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_text if not "\n" in sentence]
    sentence_list_final = [
        sentence for sentence in sentence_list if "." in sentence
    ]

    article_text = " ".join(sentence_list_final)

    tts = gTTS(article_text, lang="en")
    tts.save("article.mp3")
    playsound("article.mp3")

    another_article = input("Wold you like to play another article? [y/n]: ")
