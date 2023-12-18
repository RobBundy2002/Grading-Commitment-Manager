import tkinter as tk

# Initialize an empty dictionary to store grading commitments
grading_commitments = {}

def add_commitment(user, subject):
    """Add a grading commitment for a user."""
    if user not in grading_commitments:
        grading_commitments[user] = []
    grading_commitments[user].append(subject)

def take_over_commitment(user, taker, subject):
    """Allow a user to take over another user's grading commitment."""
    if user in grading_commitments and subject in grading_commitments[user]:
        grading_commitments[user].remove(subject)
        add_commitment(taker, subject)

def view_commitments(user):
    """View a user's grading commitments."""
    if user in grading_commitments:
        commitments = grading_commitments[user]
        return "\n".join(commitments)
    else:
        return f"{user} has no grading commitments."

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
    status_label.config(text=f"{taker} has taken over {user}'s grading commitment for {subject}.")
    original_user_entry.delete(0, tk.END)  # Clear the original user field
    taker_entry.delete(0, tk.END)  # Clear the taker field
    assignment_takeover_entry.delete(0, tk.END)  # Clear the assignment takeover field
    refresh_commitments()

def view_commitments_button():
    user = view_user_entry.get()
    commitments = view_commitments(user)
    commitments_label.config(text=commitments)

def refresh_commitments():
    user = view_user_entry.get()
    commitments = view_commitments(user)
    commitments_label.config(text=commitments)

# Create the main window
root = tk.Tk()
root.title("Grading Commitments Manager")

# Styling
root.geometry("400x800")  # Set the window size
root.configure(bg="#f0f0f0")  # Set background color

# Create and arrange widgets with padding
pad_y = 5
pad_x = 20

name_label = tk.Label(root, text="Your Name:")
name_label.pack(pady=pad_y, padx=pad_x)
name_entry = tk.Entry(root)
name_entry.pack(pady=pad_y, padx=pad_x)

assignment_label = tk.Label(root, text="Assignment:")
assignment_label.pack(pady=pad_y, padx=pad_x)
assignment_entry = tk.Entry(root)
assignment_entry.pack(pady=pad_y, padx=pad_x)

add_button = tk.Button(root, text="Add Commitment", command=add_commitment_button)
add_button.pack(pady=pad_y, padx=pad_x)

original_user_label = tk.Label(root, text="Original User:")
original_user_label.pack(pady=pad_y, padx=pad_x)
original_user_entry = tk.Entry(root)
original_user_entry.pack(pady=pad_y, padx=pad_x)

taker_label = tk.Label(root, text="Taker:")
taker_label.pack(pady=pad_y, padx=pad_x)
taker_entry = tk.Entry(root)
taker_entry.pack(pady=pad_y, padx=pad_x)

assignment_takeover_label = tk.Label(root, text="Assignment:")
assignment_takeover_label.pack(pady=pad_y, padx=pad_x)
assignment_takeover_entry = tk.Entry(root)
assignment_takeover_entry.pack(pady=pad_y, padx=pad_x)

take_over_button = tk.Button(root, text="Take Over Commitment", command=take_over_commitment_button)
take_over_button.pack(pady=pad_y, padx=pad_x)

view_user_label = tk.Label(root, text="View Commitments for:")
view_user_label.pack(pady=pad_y, padx=pad_x)
view_user_entry = tk.Entry(root)
view_user_entry.pack(pady=pad_y, padx=pad_x)

view_button = tk.Button(root, text="View Commitments", command=view_commitments_button)
view_button.pack(pady=pad_y, padx=pad_x)

commitments_label = tk.Label(root, text="")
commitments_label.pack(pady=pad_y, padx=pad_x)

status_label = tk.Label(root, text="")
status_label.pack(pady=pad_y, padx=pad_x)

root.mainloop()

from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize an empty dictionary to store grading commitments
grading_commitments = {}

# Your existing functions here...

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
