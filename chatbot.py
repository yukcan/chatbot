import selenium
from selenium import webdriver
import time
import speech_recognition as sr
import openai
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

openai.api_key = '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'

messages = [{"role":"system", "content":"You are a intelligent assistant."}]

def chatWithChatGPT(message):
	if message:
		messages.append({"role":"user","content": message})
		chat = openai.ChatCompletion.create(
			model="gpt-3.5-turbo", messages=messages )
	reply = chat.choices[0].message.content
	speak(reply)

r = sr.Recognizer()

def speak(read):
	print("ChatBot: ", read)
	tts = gTTS(text= read, lang="tr")
	file = "answer.mp3"
	tts.save(file)
	playsound(file)
	os.remove(file)

def record():
	print("Dinliyorum.")
	with sr.Microphone() as source:
		audio = r.listen(source)
		voice = ""
		try:
			voice = r.recognize_google(audio, language="tr")
			print("Siz: ", voice)
		except sr.UnknownValueError:
			print("Anlayamadım.")
			if wakeUp:
				speak("Anlayamadım.")
			record()
		except sr.RequestError:
			speak("Sistem çalışmıyor.")
		return voice

def playMusic(music):
	browser = webdriver.Firefox()
	url = "https://music.youtube.com/search?q=" + music
	browser.get(url)
	time.sleep(5)
	clickButton = browser.find_element("xpath",'/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-card-shelf-renderer/div/div[2]/div[1]/div/div[2]/div[2]/yt-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
	clickButton.click()


wakeUp = False
while True:
	voice = record()
	voice = voice.lower()
	if voice != "" and not(wakeUp):
		if "fişek" in voice:
			wakeUp = True
			speak("İnsan.")
	while wakeUp:
		voice = record()
		voice = voice.lower()
		if "fişek kapan" in voice:
			wakeUp = False
			speak("Kapandım insan.")
		elif "müzik oynat" in voice:
			speak("Hangi müziği oynatmamı istersin.")
			voice = record()
			playMusic(voice)
			speak("Youtube müzikden " + voice + " oynatılıyor.")
		elif voice != "":
			chatWithChatGPT(voice)

