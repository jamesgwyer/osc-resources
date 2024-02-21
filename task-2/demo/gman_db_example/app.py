from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def create_table():
    connection = sqlite3.connect("my_database.db")
    cursor = connection.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_table(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   location TEXT,
                   amount INTEGER,
                   date TEXT
            )
    ''')

    connection.commit()
    connection.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM my_table')
    data = cursor.fetchall()
    connection.close()
    return jsonify(data)

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    location = data['location']
    amount = data['amount']
    date = data['date']

    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO my_table(location, amount, date) VALUES(?, ?, ?)', (location,amount, date))

    connection.commit()
    connection.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)