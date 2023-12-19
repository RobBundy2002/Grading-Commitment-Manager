
import sys
import tkinter as tk
from tkinter import ttk
from database_operations import add_commitment, take_over_commitment, view_commitments, delete_commitment


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


def delete_commitment_button():
    user = delete_user_entry.get()
    subject = delete_assignment_entry.get()
    delete_commitment(user, subject, status_label, refresh_commitments)


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
root.geometry("830x370")  # Set the window size
root.configure(bg="darkblue")  # Set background color

# Add padding around the frames
frame_pad_x = 10
frame_pad_y = 10

pad_y = 11
pad_x = 30

# Create and arrange frames
left_frame = ttk.Frame(root, padding=(frame_pad_x, frame_pad_y), width=400, height=200)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

right_frame = ttk.Frame(root, padding=(frame_pad_x, frame_pad_y), width=400, height=200)
right_frame.grid(row=0, column=1, padx=3, pady=20, sticky=tk.W)

# Left Frame (Add Commitments and View Commitments)
name_label = ttk.Label(left_frame, text="Your Name:")
name_label.grid(row=0, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

name_entry = ttk.Entry(left_frame)
name_entry.grid(row=0, column=1, pady=pad_y, padx=pad_x)

assignment_label = ttk.Label(left_frame, text="Assignment:")
assignment_label.grid(row=1, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

assignment_entry = ttk.Entry(left_frame)
assignment_entry.grid(row=1, column=1, pady=pad_y, padx=pad_x)

add_button = ttk.Button(left_frame, text="Add Commitment", command=add_commitment_button)
add_button.grid(row=2, column=0, columnspan=2, pady=pad_y, padx=pad_x)

view_commitments_label = ttk.Label(left_frame, text="View Commitments:")
view_commitments_label.grid(row=3, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

view_user_entry = ttk.Entry(left_frame)
view_user_entry.grid(row=3, column=1, pady=pad_y, padx=pad_x)

view_button = ttk.Button(left_frame, text="View Commitments", command=view_commitments_button)
view_button.grid(row=4, column=0, columnspan=2, pady=pad_y, padx=pad_x)

commitments_label = ttk.Label(left_frame, text="")
commitments_label.grid(row=5, column=0, columnspan=2, pady=pad_y, padx=pad_x)
# Right Frame (Take Over Commitments and Delete Assignments)
original_user_label = ttk.Label(right_frame, text="Original User:")
original_user_label.grid(row=0, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

original_user_entry = ttk.Entry(right_frame)
original_user_entry.grid(row=0, column=1, pady=pad_y, padx=pad_x)

taker_label = ttk.Label(right_frame, text="Taker:")
taker_label.grid(row=1, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

taker_entry = ttk.Entry(right_frame)
taker_entry.grid(row=1, column=1, pady=pad_y, padx=pad_x)

assignment_takeover_label = ttk.Label(right_frame, text="Assignment:")
assignment_takeover_label.grid(row=2, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

assignment_takeover_entry = ttk.Entry(right_frame)
assignment_takeover_entry.grid(row=2, column=1, pady=pad_y, padx=pad_x)

take_over_button = ttk.Button(right_frame, text="Take Over Commitment", command=take_over_commitment_button)
take_over_button.grid(row=3, column=0, columnspan=2, pady=pad_y, padx=pad_x)

delete_user_label = ttk.Label(right_frame, text="User Who Wishes To Delete:")
delete_user_label.grid(row=4, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

delete_user_entry = ttk.Entry(right_frame)
delete_user_entry.grid(row=4, column=1, pady=pad_y, padx=pad_x)

delete_assignment_label = ttk.Label(right_frame, text="Assignment to Delete:")
delete_assignment_label.grid(row=5, column=0, pady=pad_y, padx=pad_x, sticky=tk.W)

delete_assignment_entry = ttk.Entry(right_frame)
delete_assignment_entry.grid(row=5, column=1, pady=pad_y, padx=pad_x)

delete_button = ttk.Button(right_frame, text="Delete Assignment", command=delete_commitment_button)
delete_button.grid(row=6, column=0, columnspan=2, pady=pad_y, padx=pad_x)

status_label = ttk.Label(root, text="")
status_label.grid(row=1, column=0, columnspan=2, pady=pad_y, padx=pad_x)

cs_label = tk.Label(root, text="CS1112 Grading Manager", font=("Helvetica", 19, "bold"), fg="#ff9900", bg="darkblue")
cs_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.NW)

root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing

root.mainloop()
