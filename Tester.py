import tkinter as tk
import random
import time
import mysql.connector
import re

# -------- DATABASE -------- #
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kannekt123#",
    database="typing_app"
)
cursor = db.cursor()

# -------- WORDS -------- #
easy_words = ["cat","dog","sun","sky","food","play","run","blue","red","fast"]
medium_words = ["python","coding","practice","logic","system","typing","program","learn"]
hard_words = ["consistency","discipline","development","performance","optimization"]

def gen(words,n): return " ".join(random.choice(words) for _ in range(n))
def med(s): return " ".join(w.capitalize() if random.random()<0.3 else w for w in s.split())
def hard(s): return "".join(c.upper() if random.random()<0.5 else c.lower() for c in s)

def get_sentence(mode):
    if mode=="easy": return gen(easy_words, random.randint(3,6))
    elif mode=="medium": return med(gen(medium_words, random.randint(5,8)))
    else: return hard(gen(hard_words, random.randint(6,10)))

# -------- APP -------- #
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Tester Pro")
        self.root.geometry("900x600")
        self.root.config(bg="#121212")

        self.history = []
        self.current_user = None
        self.practice_running = False

        self.login_screen()  # ✅ FIXED

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def center(self):
        f = tk.Frame(self.root, bg="#121212")
        f.place(relx=0.5, rely=0.5, anchor="center")
        return f

# -------- LOGIN -------- #
    def login_screen(self):
        self.clear()
        f = self.center()

        tk.Label(f, text="Login", font=("Segoe UI", 20),
                 fg="white", bg="#121212").pack(pady=10)

        self.username = tk.Entry(f)
        self.username.pack()

        self.password = tk.Entry(f, show="*")
        self.password.pack()

        tk.Button(f, text="Login", command=self.login).pack(pady=5)
        tk.Button(f, text="Sign Up", command=self.signup_screen).pack(pady=5)
        tk.Button(f, text="Continue Without Login", command=self.menu).pack(pady=5)

    def login(self):
        user = self.username.get().lower()
        pwd = self.password.get()

        cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s",(user,pwd))
        res = cursor.fetchone()

        if res:
            self.current_user = res[0]
            self.menu()
        else:
            tk.Label(self.root, text="Invalid Login", fg="red", bg="#121212").pack()

# -------- SIGNUP -------- #
    def signup_screen(self):
        self.clear()
        f = self.center()

        tk.Label(f, text="Sign Up", fg="white", bg="#121212").pack()

        self.new_user = tk.Entry(f)
        self.new_user.pack()

        self.new_pass = tk.Entry(f, show="*")
        self.new_pass.pack()

        self.email = tk.Entry(f)
        self.email.pack()

        tk.Button(f, text="Create Account", command=self.signup).pack()

    def valid_username(self, u):
        return re.match(r'^[a-zA-Z0-9._-]+$', u)

    def valid_email(self, e):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', e)

    def signup(self):
        u = self.new_user.get().lower()
        p = self.new_pass.get()
        e = self.email.get()

        if not self.valid_username(u):
            tk.Label(self.root, text="Invalid Username").pack()
            return

        if not self.valid_email(e):
            tk.Label(self.root, text="Invalid Email").pack()
            return

        try:
            cursor.execute("INSERT INTO users(username,password,email) VALUES(%s,%s,%s)",(u,p,e))
            db.commit()
            tk.Label(self.root, text="Account Created").pack()
            self.login_screen()
        except:
            tk.Label(self.root, text="Username Exists").pack()

# -------- MENU -------- #
    def menu(self):
        self.clear()
        f = self.center()

        tk.Label(f, text="Typing Tester Pro", font=("Segoe UI", 28),
                 fg="white", bg="#121212").pack(pady=20)

        tk.Button(f, text="Practice", command=self.practice_menu, width=20).pack(pady=5)
        tk.Button(f, text="Level Mode", command=self.start_levels, width=20).pack(pady=5)
        tk.Button(f, text="History", command=self.show_history, width=20).pack(pady=5)
        tk.Button(f, text="Stats", command=self.show_stats, width=20).pack(pady=5)
        tk.Button(f, text="Leaderboard", command=self.leaderboard, width=20).pack(pady=5)
        tk.Button(f, text="Exit", command=self.root.destroy, width=20).pack(pady=5)

# -------- SAVE SCORE -------- #
    def save_score(self, wpm, acc):
        if self.current_user:
            cursor.execute("INSERT INTO scores(user_id,wpm,accuracy) VALUES(%s,%s,%s)",
                           (self.current_user,wpm,acc))
            db.commit()

# -------- LEADERBOARD -------- #
    def leaderboard(self):
        self.clear()
        f = self.center()

        tk.Label(f, text="Leaderboard", fg="white", bg="#121212").pack()

        cursor.execute("""
        SELECT users.username, MAX(scores.wpm)
        FROM scores
        JOIN users ON users.id = scores.user_id
        GROUP BY users.username
        ORDER BY MAX(scores.wpm) DESC
        LIMIT 10
        """)

        for row in cursor.fetchall():
            tk.Label(f, text=f"{row[0]} - {row[1]} WPM",
                     fg="white", bg="#121212").pack()

        tk.Button(f, text="Back", command=self.menu).pack()

# -------- PRACTICE -------- #
    def practice_menu(self):
        self.clear()
        f = self.center()

        tk.Label(f, text="Practice Mode", fg="white", bg="#121212").pack(pady=10)

        tk.Button(f, text="Mixed", command=lambda: self.start_practice("mixed")).pack()
        tk.Button(f, text="Easy", command=lambda: self.start_practice("easy")).pack()
        tk.Button(f, text="Medium", command=lambda: self.start_practice("medium")).pack()
        tk.Button(f, text="Hard", command=lambda: self.start_practice("hard")).pack()

        tk.Button(f, text="Back", command=self.menu).pack(pady=10)

    def start_practice(self, mode):
        self.practice_running = True
        self.run_test(mode, practice=True)

