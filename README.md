# ⌨️ Typing Speed Tester

A simple typing speed tester built with **Python (Tkinter)** and **MySQL**.
Started as a small project to practice GUI + database stuff, ended up becoming a full typing app with stats, levels, and a leaderboard.

---

## 🚀 What it does

* Test your typing speed (**WPM**) and **accuracy**
* Multiple difficulty modes: **easy / medium / hard / mixed**
* Practice mode that runs continuously
* Level mode with increasing difficulty
* Save scores (when logged in)
* View **stats**, **history**, and **leaderboard**

---

## ✨ Features

### 🧪 Practice Mode

Pick a difficulty and start typing.
The app automatically gives you new sentences after each test.

---

### 🎯 Level Mode

* Starts easy → gradually becomes harder
* Total **7 levels**
* Countdown before each level starts

---

### ⚡ Live Feedback

* ✅ Correct letters → **green**
* ❌ Wrong letters → **red**
* 📊 Progress bar while typing
* ⌨️ On-screen keyboard highlights key presses

---

### 📊 Stats & History

* Average WPM
* Average accuracy
* Best WPM
* Total tests taken

---

### 🏆 Leaderboard

* Top 10 users ranked by highest WPM
* Stored using MySQL database

---

## 🛠️ Tech Stack

* **Python**
* **Tkinter**
* **MySQL**
* **mysql-connector-python**

---

## ⚙️ Setup

### 1. Clone the repository

```bash id="a1b2c3"
git clone https://github.com/thesm_saif/typing_speed_tester.git
cd typing-tester-pro
```

---

### 2. Install dependency

```bash id="d4e5f6"
pip install mysql-connector-python
```

---

### 3. Setup MySQL database

Run the following in MySQL:

```sql id="g7h8i9"
CREATE DATABASE typing_app;

USE typing_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    wpm INT,
    accuracy INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

### 4. Update database credentials

In your Python file, change this:

```python id="j1k2l3"
password = "YOUR_PASSWORD"
```

---

### 5. Run the app

```bash id="m4n5o6"
python main.py
```

---

## 📝 Notes

* Passwords are stored as plain text (not secure, just for learning)
* This is a **project app**, not production-ready

---

## 💡 Future Improvements

* Add password hashing
* Improve UI design
* Add timer-based mode
* Multiplayer typing mode
* Sound effects

---

## 🤔 Why I built this

Wanted to build something that combines:

* GUI
* real-time interaction
* database

Typing tester felt like a good mix of all three.

---

## 👍 That's it

If you like it, feel free to fork or improve it.
