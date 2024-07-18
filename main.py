from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

with app.app_context():
    db.create_all()

@app.route('/', methods=["POST", "GET"])
def base():
    if (request.method == "POST"):
        _firstName = request.form["fname"]
        _lastName = request.form["lname"]
        _email = request.form["email"]
        _password = request.form["password"]
        _passwordConfirm = request.form["password-confirm"]

        if users.query.filter_by(email=_email).first():
            flash("Email already exists!")
            return render_template("signup.html")

        if (isValidPassword(_password, _passwordConfirm)):
            user = users(_firstName, _lastName, _email, _password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("thankYou"))
        else:
            flash("Invalid password!")

    return render_template("signup.html")

@app.route('/thank-you')
def thankYou():
    return render_template("thankyou.html")

@app.route('/signin', methods=["POST", "GET"])
def signin():
    if (request.method == "POST"):
        _email = request.form["email"]
        _password = request.form["password"]

        user = users.query.filter_by(email=_email).first()
        
        if (not user):
            flash("Email does not exist")
            return redirect(url_for("signin"))

        if (user.password != _password):
            flash("Password is incorrect")
            return redirect(url_for("signin"))
        
        return redirect(url_for("secretPage"))

    return render_template("signin.html")

@app.route('/secretPage')
def secretPage():
    return render_template("secretPage.html")







def isValidPassword(inputPassword: str, confirmedPassword):
        if (len(inputPassword) < 7):
            return False
        
        if (not inputPassword[-1].isdigit()):
            return False
        
        lowercase = any(char.islower() for char in inputPassword)
        if (not lowercase):
            return False

        uppercase = any(char.isupper() for char in inputPassword)
        if (not uppercase):
            return False
        
        if (inputPassword != confirmedPassword):
            flash("Passwords do not match!")
            return False
        
        return True












if __name__ == '__main__':
    app.run(debug=True)