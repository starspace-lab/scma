import datetime
import random
import csv
import hashlib
import os
import pdfplumber
import secrets
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.mp4 import MP4 

database_folder = "database"
os.makedirs(database_folder, exist_ok=True)

# CSV File Paths
USERS_CSV = os.path.join(database_folder, "users.csv")
ARTIFACTS_CSV = os.path.join(database_folder, "artifacts.csv")
ACCESS_LOG_CSV = os.path.join(database_folder, "access_logs.csv")
LYRICS_CSV = os.path.join(database_folder, "lyrics.csv")
MUSIC_SCORE_CSV = os.path.join(database_folder, "music_scores.csv")
AUDIO_RECORDING_CSV = os.path.join(database_folder, "audio_recordings.csv")


def generate_id(csv_filename, id_column):
    existing_ids = set()

    # Read existing IDs from the CSV file
    try:
        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_ids = {row[id_column] for row in reader if row.get(id_column)}
    except FileNotFoundError:
        pass  # If file doesn't exist, assume no existing IDs

    # Generate a unique ID
    while True:
        new_id = str(secrets.randbelow(9000) + 1000)  # Generate a secure random number between 1000-9999
        if new_id not in existing_ids:
            return new_id

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generateChecksum(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Observer Pattern
def recordAccess(user_id, artifact_id, access_type, ACCESS_LOG_CSV):
    if not artifact_id:  # Skip logging if artifact_id is empty or None
        return
    log_id = generate_id(ACCESS_LOG_CSV, "logID")
    timestamp = get_timestamp()
    with open(ACCESS_LOG_CSV, "a", newline="") as f:
        csv.writer(f).writerow([log_id, user_id, artifact_id, access_type, timestamp])


# Extract lyrics, if no file given it will store empty string so user could modify it later
def extract_lyrics(file_path):
    """Extract lyrics from a given PDF file, allowing user to retry if file is missing."""
    while True:
        if not file_path.strip():  # If blank, return empty string
            return ""

        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext != ".pdf":
                print("Unsupported file format. Only PDF files are allowed!")
                file_path = input("Enter a valid PDF file path (or press Enter to skip): ").strip()
                continue

            return extract_text_from_pdf(file_path)

        print("File not found. Please enter a valid file path.")
        file_path = input("Enter a valid PDF file path (or press Enter to skip): ").strip()

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Extract audio metadata
def extractMetadataAudio(file_path):
    """Extract the format and duration of an audio file, allowing user to retry if file is missing."""
    while True:
        if not file_path.strip():  # If blank, return empty values
            return {"format": "", "duration": ""}

        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            try:
                if ext == ".mp3":
                    audio = MP3(file_path)
                elif ext == ".wav":
                    audio = WAVE(file_path)
                elif ext == ".flac":
                    audio = FLAC(file_path)
                elif ext in [".m4a", ".mp4", ".aac"]:
                    audio = MP4(file_path)
                else:
                    print("Unsupported file format. Supported: MP3, WAV, FLAC, M4A, AAC")
                    file_path = input("Enter a valid audio file path (or press Enter to skip): ").strip()
                    continue

                duration = round(audio.info.length, 2)  # Duration in seconds (rounded)
                return {"format": ext.replace(".", "").upper(), "duration": duration}

            except Exception as e:
                print(f"Error processing file: {e}")

        print("File not found. Please enter a valid file path.")
        file_path = input("Enter a valid audio file path (or press Enter to skip): ").strip()