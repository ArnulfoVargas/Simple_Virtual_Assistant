import pyttsx4
import speech_recognition
import webbrowser
import pywhatkit
import yfinance
import pyjokes
import wikipedia
import datetime
from googletrans import Translator

engine = pyttsx4.init()
translator = Translator()


def transform_speech_to_text():
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.Microphone() as origin:
        recognizer.pause_threshold = .5
        print("ready")
        data = recognizer.listen(origin)

        try:
            request = recognizer.recognize_google(data, language = "es-mx")
            return request
        except speech_recognition.UnknownValueError:
            return " "
        except speech_recognition.RequestError:
            return " "
        except:
            return " "


def speak(text):
    global engine
    engine.say(text)
    engine.runAndWait()


def ask_for_day():
    global translator
    today = translator.translate( text=str(datetime.datetime.today().date().strftime("%A %d of %B of %Y")), dest= "es")
    return today.text


def ask_for_hour():
    c_hour = datetime.datetime.now()

    hour = c_hour.time().strftime('%I:%M %p')
    return hour


def greetings():
    hour = datetime.datetime.now()
    if hour.hour < 6 or hour.hour > 20:
        speak("Buenas noches, que puedo hacer hoy?")
    elif 6 <= hour.hour < 13:
        speak("Buenos dias, que puedo hacer por ti?")
    else:
        speak("Buenas tardes, que puedo hacer hoy por ti?")


def make_requests():
    greetings()

    global engine
    start = True

    open_synonyms = ['abre', 'abrir', 'abreme', 'abrirme', 'abres']
    search_synonyms = ['busca', 'buscame', 'encuentra', 'buscarme', 'buscar']
    yt_synonyms = [ 'reproduce', 'reproduceme', 'pon', 'reproducirme', 'reproducir']
    internet_synonyms = ['internet', 'google', 'navegador']

    while start:
        r = transform_speech_to_text().lower()
        engine.runAndWait()

        if 'adiós' in r or 'hasta luego' in r:
            speak("Adiós")
            start = False
        else:
            if 'día' in r or 'hoy' in r:
                speak("Hoy es " + ask_for_day())

            if 'hora' in r:
                speak("actualmente son las " + ask_for_hour())

            if 'broma' in r or 'chiste' in r:
                speak(pyjokes.get_joke('es'))

            for w in open_synonyms:
                if w in r:
                    if 'youtube' in r:
                        speak("Claro, abriendo YouTube")
                        webbrowser.open('https://www.youtube.com')
                        break
                    else:
                        for i in internet_synonyms:
                            if i in r:
                                speak("Claro, abriendo Google")
                                webbrowser.open('https://www.google.com')
                                break

            for w in search_synonyms:
                if w in r:
                    if 'wikipedia' in r:
                        search = r[r.index('wikipedia') + 10:]
                        wikipedia.set_lang('es')
                        result = wikipedia.summary(search, sentences = 1)
                        speak(result)
                        break

                    else:
                        for i in internet_synonyms:
                            if i in r:
                                search = r[r.index(i) + len(i)+1:]
                                pywhatkit.search(search)
                                speak("Aca esta tu busqueda")
                                break

            for w in yt_synonyms:
                if w in r:
                    search = r[r.index(w) + len(w)+1:]
                    pywhatkit.playonyt(search)
                    speak("Aca esta tu busqueda")
                    break
        engine.stop()


if __name__ == "__main__":
    make_requests()
