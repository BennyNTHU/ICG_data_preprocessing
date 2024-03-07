import os
import numpy as np
import shutil
import librosa
import librosa.display
import soundfile as sf
import speech_recognition as sr
import speech_recognition as sr
import matplotlib.pyplot as plt
from tqdm import tqdm
from pydub import AudioSegment

# We need to do the following things to wash the dataset:
# (1) Remove the broken files
# (2) Change all the files to mono channel
# (3) Generate the scripts
# (4) Move the files to check directory for further human inspecting
# (5) Resample all the files to 16000Hz
# This file do (1) and (2)

icg_dataset_folder = "./data/ICG_dataset/"

# (1) Remove the broken files
for root, dirs, files in tqdm(os.walk(icg_dataset_folder)):
    for filename in files:
        if filename.endswith('.wav'):
            file_path = os.path.join(root, filename)
            try:
                y, sr = librosa.load(file_path)
            except:
                os.remove(file_path)

# (2) Change all the files to mono channel
for root, dirs, files in tqdm(os.walk(icg_dataset_folder)):
    for filename in files:
        if filename.endswith('.wav'):
            file_path = os.path.join(root, filename)
            try:
                audio_data = AudioSegment.from_wav(file_path)
                audio_data = audio_data.set_channels(1)
                audio_data.export(file_path, format="wav")            
            except:
                print("Cannot convert file " + file_path + " to mono")
