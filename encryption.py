from cryptography.fernet import Fernet
import csv

# Strategy Pattern
def encrypt_data(encryption_key: str, data: str) -> str:
    f = Fernet(encryption_key)  # Convert key back to bytes
    encrypted_data = f.encrypt(data.encode())  # Encrypt string
    return encrypted_data.decode()  # Convert to a string for CSV storage

def decrypt_data(encryption_key: str, encrypted_data: str) -> str:
    try:
        f = Fernet(encryption_key.encode())  # Convert key to bytes
        return f.decrypt(encrypted_data.encode()).decode()  # Decrypt and return plaintext
    except Exception as e:
        return f"[Decryption Failed: {e}]"  # Return error message if decryption fails

def get_encryption_key(artifact_id, artifacts_csv):
    """Retrieve the encryption key for a given artifactID from ARTIFACTS_CSV."""
    with open(artifacts_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("artifactID") == artifact_id:
                return row.get("encryptionKey")  # Return the encryption key if found
    return None  # Return None if not found