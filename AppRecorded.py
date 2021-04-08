import speech_recognition as sr


def main():

    sound = "recordedaudio.wav"

    r = sr.Recognizer()

    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)

        print("Transcribing Audio File...")

        audio = r.listen(source)

        try:
            print("Converted Audio Is : \n " + r.recognize_google(audio))

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()