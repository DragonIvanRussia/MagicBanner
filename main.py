from flask import Flask, render_template, redirect, request, make_response, session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port='8080', host='192.168.1.51')
    
