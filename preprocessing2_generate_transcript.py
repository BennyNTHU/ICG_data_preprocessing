import os
import speech_recognition as sr
from tqdm import tqdm

# We need to do the following things to wash the dataset:
# (1) Remove the broken files
# (2) Change all the files to mono channel
# (3) Generate the scripts
# (4) Move the files to check directory for further human inspecting
# (5) Resample all the files to 16000Hz
# This file do (3). This usually takes a long time and need several times of running (may disconnect to google speech recognition API)

icg_dataset_folder = "./data/ICG_dataset/"
transcript_file_path = "./data/transcripts.txt"

# Generate the ASR file
def transcribe_audio_files(dataset_folder, transcript_file_path, max_file_size_mb=10):
    with open(transcript_file_path, 'a', encoding='utf-8') as transcript_file:
        transcript_file.write("File Name\tTranscript\n")

        for root, dirs, files in os.walk(icg_dataset_folder):
            print('Transcripting the subdirectory: ' + os.path.basename(root))
            for filename in tqdm(files):
                if filename.endswith('.wav'):
                    sub = os.path.basename(root) # subdirectory
                    file_path = os.path.join(root, filename)
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB

                    # If file is too large
                    if file_size_mb > max_file_size_mb:
                        transcript_file.write(f"{sub + '/' + filename}\t{'File too large'}\n")
                        continue

                    # conduct ASR
                    try:
                    	recognizer = sr.Recognizer()
                    	with sr.AudioFile(file_path) as audio_file:
                            try:
                                audio_data = recognizer.record(audio_file)
                                transcript = recognizer.recognize_google(audio_data, language='zh-tw', show_all=False)
                                if not transcript:
                                    transcript_file.write(f"{sub + '/' + filename}\t{'Need verification'}\n")
                                else:
                                    transcript_file.write(f"{sub + '/' + filename}\t{transcript}\n")
                            except sr.UnknownValueError:
                                transcript_file.write(f"{sub + '/' + filename}\t{'Could not understand'}\n")
                            except sr.RequestError as e:
                                transcript_file.write(f"{sub + '/' + filename}\t{'RequestError'}\n")
                            except:
                                transcript_file.write(f"{sub + '/' + filename}\t{'Need verification'}\n")
                    except:
                        transcript_file.write(f"{sub + '/' + filename}\t{'Could not open file'}\n")


transcribe_audio_files(icg_dataset_folder, transcript_file_path)

