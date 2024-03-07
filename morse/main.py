from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, translate_to TEXT, translated_text TEXT)''')
    conn.commit()
    conn.close()

# Function to insert a new query into the database
def insert_query(text, translate_to, translated_text):
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute("INSERT INTO queries (text, translate_to, translated_text) VALUES (?, ?, ?)", (text, translate_to, translated_text))
    conn.commit()
    conn.close()

# Function to fetch all past queries from the database
def get_past_queries():
    conn = sqlite3.connect('queries.db')
    c = conn.cursor()
    c.execute("SELECT * FROM queries")
    rows = c.fetchall()
    conn.close()
    return rows

# Text to Morse code conversion
def text_to_morse(text):
    morse_code = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                  'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                  'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                  'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                  '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/', '.': '.-.-.-',
                  ',': '--..--', '?': '..--..', '\'': '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.',
                  ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
                  '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', 'Ä': '.-.-',
                  'Á': '.--.-', 'Å': '.--.-', 'Ch': '----', 'É': '..-..', 'Ñ': '--.--', 'Ö': '---.', 'Ü': '..--'}
    morse = ''
    for char in text:
        if char.upper() in morse_code:
            morse += morse_code[char.upper()] + ' '
    return morse.strip()

# Morse code to text conversion
def morse_to_text(morse):
    morse_code = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
                  '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
                  '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
                  '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
                  '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0', '/': ' ', '.-.-.-': '.',
                  '--..--': ',', '..--..': '?', '.----.': '\'', '-.-.--': '!', '-..-.': '/', '-.--.': '(',
                  '-.--.-': ')', '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+',
                  '-....-': '-', '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@', '.-.-': 'Ä',
                  '.--.-': 'Á', '.--.-': 'Å', '----': 'Ch', '..-..': 'É', '--.--': 'Ñ', '---.': 'Ö', '..--': 'Ü'}
    text = ''
    morse_list = morse.split(' ')
    for code in morse_list:
        if code in morse_code:
            text += morse_code[code]
    return text

create_table()  # Create the table when the application starts

@app.route('/', methods=['GET', 'POST'])
def index():
    past_queries = get_past_queries()
    translated_text = ''
    if request.method == 'POST':
        text = request.form['text']
        translate_to = request.form['translate_to']
        if translate_to == 'morse':
            translated_text = text_to_morse(text)
        elif translate_to == 'text':
            translated_text = morse_to_text(text)
        insert_query(text, translate_to, translated_text)  # Insert the query into the database
    return render_template('index.html', translated_text=translated_text, past_queries=past_queries)

@app.route('/database')
def database():
    past_queries = get_past_queries()
    return render_template('database.html', past_queries=past_queries)

if __name__ == '__main__':
    app.run(debug=True)
