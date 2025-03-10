import csv
from cryptography.fernet import Fernet # type: ignore
from encryption import *
from utils import *
import os

database_folder = "database"
os.makedirs(database_folder, exist_ok=True)

# CSV File Paths
USERS_CSV = os.path.join(database_folder, "users.csv")
ARTIFACTS_CSV = os.path.join(database_folder, "artifacts.csv")
ACCESS_LOG_CSV = os.path.join(database_folder, "access_logs.csv")
LYRICS_CSV = os.path.join(database_folder, "lyrics.csv")
MUSIC_SCORE_CSV = os.path.join(database_folder, "music_scores.csv")
AUDIO_RECORDING_CSV = os.path.join(database_folder, "audio_recordings.csv")


def load_user_data(users_csv: str) -> dict:
    users = {}
    with open(users_csv, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["userID"]] = row["username"]  # Map userID to username
    return users

def display_csv_data(csv_filename: str, users_csv: str, role: str, owner_id: str = None):
    # Load user data to match ownerID -> username
    user_data = load_user_data(users_csv)

    with open(csv_filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Table header
        print(f"{'Artifact ID':<12} | {'Owner':<15} | {'Title (Decrypted)':<30}")
        print("-" * 65)

        for row in reader:
            if role == "creator" and row["ownerID"] != owner_id:
                continue  # Skip records that don't match ownerID

            decrypted_title = decrypt_data(row["encryptionKey"], row["title"])
            creator_name = user_data.get(row["ownerID"], "Unknown")  # Get creator name

            print(f"{row['artifactID']:<12} | {creator_name:<15} | {decrypted_title:<30}")

def display_all_data(artifact_id, role, owner_id):
    csv_files = [ARTIFACTS_CSV, USERS_CSV, LYRICS_CSV, MUSIC_SCORE_CSV, AUDIO_RECORDING_CSV]
    artifact_data = {"artifactID": artifact_id}  # Start with the ID
    displayed_data = ["title", "type", "lyrics", "language", "score", "format", "duration"]

    # Get the encryption key and ownerID from ARTIFACTS_CSV
    artifact_owner_id = None
    encryption_key = None

    with open(ARTIFACTS_CSV, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["artifactID"] == artifact_id:
                artifact_owner_id = row["ownerID"]
                encryption_key = row["encryptionKey"]
                break  # Stop searching once found

    # If no encryption key is found, the artifact doesn't exist
    if encryption_key is None:
        print("Artifact not found.")
        return

    # If user is a creator, ensure they own the artifact
    if role == "creator" and artifact_owner_id != owner_id:
        print("Invalid artifact. You do not have permission to access this artifact.")
        return

    # Proceed to collect artifact data
    for csv_filename in csv_files:
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("artifactID") == artifact_id:
                    for key, value in row.items():
                        if key in displayed_data:  # Only collect displayed fields
                            artifact_data[key] = decrypt_data(encryption_key, value)

    # Display the artifact data if found
    if len(artifact_data) > 1:
        print("\nArtifact Data Found:")
        for key, value in artifact_data.items():
            print(f"{key}: {value}")
    else:
        print("\nArtifact not found.")

def get_artifact_data(artifact_id):
    """Fetches all related artifact data."""
    artifact = lyrics = music_score = audio_recording = None

    # Read artifacts.csv
    with open(ARTIFACTS_CSV, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["artifactID"] == artifact_id:
                artifact = row
                break

    # Read lyrics.csv
    with open(LYRICS_CSV, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["artifactID"] == artifact_id:
                lyrics = row
                break

    # Read music_score.csv
    with open(MUSIC_SCORE_CSV, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["artifactID"] == artifact_id:
                music_score = row
                break

    # Read audio_recording.csv
    with open(AUDIO_RECORDING_CSV, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["artifactID"] == artifact_id:
                audio_recording = row
                break

    return artifact, lyrics, music_score, audio_recording

# Factory Pattern
def addArtifact(user_id):
    encryption_key = Fernet.generate_key().decode()
    # data input + encryption
    title = encrypt_data(encryption_key, input("Title: "))
    type_ = encrypt_data(encryption_key, input("Type: "))
    artifact_id = generate_id(ARTIFACTS_CSV, "artifactID")
    creation_date = modification_date = get_timestamp()
    file_loc_lyrics = encrypt_data(encryption_key, input("Lyrics File Location (Enter file exact path): "))
    checksum = generateChecksum(decrypt_data(encryption_key, title) + decrypt_data(encryption_key, type_))
    lyrics_data = extract_lyrics(decrypt_data(encryption_key, file_loc_lyrics))
    lyrics = encrypt_data(encryption_key, lyrics_data)
    language = encrypt_data(encryption_key, input("Language: "))
    score = encrypt_data(encryption_key, input("Score: "))
    file_loc_audio = encrypt_data(encryption_key, input("Audio File Location (Enter file exact path): "))
    audio_data = extractMetadataAudio(decrypt_data(encryption_key, file_loc_audio))
    audio_format = encrypt_data(encryption_key, audio_data["format"])
    duration = encrypt_data(encryption_key, str(audio_data["duration"]))
    
    # save data
    with open(ARTIFACTS_CSV, "a", newline="") as f:
        csv.writer(f).writerow([artifact_id, title, type_, user_id, creation_date, modification_date, checksum, encryption_key, file_loc_lyrics, file_loc_audio])
    with open(LYRICS_CSV, "a", newline="") as f:
        csv.writer(f).writerow([generate_id(LYRICS_CSV, "lyricsID"), artifact_id, lyrics, language])
    with open(MUSIC_SCORE_CSV, "a", newline="") as f:
        csv.writer(f).writerow([generate_id(MUSIC_SCORE_CSV, "scoreID"), artifact_id, score])
    with open(AUDIO_RECORDING_CSV, "a", newline="")as f:
        csv.writer(f).writerow([generate_id(AUDIO_RECORDING_CSV, "recordingID"), artifact_id, audio_format, duration])
    
    recordAccess(user_id, artifact_id, "Add Artifact", ACCESS_LOG_CSV) # access log
    print("Artifact added successfully!")

def viewArtifacts(user_id, role):
    if role == "creator": # ensuring creator could only access their own artifacts
        display_csv_data("database/artifacts.csv", "database/users.csv", role, owner_id = user_id)
        artifact_id = input("Enter the artifact ID you want to view: ").strip()
        recordAccess(user_id, artifact_id, "View Artifact", ACCESS_LOG_CSV) # access log
        display_all_data(artifact_id, role, owner_id=user_id)
    else:
        display_csv_data("database/artifacts.csv", "database/users.csv", role)
        artifact_id = input("Enter the artifact ID you want to view: ").strip()
        recordAccess(user_id, artifact_id, "View Artifact", ACCESS_LOG_CSV) # access log
        display_all_data(artifact_id, role, owner_id=user_id)

def modifyOwnArtifact(user_id, role):
    # Display artifacts before modification
    if role == "creator": # ensuring creator could only access their own artifacts
        display_csv_data(ARTIFACTS_CSV, USERS_CSV, role, owner_id=user_id)
    else:
        display_csv_data(ARTIFACTS_CSV, USERS_CSV, role)

    # Ask for artifact ID
    artifact_id = input("Enter the artifact ID you want to modify: ").strip()
    display_all_data(artifact_id, role, owner_id=user_id)
    artifact, lyrics, music_score, audio_recording = get_artifact_data(artifact_id)

    if not artifact:
        print("Error: Artifact ID not found.")
        return

    # Extract encryption key
    encryption_key = get_encryption_key(artifact_id, ARTIFACTS_CSV)

    # Ask for new values, allowing blank value to keep old ones
    new_title = input("Enter new title (leave blank to keep previous data): ").strip()
    new_type = input("Enter new type (leave blank to keep previous data): ").strip()

    new_lyrics_path = input("Enter new lyrics exact file path (leave blank to keep previous data): ").strip() if lyrics else None
    new_lyrics = extract_lyrics(new_lyrics_path)
    new_language = input("Enter new language (leave blank to keep previous data): ").strip() if lyrics else None

    new_score = input("Enter new score (leave blank to keep previous data): ").strip() if music_score else None

    new_audio_path = input("Enter new audio exact file path (leave blank to keep previous data): ").strip() if audio_recording else None
    new_audio = extractMetadataAudio(new_audio_path)

    # Update artifact data
    artifact["title"] = encrypt_data(encryption_key, new_title) if new_title else artifact["title"]
    artifact["type"] = encrypt_data(encryption_key, new_type) if new_type else artifact["type"]
    artifact["modificationDate"] = get_timestamp()
    artifact["fileLocLyrics"] = encrypt_data(encryption_key, new_lyrics_path) if new_lyrics_path else artifact["fileLocLyrics"]
    artifact["fileLocAudio"] = encrypt_data(encryption_key, new_audio_path) if new_audio_path else artifact["fileLocAudio"]

    if lyrics:
        lyrics["lyrics"] = encrypt_data(encryption_key, new_lyrics) if new_lyrics_path else lyrics["lyrics"]
        lyrics["language"] = encrypt_data(encryption_key, new_language) if new_language else lyrics["language"]

    if music_score:
        music_score["score"] = encrypt_data(encryption_key, new_score) if new_score else music_score["score"]

    if audio_recording:
        audio_recording["format"] = encrypt_data(encryption_key, new_audio["format"]) if new_audio_path else audio_recording["format"]
        audio_recording["duration"] = encrypt_data(encryption_key, str(new_audio["duration"])) if new_audio_path else audio_recording["duration"]


    # Save the updated records back to the CSV files
    def update_csv(file_path, data, key_column):
        """Updates a CSV file with modified data."""
        rows = []
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row[key_column] == artifact_id:
                    rows.append(data)
                else:
                    rows.append(row)

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    update_csv(ARTIFACTS_CSV, artifact, "artifactID")
    if lyrics:
        update_csv(LYRICS_CSV, lyrics, "artifactID")
    if music_score:
        update_csv(MUSIC_SCORE_CSV, music_score, "artifactID")
    if audio_recording:
        update_csv(AUDIO_RECORDING_CSV, audio_recording, "artifactID")

    recordAccess(user_id, artifact_id, "Modify Artifact", ACCESS_LOG_CSV) # access log
    print("Artifact updated successfully!")

def delete_artifact(user_id, ARTIFACTS_CSV, AUDIO_RECORDING_CSV, LYRICS_CSV, MUSIC_SCORE_CSV):

    """Deletes an artifact and its related data from all sources."""
    
    artifact_id = input("\nEnter Artifact ID to remove (leave blank to cancel): ").strip()
    
    if not artifact_id:  # If empty input
        print("No artifact id entered. Operation cancelled.")    
    
    def remove_entry(csv_file, key, value):
        """Helper function to remove entries matching a key-value pair in a CSV file."""
        updated_data = []
        found = False
        
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        
        for row in data:
            if row[key] == value:
                found = True  # Mark that we found and removed the entry
            else:
                updated_data.append(row)
        
        if found:
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(updated_data)
        
        return found

    # Delete artifact from all sources
    artifact_deleted = remove_entry(ARTIFACTS_CSV, "artifactID", artifact_id)
    audio_deleted = remove_entry(AUDIO_RECORDING_CSV, "artifactID", artifact_id)
    lyrics_deleted = remove_entry(LYRICS_CSV, "artifactID", artifact_id)
    score_deleted = remove_entry(MUSIC_SCORE_CSV, "artifactID", artifact_id)

    recordAccess(user_id, artifact_id, "Delete Artifact", ACCESS_LOG_CSV) # access log
    # Check if anything was deleted
    if artifact_deleted or audio_deleted or lyrics_deleted or score_deleted:
        print(f"Artifact ID {artifact_id} and related data have been removed.")
    else:
        print(f"Artifact ID {artifact_id} not found.")