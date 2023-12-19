
import sqlite3

from flask import Flask, render_template, request
from database_operations import add_commitment, take_over_commitment, view_commitments

app = Flask(__name__)


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
