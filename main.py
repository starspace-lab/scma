import os
from auth import register, login

database_folder = "database"
os.makedirs(database_folder, exist_ok=True)

# CSV File Paths
USERS_CSV = os.path.join(database_folder, "users.csv")
ARTIFACTS_CSV = os.path.join(database_folder, "artifacts.csv")
ACCESS_LOG_CSV = os.path.join(database_folder, "access_logs.csv")
LYRICS_CSV = os.path.join(database_folder, "lyrics.csv")
MUSIC_SCORE_CSV = os.path.join(database_folder, "music_scores.csv")
AUDIO_RECORDING_CSV = os.path.join(database_folder, "audio_recordings.csv")

def main():
    while True:
        print("\nWelcome to SCMA Application")
        print("> Register (re)\n> Login (lo)\n> Exit (ex)")
        choice = input("Select an option: ").strip().lower()
        if choice == "re":
            register()
        elif choice == "lo":
            login()
        elif choice == "ex":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()