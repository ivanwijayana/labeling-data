from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Inisialisasi database SQLite
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS labeled_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            label INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('text-labeling.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    label = request.form['label']

    # Menyimpan data ke database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO labeled_data (text, label) VALUES (?, ?)", (text, label))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data berhasil disimpan!"})

@app.route('/save')
def save():
    # Menampilkan data yang sudah disimpan
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM labeled_data")
    data = cursor.fetchall()
    conn.close()
    return render_template('save.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
