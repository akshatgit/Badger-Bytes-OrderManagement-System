from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/adminLogin')
def adminLogin():
    return render_template("adminLogin.html")

if __name__ == '__main__':
    app.run()
