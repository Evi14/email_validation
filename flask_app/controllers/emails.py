from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.email import Email

@app.route('/')
def index():
    return render_template("index.html")    

@app.route("/validation", methods=["POST"])
def get_email():
    if Email.is_valid(request.form):
        Email.save(request.form)
        return redirect("/success")
    return redirect("/")

@app.route('/success')
def allDojos():
    emails = Email.get_all()
    return render_template("success.html", all_emails = emails)


@app.route('/delete/<int:id>')
def deleteEmail(id):
    data ={
        'id': id
    }
    Email.delete(data)
    return redirect('/') 
