import numpy as np
import wave
import matplotlib.pyplot as plt
from scipy.signal import correlate
from pydub import AudioSegment

# Fonction pour vérifier si un fichier est un fichier audio
# La fonction essaie d'ouvrir le fichier en tant que MP3 et retourne True s'il s'agit d'un fichier audio.
# Si une exception est levée, le fichier n'est pas considéré comme un fichier audio.
def is_audio(file_path):
    try:
        with mp3.open(file_path, 'r') as mp3:
            return True
    except Exception as e:
        return False

# Fonction pour convertir un fichier MP3 en fichier WAV temporaire
# Cela est nécessaire car le traitement audio se fait ici sur le format WAV
def convert_mp3_to_wav(mp3_file, wav_file):
    try:
        # Charger le fichier MP3
        audio = AudioSegment.from_mp3(mp3_file)
    except:
        return False
    # Exporter le fichier audio en format WAV
    audio.export(wav_file, format="wav")
    return True

# Fonction pour lire un fichier WAV et extraire les données audio et la fréquence d'échantillonnage
# La fonction ouvre le fichier WAV, extrait les canaux, la largeur des échantillons, et lit les trames audio.
def read_wav(file_path):
    with wave.open(file_path, 'r') as wav_file:
        n_channels = wav_file.getnchannels()  # Nombre de canaux (ex: mono ou stéréo)
        sample_width = wav_file.getsampwidth()  # Largeur de l'échantillon en octets
        framerate = wav_file.getframerate()  # Fréquence d'échantillonnage
        n_frames = wav_file.getnframes()  # Nombre de trames audio

        # Lire toutes les trames audio
        frames = wav_file.readframes(n_frames)
        
        # Déterminer le type de données en fonction de la largeur de l'échantillon
        if sample_width == 1:
            dtype = np.uint8  # 8 bits
        elif sample_width == 2:
            dtype = np.int16  # 16 bits
        else:
            raise ValueError("Le format audio n'est pas supporté")
        
        # Convertir les trames audio en tableau NumPy
        audio_data = np.frombuffer(frames, dtype=dtype)
        
        # Si audio stéréo, réduire en mono en faisant la moyenne des canaux
        if n_channels > 1:
            audio_data = audio_data.reshape(-1, n_channels).mean(axis=1)
        
        return audio_data, framerate

# Fonction pour calculer la corrélation croisée entre deux signaux audio
# La corrélation mesure la similitude entre deux signaux audio en fonction d'un décalage
def calculate_correlation(signal1, signal2):
    # Normaliser les signaux en soustrayant la moyenne et divisant par l'écart-type
    signal1 = (signal1 - np.mean(signal1)) / np.std(signal1)
    signal2 = (signal2 - np.mean(signal2)) / np.std(signal2)
    
    # Calculer la corrélation croisée avec un mode "full" pour toutes les positions de décalage
    correlation = correlate(signal1, signal2, mode='full')
    lags = np.arange(-len(signal1) + 1, len(signal2))  # Calcul des décalages associés
    return correlation, lags

# Fonction pour afficher la corrélation croisée
# Produit un graphique de la corrélation en fonction du décalage
def plot_correlation(correlation, lags):
    plt.figure(figsize=(10, 6))
    plt.plot(lags, correlation)
    plt.title('Corrélation croisée entre les deux fichiers audio')
    plt.xlabel('Décalage')
    plt.ylabel('Corrélation')
    plt.grid(True)
    plt.show()

# Chemins des fichiers audio (clés)
# Liste de clés audio pour lesquelles on souhaite vérifier la corrélation avec des échantillons
lst_cle = ['KeyA.mp3', 'KeyB.mp3', 'KeyC.mp3', 'KeyD.mp3']
lst_cle_temp_wav = ['KeyA.wav', 'KeyB.wav', 'KeyC.wav', 'KeyD.wav']
lst_audio_cle = {}  # Dictionnaire contenant les signaux audio (clé) et leurs fréquences d'échantillonnage

# Conversion de chaque clé MP3 en WAV
for i in lst_cle:
    convert_mp3_to_wav('labeled/' + i, 'labeled/' + i[:-3] + 'wav')

# Lecture des fichiers WAV et stockage des données audio
for i in lst_cle_temp_wav:
    signal, sr = read_wav('labeled/' + i)
    lst_audio_cle[i] = signal, sr

# Liste des fichiers audio étiquetés pour comparaison
lst_etiquete = ['sample1.mp3', 'sample2.mp3', 'sample3.mp3', 'sample4.mp3', ...]
lst_etiquete_temp_wav = ['sample1.wav', 'sample2.wav', 'sample3.wav', 'sample4.wav', ...]
lst_audio_etiquete = {}

# Conversion et vérification de chaque échantillon MP3 en WAV
for i in lst_etiquete:
    is_audio = convert_mp3_to_wav('unlabel/samples/' + i, 'unlabel/samples/' + i[:-3] + 'wav')
    if not is_audio:
        # Si la conversion échoue, retirer le fichier de la liste
        lst_etiquete_temp_wav.remove(i[:-3] + 'wav')

# Lecture des fichiers WAV convertis et stockage dans un dictionnaire
for i in lst_etiquete_temp_wav:
    signal, sr = read_wav('unlabel/samples/' + i)
    lst_audio_etiquete[i] = signal, sr

# Comparaison de chaque clé avec chaque échantillon pour identifier les correspondances
for i in lst_cle_temp_wav:
    for j in lst_etiquete_temp_wav:
        # Vérification de la compatibilité des fréquences d'échantillonnage
        if lst_audio_cle[i][1] != lst_audio_etiquete[j][1]:
            raise ValueError("Les fichiers audio doivent avoir la même fréquence d'échantillonnage.")
        else:
            # Calcul de la corrélation croisée
            correlation, lags = calculate_correlation(lst_audio_cle[i][0], lst_audio_etiquete[j][0])
            
            # Vérification des corrélations "parfaites" avec seuils 0.9 et -0.9
            if max(correlation) > 0.9 or min(correlation) < -0.9:
                print("Corrélation entre", i, "et", j)
                print(correlation)
                print(lags)
                
                # Enregistrement des corrélations et décalages significatifs dans un fichier
                with open('correlation.txt', 'a') as f:
                    f.write("Corrélation entre " + i + " et " + j + "\n")
                    f.write(str(correlation) + "\n")
            else:
                print("Mauvaise corrélation ?")

