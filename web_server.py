from flask import Flask
from threading import threading 

app = Flask('')
@app.rouite('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

