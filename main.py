from flask import Flask, render_template, request
import smtplib

import requests
MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"

app = Flask(__name__)

posts = requests.get('https://api.npoint.io/9dc649126a496c0c1921').json()


@app.route('/')
def home_page():
    return render_template("index.html", all_posts=posts)


@app.route('/about')
def get_about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = f"subject:User Question ?\n\nName: {request.form['name']}\nEmail: {request.form['email']}\nContact Number: {request.form['telephone']}\nMessage: {request.form['message']}"
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message)
        connection.close()
        return render_template("contact.html", heading="Successfully sent message")
    return render_template("contact.html", heading="Contact Me")


@app.route('/post/<int:num>')
def get_post(num):
    requested_post = None
    for p in posts:
        if p['id'] == num:
            requested_post = p
    return render_template("post.html", post=requested_post, id=num, image=requested_post['img'])


if __name__ == "__main__":
    app.run(debug=True)
