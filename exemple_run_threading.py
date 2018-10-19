import threading
import time
from flask import Flask
app = Flask(__name__)

x = 0


def run_job():
    while True:
        print("Run recurring task")
        global x
        x += 1
        time.sleep(3)

@app.route("/")
def hello():
    return "Hello World!" + str(x)


if __name__ == "__main__":
    thread = threading.Thread(target=run_job)
    thread.start()
    app.run()