# -------- LEVEL MODE -------- #
    def start_levels(self):
        self.level = 1
        self.scores = []
        self.next_level()

    def next_level(self):
        if self.level > 7:
            self.menu()
            return

        if self.level <= 2: mode="easy"
        elif self.level <= 5: mode="medium"
        else: mode="hard"

        self.countdown(lambda: self.run_test(mode, level=True))

    def countdown(self, callback):
        self.clear()
        f = self.center()
        label = tk.Label(f, font=("Segoe UI", 50), fg="white", bg="#121212")
        label.pack()

        def count(n):
            if n == 0:
                label.config(text="GO!")
                self.root.after(500, callback)
            else:
                label.config(text=str(n))
                self.root.after(1000, lambda: count(n-1))

        count(3)

# -------- TEST -------- #
    def run_test(self, mode, practice=False, level=False):
        self.clear()
        f = self.center()

        if mode == "mixed":
            mode = random.choice(["easy","medium","hard"])

        self.sentence = get_sentence(mode)

        self.display = tk.Text(f, height=3, width=60,
                               font=("Consolas", 16),
                               bg="#121212", fg="white", bd=0)
        self.display.pack()

        self.display.insert("1.0", self.sentence)
        self.display.config(state="disabled")

        self.entry = tk.Entry(f, font=("Consolas", 16), width=50)
        self.entry.pack(pady=10)

        self.entry.bind("<KeyRelease>", self.live_color)
        self.entry.bind("<KeyPress>", self.highlight_key)
        self.entry.bind("<Return>", lambda e: self.finish_test(practice, level))

        self.start_time = time.time()

        self.result = tk.Label(f, fg="yellow", bg="#121212")
        self.result.pack()

        self.progress = tk.Canvas(f, width=400, height=10, bg="gray")
        self.progress.pack(pady=5)

        self.draw_keyboard(f)

        tk.Button(f, text="Back", command=self.menu).pack()

    def live_color(self, e=None):
        typed = self.entry.get()

        self.display.config(state="normal")
        self.display.delete("1.0", tk.END)

        for i, ch in enumerate(self.sentence):
            if i < len(typed):
                if typed[i] == ch:
                    self.display.insert(tk.END, ch, "correct")
                else:
                    self.display.insert(tk.END, ch, "wrong")
            else:
                self.display.insert(tk.END, ch)

        self.display.tag_config("correct", foreground="#00e676")
        self.display.tag_config("wrong", foreground="#ff1744")

        self.display.config(state="disabled")

        progress = len(typed)/len(self.sentence)
        self.progress.delete("all")
        self.progress.create_rectangle(0,0,400*progress,10, fill="green")

    def highlight_key(self, event):
        key = event.char.lower()
        if key in self.keys:
            self.keys[key].config(bg="#00e676")
            self.root.after(100, lambda: self.keys[key].config(bg="gray"))

    def draw_keyboard(self, parent):
        kb = tk.Frame(parent, bg="#121212")
        kb.pack(pady=15)

        self.keys = {}

        rows = ["qwertyuiop","asdfghjkl","zxcvbnm"]

        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                lbl = tk.Label(kb, text=ch.upper(),
                               width=6, height=3,
                               bg="#2a2a2a", fg="white",
                               font=("Segoe UI", 14, "bold"))
                lbl.grid(row=r, column=c, padx=5, pady=5)
                self.keys[ch] = lbl

# -------- FINISH -------- #
    def finish_test(self, practice, level):
        end = time.time()
        typed = self.entry.get()

        wpm = (len(typed.split())/(end-self.start_time))*60
        acc = sum(1 for a,b in zip(typed,self.sentence) if a==b)/len(self.sentence)*100

        self.result.config(text=f"{int(wpm)} WPM | {int(acc)}%")
        self.history.append((int(wpm), int(acc)))
        self.save_score(int(wpm), int(acc))

        if practice:
            self.root.after(1500, lambda: self.run_test("mixed", practice=True))

        if level:
            self.scores.append(wpm)
            self.level += 1
            self.root.after(1500, self.next_level)

# -------- HISTORY -------- #
    def show_history(self):
        self.clear()
        f = self.center()

        for i,h in enumerate(self.history,1):
            tk.Label(f, text=f"{i}. {h[0]}WPM {h[1]}%", fg="white", bg="#121212").pack()

        tk.Button(f, text="Back", command=self.menu).pack()

# -------- STATS -------- #
    def show_stats(self):
        self.clear()
        f = self.center()

        if not self.history:
            tk.Label(f, text="No data yet", fg="white", bg="#121212").pack()
        else:
            avg_wpm = sum(h[0] for h in self.history)/len(self.history)
            avg_acc = sum(h[1] for h in self.history)/len(self.history)
            best = max(h[0] for h in self.history)

            tk.Label(f, text=f"Avg WPM: {int(avg_wpm)}", fg="white", bg="#121212").pack()
            tk.Label(f, text=f"Avg Accuracy: {int(avg_acc)}%", fg="white", bg="#121212").pack()
            tk.Label(f, text=f"Best WPM: {best}", fg="white", bg="#121212").pack()
            tk.Label(f, text=f"Total Tests: {len(self.history)}", fg="white", bg="#121212").pack()

        tk.Button(f, text="Back", command=self.menu).pack()

# -------- RUN -------- #
root = tk.Tk()
App(root)
root.mainloop()
