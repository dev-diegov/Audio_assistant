import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

spanish_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
english_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

# listen our mic and give back the audio as text
def transform_audio_in_text():
    # save recognizer in var
    r = sr.Recognizer()

    with sr.Microphone() as origin:
        # cooldown
        r.pause_threshold = 0.8
        print("You can talk")
        # save audio
        audio = r.listen(origin)

        try:
            # search in google
            order = r.recognize_google(audio, language="es-ar")
            # test
            print("You have said: " + order)
            return order

        # if it can't hear the audio
        except sr.UnknownValueError:
            print("Oooops, i didn't understand.")
            return "I keep waiting"

        # if order is damaged
        except sr.RequestError:
            print("Oooops, no service (order).")
            return "I keep waiting"

        # unenspected error
        except:
            print("Oooops, there's something wrong.")
            return "I keep waiting"

# the assistant can be heard
def talk(message):
    # turn on pyttsx3's engine
    engine = pyttsx3.init()
    engine.setProperty('voice', english_voice_id)

    # pronounce message
    engine.say(message)
    engine.runAndWait()

# notify and get day of the week
def get_day():
    day = datetime.date.today()
    print(day)

    day_week = day.weekday()
    print(day_week)

    # dict with days name
    calendar = {0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'}

    # say day of the week
    talk(f'Today is {calendar[day_week]}')

# function to get hour
def get_hour():
    hour = datetime.datetime.now()
    hour = f'In this moment its {hour.hour} hour with {hour.minute} minutes and {hour.second} seconds'
    print(hour)
    talk(hour)

def initial_greeting():
    hour = datetime.datetime.now()
    if hour.hour < 6 or hour.hour > 20:
        moment = 'Good night'
    elif 6 <= hour.hour < 13:
        moment = 'Good morning'
    else:
        moment = 'Good afternoon'

    talk(f'{moment}, I am Helena, your virtual assistant personal. Please, tell me what do you need?')

def ask_for_things():
    initial_greeting()

    start = True

    while start:
        # activate microphone and save the order in a string
        order = transform_audio_in_text().lower()

        if 'open youtube' in order:
            talk('Sure, i am opening youtube.')
            webbrowser.open('https://www.youtube.com')
            continue # keep loop
        elif 'open google chrome' in order:
            talk('Sure, i am opening google chrome.')
            webbrowser.open('https://www.google.com')
            continue
        elif 'what day is today?' in order:
            get_day()
            continue
        elif 'what hour is?' in order:
            get_hour()
            continue
        elif 'search in wikipedia' in order:
            talk('Searching it in wikipedia')
            order = order.replace('search in wikipedia', '').strip() # delete 'search in wikipedia' and extra spaces
            wikipedia.set_lang('en')

            try:
                result = wikipedia.summary(order, sentences=1)
                talk('Wikipedia says:')
                talk(result)
            except wikipedia.exceptions.PageError:
                talk("No information found in wikipedia.")
                continue
        elif 'search in internet' in order:
            talk('Okey, i will search')
            order = order.replace('search in internet', '')
            pywhatkit.search(order)
            talk('This is what i have found')
        elif 'reproduce' in order:
            talk('Good idea, i will reproduce it right now')
            pywhatkit.playonyt(order)
            continue
        elif 'joke' in order:
            talk(pyjokes.get_joke('en'))
            continue
        elif 'stock price' in order:
            stock = order.split('of')[-1].strip()
            wallet = {'apple':'APPL',
                      'amazon':'AMZN',
                      'google':'GOOGL'}

            try:
                stock_searched = wallet[stock]
                stock_searched = yf.Ticker(stock_searched)
                actual_price = stock_searched.info['regularMarketPrice']
                talk(f'I have found, the stock {stock} price is {actual_price}')
                continue
            except:
                talk('Sorry but i have not found it')
                continue
        elif 'goodbye' in order:
            talk('I am going to take a rest, if you need anything call me')
            break

# run program
ask_for_things()