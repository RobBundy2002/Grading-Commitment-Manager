import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from flask import Flask, render_template, request
import sys

app = Flask(__name__)

# Create SQLite database and table
conn = sqlite3.connect('grading_commitments.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS commitments (
        user TEXT,
        subject TEXT,
        PRIMARY KEY (user, subject)
    )
''')
conn.commit()


def add_commitment(user, subject):
    """Add a grading commitment for a user."""
    # Check if the assignment already exists for the user
    cursor.execute("SELECT * FROM commitments WHERE user = ? AND subject = ?", (user, subject))
    existing_commitment = cursor.fetchone()

    if existing_commitment:
        # Assignment already exists, display an error message
        messagebox.showinfo("Error", f"{user} already has a grading commitment for {subject}.")
    else:
        # Assignment doesn't exist, add it
        cursor.execute("INSERT INTO commitments (user, subject) VALUES (?, ?)", (user, subject))
        conn.commit()

def take_over_commitment(user, taker, subject):
    """Allow a user to take over another user's grading commitment."""
    # Check if the commitment exists for the specified user
    cursor.execute("SELECT * FROM commitments WHERE user = ? AND subject = ?", (user, subject))
    existing_commitment = cursor.fetchone()

    if existing_commitment:
        # Commitment exists, proceed with takeover
        cursor.execute("DELETE FROM commitments WHERE user = ? AND subject = ?", (user, subject))
        add_commitment(taker, subject)
        conn.commit()
        status_label.config(text=f"{taker} has taken over {user}'s grading commitment for {subject}.")
    else:
        # Commitment doesn't exist for the specified user
        messagebox.showinfo("Error", f"{user}'s grading commitment for {subject} does not exist.")

    refresh_commitments()


def view_commitments(user):
    """View a user's grading commitments."""
    cursor.execute("SELECT subject FROM commitments WHERE user = ?", (user,))
    commitments = cursor.fetchall()
    return "\n".join(commitment[0] for commitment in commitments)


def add_commitment_button():
    user = name_entry.get()
    subject = assignment_entry.get()
    add_commitment(user, subject)
    status_label.config(text=f"{user} has added a grading commitment for {subject}.")
    name_entry.delete(0, tk.END)  # Clear the name field
    assignment_entry.delete(0, tk.END)  # Clear the assignment field
    refresh_commitments()


def take_over_commitment_button():
    user = original_user_entry.get()
    taker = taker_entry.get()
    subject = assignment_takeover_entry.get()
    take_over_commitment(user, taker, subject)


def view_commitments_button():
    user = view_user_entry.get()
    commitments = view_commitments(user)
    commitments_label.config(text=commitments)


def refresh_commitments():
    user = view_user_entry.get()
    commitments = view_commitments(user)
    commitments_label.config(text=commitments)


def on_closing():
    root.destroy()
    sys.exit()


# Create the main window
root = tk.Tk()
root.title("Grading Commitments Manager")

# Styling
root.geometry("400x800")  # Set the window size
root.configure(bg="#333333")  # Set background color
root.option_add('*TButton*highlightBackground', '#333333')  # Set button highlight color

# Create and arrange widgets with padding
pad_y = 5
pad_x = 20

style = ttk.Style()
style.configure('TButton', padding=6, font=('Helvetica', 10, 'bold'), background='black', foreground='black')  # Set button color to black
style.configure('TEntry', padding=6, font=('Helvetica', 10), background='#555555', foreground='black')  # Set text color to black
style.configure('TLabel', font=('Helvetica', 10), background='#333333', foreground='white')

name_label = ttk.Label(root, text="Your Name:")
name_label.pack(pady=pad_y, padx=pad_x)

name_entry = ttk.Entry(root)
name_entry.pack(pady=pad_y, padx=pad_x)

assignment_label = ttk.Label(root, text="Assignment:")
assignment_label.pack(pady=pad_y, padx=pad_x)

assignment_entry = ttk.Entry(root)
assignment_entry.pack(pady=pad_y, padx=pad_x)

add_button = ttk.Button(root, text="Add Commitment", command=add_commitment_button)
add_button.pack(pady=pad_y, padx=pad_x)

original_user_label = ttk.Label(root, text="Original User:")
original_user_label.pack(pady=pad_y, padx=pad_x)

original_user_entry = ttk.Entry(root)
original_user_entry.pack(pady=pad_y, padx=pad_x)

taker_label = ttk.Label(root, text="Taker:")
taker_label.pack(pady=pad_y, padx=pad_x)

taker_entry = ttk.Entry(root)
taker_entry.pack(pady=pad_y, padx=pad_x)

assignment_takeover_label = ttk.Label(root, text="Assignment:")
assignment_takeover_label.pack(pady=pad_y, padx=pad_x)

assignment_takeover_entry = ttk.Entry(root)
assignment_takeover_entry.pack(pady=pad_y, padx=pad_x)

take_over_button = ttk.Button(root, text="Take Over Commitment", command=take_over_commitment_button)
take_over_button.pack(pady=pad_y, padx=pad_x)

view_user_label = ttk.Label(root, text="View Commitments for:")
view_user_label.pack(pady=pad_y, padx=pad_x)

view_user_entry = ttk.Entry(root)
view_user_entry.pack(pady=pad_y, padx=pad_x)

view_button = ttk.Button(root, text="View Commitments", command=view_commitments_button)
view_button.pack(pady=pad_y, padx=pad_x)

commitments_label = ttk.Label(root, text="")
commitments_label.pack(pady=pad_y, padx=pad_x)

status_label = ttk.Label(root, text="")
status_label.pack(pady=pad_y, padx=pad_x)

root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing

root.mainloop()
from flask import Flask, render_template, request

app = Flask(__name__)

# Use the existing SQLite connection and cursor
conn = sqlite3.connect('grading_commitments.db')
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_commitment', methods=['POST'])
def add_commitment_route():
    user = request.form['name']
    subject = request.form['assignment']
    add_commitment(user, subject)
    return "Commitment added successfully."

@app.route('/take_over_commitment', methods=['POST'])
def take_over_commitment_route():
    user = request.form['original_user']
    taker = request.form['taker']
    subject = request.form['assignment_takeover']
    take_over_commitment(user, taker, subject)
    return "Commitment taken over successfully."

@app.route('/view_commitments', methods=['POST'])
def view_commitments_route():
    user = request.form['view_user']
    commitments = view_commitments(user)
    return commitments

if __name__ == '__main__':
    app.run(debug=True)
