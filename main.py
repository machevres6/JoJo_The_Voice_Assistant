import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from bs4 import BeautifulSoup as bs
import requests

# Weather Requests:
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 " \
             "Safari/537.36 "
# US english
LANGUAGE = "en-US,en;q=0.5"


# Get Weather:
def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create new soup
    soup = bs(html.text, "html.parser")

    # store all results on this dictionary
    result = {'region': soup.find("h1", attrs={'class': "CurrentConditions--location--kyTeL"}).text,
              'temp_now': soup.find("span", attrs={"data-testid": "TemperatureValue"}).text,
              'weather_now': soup.find("div", attrs={"data-testid": "wxPhrase"}).text,
              'precipitation': soup.find("div", attrs={'data-testid': 'precipPhrase'}).text}

    return result


if __name__ == "__main__":
    URL = "https://weather.com/weather/today/l/22fb189f1a1607f5098f491c161838c404c7b10bb1359fd4203a0cf0cb3c17da"
    import argparse

    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather Data using The Weather Channel")

    # parse arguments
    args = parser.parse_args()
    # get data
    data = get_weather_data(URL)


# JoJo AI Assistant

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def create_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jojo' in command:
                command = command.replace('jojo', '')
    except:
        pass

    return command


def run_jojo():
    command = create_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'The current time is {time}')
        print(time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
    elif 'what is' in command:
        thing = command.replace('what is', '')
        info_1 = wikipedia.summary(thing, 2)
        print(info_1)
        talk(info_1)
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
    elif 'weather today' in command:
        location = data['region']
        temp = data['temp_now']
        current_weather = data['weather_now']
        precipitation = data['precipitation']

        talk(location)
        talk(f"The current temperature is: {temp}")
        talk(f"The sky looks: {current_weather}")
        talk(precipitation)

    else:
        talk('Please say that again.')


run_jojo()
