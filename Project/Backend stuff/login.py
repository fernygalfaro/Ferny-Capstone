from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your authentication logic here
        if username == "correct_username" and password == "correct_password":
            return "Login successful!", 200
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
