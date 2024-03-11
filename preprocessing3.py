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
# This script do (4) and (5)

# (4) Move the files to check directory for further human inspecting
dataset_folder = "./data/" # 有些檔案已經被一到待處理區了
icg_dataset_folder = "./data/ICG_dataset/"
transcript_file_path = "./data/transcripts.txt"

def get_destination_folder(transcript):
    if transcript == 'File too large':
        return "./data/check/File_too_large"
    elif transcript == 'Need verification':
        return "./data/check/Need_verification"
    elif transcript == 'Could not understand':
        return "./data/check/Could_not_understand"
    elif transcript == 'Could not open file':
        return "./data/check/Could_not_open_file"
    else:
        return None  # Skip files with other transcripts

def move_files_based_on_transcript(transcript_file_path):
    with open(transcript_file_path, 'r', encoding='utf-8') as transcript_file:
        next(transcript_file)  # Skip header
        for line in tqdm(transcript_file):
            parts = line.strip().split('\t', 1) 
            file_name, transcript = parts # Obtain file name
            subdirectory = os.path.dirname(file_name) # original subdirectory
            adjusted_file_name = os.path.basename(file_name) # the file name dropping subdirectory's path
            destination_folder = get_destination_folder(transcript)

            if destination_folder: # Not None
            	original_path = os.path.join(icg_dataset_folder, file_name)
            	destination_path = os.path.join(destination_folder, adjusted_file_name)
            	shutil.move(original_path, destination_path) # move the file to the destination_folder

move_files_based_on_transcript(transcript_file_path)

# (5) Resample all the files to 16000Hz
for root, dirs, files in tqdm(os.walk(dataset_folder)):
    for filename in files:
        if filename.endswith('.wav'):
            file_path = os.path.join(root, filename)
            try:
                audio, sr = librosa.load(file_path, sr=None) # Load audio file
                audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=16000)
                sf.write(file_path, audio_resampled, 16000) # Save the resampled audio to a new file
            except:
                destination_path = os.path.join(destination_folder, filename) # new path of the file
                shutil.move(file_path, destination_path) # move the file to the destination_folder
