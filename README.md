# Password Cracking Application

> **Cyber Security Mini Project**  
> Made by **Samridhi**

A GUI-based password cracking application built with Python and Tkinter, powered by **John the Ripper** - one of the most widely used open-source password security auditing tools.

---


## About the Project

This project is a **GUI wrapper** around John the Ripper - a powerful command-line password cracking tool. Instead of requiring users to type commands in a terminal, this application provides a clean and intuitive graphical interface where users can:

- Upload a file containing hashed passwords
- Crack the hashes using John the Ripper in the background
- See the recovered plaintext password instantly in the UI

This project demonstrates the integration of a cybersecurity tool into a Python desktop application, and covers concepts like **hash cracking**, **subprocess execution**, **multi-threading**, and **GUI development**.

---

## Features

| Feature | Description |
|---|---|
|  File Browser | Browse and select hash files from your system |
|  Drag & Drop | Drag a `.txt` hash file directly onto the app |
|  Clear File | Remove the loaded file with one click |
|  One-Click Cracking | Start cracking with a single button press |
|  Instant Result Box | Cracked password displayed in large, highlighted text with a blinking alert |
|  Copy Logs | Copy the full technical log output to clipboard |
|  Console Output | Detailed session logs in the Step 3 console |
|  Status Bar | Live status messages at the bottom of the window |
|  Custom Theme | Deep indigo + electric violet + amber colour palette |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| GUI Framework | Tkinter (built-in) |
| Drag & Drop | tkinterdnd2 |
| Password Cracker | John the Ripper v1.9.0-jumbo-1 |
| Execution | Python `subprocess` module |
| Threading | Python `threading` module |

---

## Prerequisites

Before running this project, make sure the following are installed and set up:

### 1. Python 3.x
Download from: https://www.python.org/downloads/

>  During installation, tick **"Add Python to PATH"**

Verify installation:
```bash
python --version
```

### 2. tkinterdnd2 (Drag & Drop support)
```bash
pip install tkinterdnd2
```

### 3. John the Ripper (Jumbo version)
Download from: https://www.openwall.com/john/

- Download: `1.9.0-jumbo-1 64-bit Windows binaries (zip)`
- Extract the ZIP
- Navigate to the `run/` folder inside — this contains `john.exe`

>  **Important:** The path to `john.exe` is hardcoded in the application. See [Setup](#setup--installation) for details.

---

##  Project Structure

```
john_project/
│
├── john_gui.py             ← Main application (GUI)
├── README.md               ← This file
│
# John the Ripper (kept separately in Downloads)
└── john-1.9.0-jumbo-1-win64/
    └── john-1.9.0-jumbo-1-win64/
        └── run/
            ├── john.exe    ← The cracking engine
            ├── test.txt    ← Sample hash file (you create this)
            ├── password.lst← Default wordlist
            └── john.pot    ← Auto-created: stores cracked passwords
```

---

##  Setup & Installation

### Step 1: Clone or download the project
Place `john_gui.py` in a folder (e.g. `Desktop/john_project/`).

### Step 2: Install the dependency
```bash
pip install tkinterdnd2
```

### Step 3: Verify the John the Ripper path
Open `john_gui.py` and check this line near the top:

```python
JOHN_EXE = r"C:\Users\SAMRIDHI\Downloads\john-1.9.0-jumbo-1-win64\john-1.9.0-jumbo-1-win64\run\john.exe"
```

Update it to match the actual path of `john.exe` on your system.

### Step 4: Run the application
```bash
python john_gui.py
```

---

##  How to Use

The interface is divided into **3 simple steps**:

```
STEP 1 — SELECT A HASH FILE
  → Drag & drop a .txt file onto the drop zone
  → OR click "Browse File" to select it
  → Click "✕ Clear File" to remove it

STEP 2 — CRACK THE PASSWORD
  → Click "Crack Password ▸"
  → Wait a few seconds

STEP 3 — VIEW RESULTS
  → The cracked password appears in the result box above with a blinking red alert
  → Full technical log is shown in the console below
  → Click "📋 Copy Logs" to copy the log output
```

---

## How It Works

```
User selects a hash file
        ↓
App calls john.exe with --format=Raw-MD5
        ↓
John tries passwords from its built-in wordlist
        ↓
App calls john.exe --show to retrieve result
        ↓
Cracked password displayed in the GUI
```

The application uses Python's `subprocess` module to invoke John the Ripper as a background process and captures its output to display in the interface. Cracking runs on a **background thread** so the UI stays fully responsive.

---

## Sample Test File

To test the application, create a file called `test.txt` containing this MD5 hash:

```
5f4dcc3b5aa765d61d8327deb882cf99
```

This is the MD5 hash of the word: `password`

After cracking, the result box should show:
```
password
```

---

## Disclaimer

> This project is built **strictly for educational purposes** as part of a Cyber Security course assignment.  
> It is intended to demonstrate how password hashing and dictionary-based cracking work conceptually.  
> **Do NOT use this tool on any system, account, or file you do not own or have explicit permission to test.**  
> The developer holds no responsibility for any misuse of this software.

---

## Concepts Demonstrated

- Password hashing (MD5 and others)
- Dictionary-based password cracking
- GUI development using Tkinter
- Subprocess execution from Python
- Multi-threading in desktop applications
- Integration of command-line security tools into a GUI

---

*Cyber Security Mini Project | Made by Samridhi*
