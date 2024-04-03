import pyaudio
import numpy as np
import soundfile as sf
import time
import os
from datetime import datetime
from statistics import mean


#Variable globale afin d'activer ou non l'écoute
stop_recording = False


def findpalier(FORMAT, CHANNELS, RATE, CHUNK):
    decib = []
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    start_time = time.time() #On récupère l'heure actuelle afin de chronometre
    while time.time() - start_time < 10: #On enregistre pendant 10sec
        print(time.time() - start_time)
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        dbmic = np.sqrt(np.mean(np.square(data)))
        print(dbmic)
        decib.append(dbmic)

    decib = [x for x in decib if not np.isnan(x) and not np.isinf(x)]

    moyenne = mean(decib)
    rounded = round(moyenne, 0)
    return rounded*2 #On rajoute le double des décibels captés pour être sûr d'éliminer les petits parasytes


#Fonction pour arrêter l'enregistrement
def stop_recording_function():
    global stop_recording
    stop_recording = True


def record_audio():
    filename_prefix = 'output'
    outputfold = 'audios'
    global stop_recording
    max_silence = 3
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # un seul micro
    RATE = 44100  # Fréquence d'échantillonnage pour bonne qualité d'enregistrement (en gros qualité CD)
    decibel_palier = findpalier(FORMAT, CHANNELS, RATE, CHUNK)  # Palier minimum afin de considérer comme un bruit viable et non parasyte
    print("Pallier de decibel : " + str(decibel_palier))
    p = pyaudio.PyAudio()

    try:
        while not stop_recording:
            #On lance l'écoute
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("En attente de bruit sonore...")

            frames = []
            is_recording = False
            silence_duration = 0

            while silence_duration <= max_silence:
                data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
                dbmic = np.sqrt(np.mean(np.square(data)))  # On récupère les décibels du micro comme ça

                if dbmic > decibel_palier and not is_recording: #On lance l'enregistrement si le son capté est au-dessus du pallier
                    print("Détection de bruit. Enregistrement en cours...")
                    is_recording = True
                    silence_duration = 0
                    print("2 - " + str(dbmic) + str(decibel_palier))

                if is_recording:
                    if dbmic < decibel_palier: #Si le son est en-dessous du palier
                        silence_duration += CHUNK / RATE  # Ajoute 1 seconde au compteur de silence
                    else:
                        silence_duration = 0

                    frames.extend(data)
                    print("3 - " + str(dbmic) + str(decibel_palier) + " - " + str(silence_duration))

            is_recording = False
            print("Arrêt de l'enregistrement...")

            now = datetime.now() #On prend l'heure pour nommer le fichier et si besoin pour plus tard

            opfile = os.path.join(outputfold, f'{filename_prefix}_{now.strftime("%H_%M_%S")}.wav')
            # Enregistrement du son
            sf.write(opfile, frames, RATE)
            frames = []  # On réinitialise

            # Pause de 1 seconde avant de recommencer
            time.sleep(1)

    except KeyboardInterrupt:
        print("Fermeture du programme")

    finally:
        p.terminate()


if __name__ == "__main__":
    try:
        record_audio()
    except KeyboardInterrupt:
        print("Fermeture du programme")

    finally:
        stop_recording_function()
