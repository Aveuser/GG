import csv
import tkinter as tk
from tkinter import messagebox
import os

# Define the leaderboard file name
LEADERBOARD_FILE = 'quiz_results.csv'


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def update_score(self, points):
        self.score += points

    def get_score(self):
        return self.score


class Question:
    def __init__(self, prompt, choices, answer):
        self.prompt = prompt
        self.choices = choices
        self.answer = answer


questions = [
    Question("What is the SI unit for length?",
             ["A) Newton (N )", "B ) Meter (m)", "C) Joule (J)", "D) Pascal (Pa)"],
             "B ) Meter (m)"),
    Question("What is the conversion factor between meters and centimeters?",
             ["A) 100 cm = 1 m", "B )10 cm = 1 m", "C) 1000 cm = 1 m", "D) 1 cm = 1 m"],
             "A) 100 cm = 1 m"),
    Question("What is the standard unit for measuring mass?",
             ["A) Kilogram (kg)", "B ) Gram (g)", "C) Newton (N )", "D) Pound (lb)"],
             "A) Kilogram (kg)"),
    Question("How many millimeters are there in a meter?",
             ["A) 1000 mm", "B ) 100 mm", "C) 10 mm", "D) 1 mm"],
             "A) 1000 mm"),
    Question("Which of the following is a unit of time?",
             ["A) Kilogram (kg)", "B ) Second (s)", "C) Newton (N )", "D) Meter (m)"],
             "B ) Second (s)"),
    Question("What is the conversion factor between kilometers and meters?",
             ["A) 1000 m = 1 km", "B )100 m = 1 km", "C) 10 m = 1 km", "D) 1 m = 1 km"],
             "A) 1000 m = 1 km"),
    Question("Which of the following is a unit of temperature in the SI system?",
             ["A) Fahrenheit (°F)", "B ) Celsius (°C)", "C) Kelvin (K)", "D) Rankine (°R)"],
             "C) Kelvin (K)"),
    Question("What is the SI unit for electric current?",
             ["A) Ampere (A)", "B ) Volt (V)", "C) Ohm (Ω)", "D) Watt (W)"],
             "A) Ampere (A)"),
    Question("How many centimeters are there in a meter?",
             ["A) 100 cm", "B )10 cm", "C) 1000 cm", "D) 1 cm"],
             "A) 100 cm"),
    Question("What is the conversion factor between grams and kilograms?",
             ["A) 1000 g = 1 kg", "B ) 100 g = 1 kg", "C) 10 g = 1 kg", "D) 1 g = 1 kg"],
             "A) 1000 g = 1 kg")
]


class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.attributes("-fullscreen", True)
        self.player = None
        self.current_question_idx = 0
        self.score_label = None
        self.choices_buttons = []

        self.load_leaderboard()  # Load leaderboard data when the program starts

        self.display_question()

    def load_leaderboard(self):
        # Check if the leaderboard file exists
        if os.path.isfile(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header
                self.leaderboard_data = list(csv_reader)
        else:
            self.leaderboard_data = []

    def display_question(self):
        self.player_name = tk.StringVar()
        self.player_name.set("Enter your name")
        self.name_entry = tk.Entry(self.master, textvariable=self.player_name, font=("Helvetica", 24))
        self.name_entry.grid(row=0, column=0, columnspan=2)

        start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz, font=("Helvetica", 24))
        start_button.grid(row=1, column=0, columnspan=2)

    def start_quiz(self):
        player_name = self.player_name.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        self.player = Player(player_name)

        self.name_entry.grid_forget()

        self.score_label = tk.Label(self.master, text=f"Score: {self.player.score}", font=("Helvetica", 24))
        self.score_label.grid(row=0, column=0, columnspan=2)

        self.display_current_question()

    def display_current_question(self):
        question = questions[self.current_question_idx]

        tk.Label(self.master, text=question.prompt, font=("Helvetica", 24)).grid(row=1, column=0, columnspan=2)

        for i, choice in enumerate(question.choices):
            button = tk.Button(self.master, text=choice, command=lambda c=choice: self.check_answer(c),
                               font=("Helvetica", 18))
            button.grid(row=i + 2, column=0, columnspan=2, padx=20, pady=10, sticky="we")
            self.choices_buttons.append(button)

    def check_answer(self, choice):
        question = questions[self.current_question_idx]
        if choice == question.answer:
            messagebox.showinfo("Result", "Correct!")
            self.player.update_score(10)
        else:
            messagebox.showinfo("Result", "Incorrect!")
            self.player.update_score(-5)

        self.current_question_idx += 1
        for button in self.choices_buttons:
            button.grid_forget()
        self.choices_buttons = []

        self.score_label.config(text=f"Score: {self.player.score}")

        if self.current_question_idx < len(questions):
            self.display_current_question()
        else:
            messagebox.showinfo("Quiz Completed", f"Congratulations, {self.player.name}! You've completed the quiz.")
            self.update_leaderboard()  # Update the leaderboard when the quiz is completed
            self.display_leaderboard()  # Display the leaderboard

    def update_leaderboard(self):
        with open(LEADERBOARD_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if len(self.leaderboard_data) == 0:
                writer.writerow(["Name", "Score"])
            writer.writerow([self.player.name, self.player.score])

    def display_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.attributes("-fullscreen", True)
        leaderboard_window.title("Leaderboard")

        leaderboard_label = tk.Label(leaderboard_window, text="Leaderboard", font=("Helvetica", 36))
        leaderboard_label.pack(pady=20)

        leaderboard = tk.Text(leaderboard_window, font=("Helvetica", 24))
        leaderboard.pack(expand=True, fill="both", padx=50, pady=10)

        for idx, row in enumerate(self.leaderboard_data, start=1):
            player_name = row[0]
            player_score = row[1]
            leaderboard.insert(tk.END, f"{idx}. {player_name} - Score: {player_score}\n")

            remove_button = tk.Button(leaderboard_window, text="Remove",
                                      command=lambda name=player_name: self.remove_player(name))
            leaderboard.window_create(tk.END, window=remove_button)
            leaderboard.insert(tk.END, "\n")

        restart_button = tk.Button(leaderboard_window, text="Restart Quiz", command=self.restart_quiz,
                                   font=("Helvetica", 24))
        restart_button.pack(pady=20)

    def remove_player(self, name):
        with open(LEADERBOARD_FILE, mode='r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)

        with open(LEADERBOARD_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Score"])
            for row in rows:
                if row[0] != name:
                    writer.writerow(row)

        messagebox.showinfo("Player Removed", f"{name} has been removed from the leaderboard.")
        self.load_leaderboard()
        self.display_leaderboard()

    def restart_quiz(self):
        self.master.destroy()
        root = tk.Tk()
        app = QuizApp(root)
        quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Helvetica", 24))
        quit_button.grid(row=3, column=0, columnspan=2)
        root.mainloop()


def main():
    root = tk.Tk()
    app = QuizApp(root)

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position for the window to be centered
    x = (screen_width - root.winfo_reqwidth()) // 2
    y = (screen_height - root.winfo_reqheight()) // 2

    # Set the geometry for the window to be centered
    root.geometry("+{}+{}".format(x, y))

    root.mainloop()


if __name__ == "__main__":
    main()
