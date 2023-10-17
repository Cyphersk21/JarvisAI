import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
import datetime
from config import *
import requests

speaker = win32com.client.Dispatch("SAPI.SpVoice")
# engine = pyttsx3.init()

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = ChatGPT_apikey
    chatStr += f"Satish: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    try:
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except Exception as e:
        return say(f"Some Error Occurred. Sorry from Jarvis {e}")


def ai(prompt):
    openai.api_key = ChatGPT_apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    try:
        text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
        with open(f"Openai/{''.join(prompt.split('chatGPT')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        return say(f"Some Error Occurred. Sorry from Jarvis {e}")

def get_weather(api_key, city):
    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f'The weather in {city} is {description} with a temperature of {temperature}°C.'
    else:
        return 'Sorry, I couldn\'t fetch the weather data at the moment.'
        
def say(text):
    speaker.Speak(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognising.....")
            query = r.recognize_google(audio, language="en-in")
            query = query.lower()
            print(f"User said: {query}")
            return query

        except Exception as e:
            return f"Some Error Occurred. Sorry from Jarvis {e}"


if __name__ == '__main__':
    print("Pycharm")
    say("Hello I am JarvisAI")
    print("Listening.......")
    while True:
        query = takeCommand()
        sites = [["youtube", "https://youtube.com"], ["google", "https://google.com"],
                 ["instagram", "https://instagram.com"],
                 ["wikipedia", "https://wikipedia.com"], ["github", "https://github.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])

        if "Open Music".lower() in query.lower():
            say(f"Opening Music Sir...")
            musicPath = "https://jiosaavn.com"
            webbrowser.open(musicPath)

        elif "The Time".lower() in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strTime}")

        elif "Using chatGPT".lower() in query.lower():
            ai(prompt=query)

        elif "weather".lower() in query.lower():
            api_key = WeatherAPI
            city = query.split("in ")[-1]  # You can get the city from user input or other sources
            response = get_weather(api_key, city)
            print(f"Weather data {response}")
            say(response)

        elif "go offline".lower() in query.lower():
            say("Going offline sir....")
            exit()
        else:
            print("User: " + query)
            say(query)
            print("Jarvis: I'm not sure how to respond to that.")
            say("I'm not sure how to respond to that.")
        # say(query)
