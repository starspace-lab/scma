import os
import hashlib
import csv
from utils import get_timestamp, generate_id
from artifacts import viewArtifacts, addArtifact, modifyOwnArtifact, delete_artifact, display_csv_data

database_folder = "database"
os.makedirs(database_folder, exist_ok=True)

# CSV File Paths
USERS_CSV = os.path.join(database_folder, "users.csv")
ARTIFACTS_CSV = os.path.join(database_folder, "artifacts.csv")
ACCESS_LOG_CSV = os.path.join(database_folder, "access_logs.csv")
LYRICS_CSV = os.path.join(database_folder, "lyrics.csv")
MUSIC_SCORE_CSV = os.path.join(database_folder, "music_scores.csv")
AUDIO_RECORDING_CSV = os.path.join(database_folder, "audio_recordings.csv")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def recordAccess(user_id, artifact_id, access_type, ACCESS_LOG_CSV):
    if not artifact_id:  # Skip logging if artifact_id is empty or None
        return
    log_id = generate_id(ACCESS_LOG_CSV, "logID")
    timestamp = get_timestamp()
    with open(ACCESS_LOG_CSV, "a", newline="") as f:
        csv.writer(f).writerow([log_id, user_id, artifact_id, access_type, timestamp]) 

def username_exists(username, csv_filename):
    """Check if the username already exists in the CSV file."""
    try:
        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return any(row["username"].lower() == username.lower() for row in reader)
    except FileNotFoundError:
        return False  # If the file doesn't exist, no usernames exist yet

def register():
    username = input("Username: ").strip()
    # verify if the username availability
    if username_exists(username, USERS_CSV):
        print("Username already exists. Please choose a different one.")
        return

    email = input("Email: ").strip()
    password = input("Password: ").strip()
    role = input("Role (admin/creator/viewer): ").strip().lower()
    
    if role not in ["admin", "creator", "viewer"]:
        print("Invalid role.")
        return

    user_id = generate_id(USERS_CSV, "userID")
    password_hash = hash_password(password)

    with open(USERS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, email, password_hash, role])

    print("Registration successful!")

def login():
    username = input("Username: ")
    password = input("Password: ")
    password_hash = hash_password(password)

    with open(USERS_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            if len(row) >= 5 and row[1] == username and row[3] == password_hash:
                user_id = row[0]  # Extract userID
                role = row[4]  # Extract role
                print(f"Welcome, {username}!")
                user_dashboard(user_id, role)  # Pass userID and role
                return

    print("Invalid credentials.")

def user_dashboard(user_id, role):
    while True:
        print("\nDashboard")
        print("> View Artifacts (va)")
        if role in ["admin", "creator"]:
            print("> Add Artifact (aa)")
        if role == "creator":
            print("> Modify Artifact (ma)")
        if role == "admin":
            print("> Delete Artifact (da)")
            print("> Manage Users (mu)")
        print("> Logout (lo)")
        
        choice = input("Select an option: ").strip().lower()
        if choice == "va":
            viewArtifacts(user_id, role)
        elif choice == "aa" and role in ["admin", "creator"]:
            addArtifact(user_id)
        elif choice == "ma" and role == "creator":
            modifyOwnArtifact(user_id, role)
        elif choice == "mu" and role == "admin":
            manage_users(USERS_CSV)
        elif choice == "da" and role == "admin":
            display_csv_data(ARTIFACTS_CSV, USERS_CSV, role)
            delete_artifact(user_id, ARTIFACTS_CSV, AUDIO_RECORDING_CSV, LYRICS_CSV, MUSIC_SCORE_CSV)
        elif choice == "lo":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")

def manage_users(users_csv):
    """Displays users and prompts for user removal."""
    
    # Read and display users
    users = []
    with open(users_csv, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print(f"{'User ID':<10} | {'Username':<15} | {'Email':<25} | {'Role':<10}")
        print("-" * 65)

        for row in reader:
            users.append(row)
            print(f"{row['userID']:<10} | {row['username']:<15} | {row['email']:<25} | {row['role']:<10}")

    if not users:
        print("No users found.")
        return

    # Ask for user ID to remove
    user_id = input("\nEnter User ID to remove (leave blank to cancel): ").strip()

    if not user_id:  # If empty input
        print("No user ID entered. Operation cancelled.")
        return

    # Filter out the user
    updated_users = [row for row in users if row["userID"] != user_id]

    # Check if user was found
    if len(updated_users) == len(users):
        print(f"User ID {user_id} not found.")
        return

    # Write back the updated data
    with open(users_csv, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["userID", "username", "email", "passwordHash", "role"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_users)

    print(f"User ID {user_id} has been removed successfully.")