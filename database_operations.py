import sqlite3
from tkinter import messagebox


conn = sqlite3.connect('grading_commitments.db')
cursor = conn.cursor()
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
        from tkinter_gui import status_label
        status_label.config(text=f"{taker} has taken over {user}'s grading commitment for {subject}.")
    else:
        # Commitment doesn't exist for the specified user
        messagebox.showinfo("Error", f"{user}'s grading commitment for {subject} does not exist.")

    from tkinter_gui import refresh_commitments
    refresh_commitments()


def view_commitments(user):
    """View a user's grading commitments."""
    cursor.execute("SELECT subject FROM commitments WHERE user = ?", (user,))
    commitments = cursor.fetchall()
    return "\n".join(commitment[0] for commitment in commitments)

def delete_commitment(user, subject, status_label, refresh_func):
    cursor.execute("DELETE FROM commitments WHERE user = ? AND subject = ?", (user, subject))
    conn.commit()
    status_label.config(text=f"{user}'s grading commitment for {subject} has been deleted.")
    refresh_func()

