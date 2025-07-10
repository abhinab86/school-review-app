from flask import Flask, render_template, request, redirect
from config import MYSQL_CONFIG
import mysql.connector

app = Flask(__name__)

# DB Connection Function
def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Home page redirects to reviews
@app.route('/')
def home():
    return redirect('/reviews')

# Page to add review
@app.route('/add-review')
def add_review():
    return render_template('add_review.html')

# Display reviews page
@app.route('/reviews')
def reviews_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, school, rating, comment FROM reviews")
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reviews.html', reviews=reviews)

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit_review():
    name = request.form['name']
    school = request.form['school']
    rating = request.form['rating']
    comment = request.form['comment']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO reviews (name, school, rating, comment) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, school, rating, comment))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/reviews')

if __name__ == '__main__':
    app.run(debug=True)
