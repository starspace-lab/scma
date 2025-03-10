import csv
import os
from datetime import datetime

DATABASE_FOLDER = "database"
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# create csv files
FILES = {
    "users": os.path.join(DATABASE_FOLDER, "users.csv"),
    "artifacts": os.path.join(DATABASE_FOLDER, "artifacts.csv"),
    "access_logs": os.path.join(DATABASE_FOLDER, "access_logs.csv"),
    "lyrics": os.path.join(DATABASE_FOLDER, "lyrics.csv"),
    "music_scores": os.path.join(DATABASE_FOLDER, "music_scores.csv"),
    "audio_recordings": os.path.join(DATABASE_FOLDER, "audio_recordings.csv"),
}


# headers for each CSV file
HEADERS = {
    "users": ["userID", "username", "email", "passwordHash", "role"],
    "artifacts": ["artifactID", "title", "type", "ownerID", "creationDate", "modificationDate", "checksum", "encryptionKey", "fileLocLyrics", "fileLocAudio"],
    "access_logs": ["logID", "userID", "artifactID", "accessType", "timeStamp"],
    "lyrics": ["lyricsID", "artifactID", "lyrics", "language"],
    "music_scores": ["scoreID", "artifactID", "score"],
    "audio_recordings": ["recordingID", "artifactID", "format", "duration"],
}

# initialize CSV files
def initialize_csv():
    for key, filename in FILES.items():
        if not os.path.exists(filename):  # Check if file exists
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(HEADERS[key])  # Write headers
            print(f"Created {filename}")

if __name__ == "__main__":
    initialize_csv()
    print("CSV files initialized successfully.")
