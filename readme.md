# CLI Application

## Installation and Setup

### 1. Install Python

Ensure that Python is installed on your system. You can check by running:

```sh
python --version
```

or

```sh
python3 --version
```

If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

### 2. Create a Virtual Environment (Recommended)

To avoid conflicts with system-wide dependencies, create a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```
- On Windows:
  ```sh
  venv\Scripts\activate
  ```

### 3. Install Dependencies

This project has dependencies listed in the `requirements.txt` file. Install them using:

```sh
pip install -r requirements.txt
```

## Running the CLI Application

Before running the application, we should initiate the creation of database (CSV files) by running:

```sh
python database/makeCSV.py
```

Run the application with:

```sh
python main.py
```

## Tips on Using the App

- When navigating through the app, enter the abbreviation mentioned in brackets.
- When prompted to input data, you can skip it by pressing "Enter" directly.
- When entering file locations for audio or lyrics, provide the **exact path**:
  - **Windows:** `C:\Users\YourName\Documents\song_lyrics.pdf`
  - **Linux/macOS:** `/home/user/Documents/song_audio.mp3`

## Programming Paradigm

This project follows a **modular programming** paradigm due to its simplicity, flexibility, and efficiency. Unlike OOP, modular programming eliminates unnecessary overhead and allows for independent, testable functions. Since the project primarily handles **CSV files** and follows a **procedural workflow**, modular programming enhances maintainability and performance.

OOP would introduce unnecessary complexity unless features like persistent user sessions or database integration were required.

## Deviation from Original Design

Some aspects of the original design were adjusted for better functionality and efficiency:

1. **String-Based Encryption:**

   - Since data is stored in an **encrypted format**, all inputs are treated as strings to be processed by the encryption function. The encrypted output is also stored as a string.

2. **Excluded Functions:**
   Some functions were not implemented for the following reasons:

   - **`updateProfile()`** → Not essential for simulating the SCMA application; excluded for simplicity.
   - **`processAudio()`** → Audio metadata extraction is handled by `extractMetadata()`, making this function redundant.
   - **`convertFormat()`** → The project does not store audio files, so format conversion is unnecessary.
   - **`verifyChecksum()`** → Artifacts are stored in CSV files, not as physical files, making checksum verification irrelevant.
   - **`verifyTimestamp()`** → The system generates timestamps during record creation, eliminating the need for timestamp verification.

## Use of External Libraries

The external libraries used in this project is listed in requirements.txt which include:

1. cryptography -> For applying encryption-decryption to the data using Fernet.
2. pdfplumber -> To extract text in pdf file as an input for lyrics data.
3. mutagen -> To extract audio file as an input for format and duration data.

---
