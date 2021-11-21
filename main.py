from flask import Flask, render_template, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mail import Message, Mail
import datetime
import os

mail = Mail()
app = Flask(__name__)

app.secret_key = os.environ['form_token']

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ['email_id']
app.config["MAIL_PASSWORD"] = os.environ['pwd']

mail.init_app(app)

current_year = datetime.datetime.now().year


class ContactForm(FlaskForm):
    name = StringField(label="Name: ", validators=[DataRequired("Please enter your name.")])
    email = EmailField(label="Email: ", validators=[DataRequired("Please enter your email address."), Email()])
    phone = StringField(label="Phone: ", validators=[DataRequired("Please enter your phone number.")])
    message = TextAreaField(label="Message: ", validators=[DataRequired("Please enter your message.")])
    submit = SubmitField(label="Send")


@app.route("/")
def home():
    return render_template("index.html", year=current_year)


@app.route("/skills.html")
def skills():
    return render_template("skills.html", year=current_year)


@app.route("/contact.html", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash("All fields are required!")
            return render_template("contact.html", year=current_year, form=form)
        else:
            msg = Message(subject="Message from Personal Website!", sender="te81493@gmail.com", recipients=["manalgafoor24@gmail.com"])
            msg.body = f"From: {form.name.data}, {form.email.data}, {form.phone.data}\n{form.message.data}"
            mail.send(msg)
            return render_template("contact.html", year=current_year, success=True)

    elif request.method == 'GET':
        return render_template("contact.html", year=current_year, form=form)


if __name__ == "__main__":
    app.run()
