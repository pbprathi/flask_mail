from flask import Flask,request
#from flask_sqlalchemy import SQLAlchemy,create_engine
from sqlalchemy import create_engine
from flask_mail import Mail,Message
import os

app=Flask(__name__)
#mail=Mail(app)

SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="XXXXX",
    hostname="localhost",
    databasename="todo",
)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pbprathi@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PWD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#curl -i http://127.0.0.1:5000/send_mail

@app.route('/send_mail')
def send_mail():
    tablebuild=  "<tr><th>Task_ID</th><th>Task Description</th><th>Status</th></tr>"
    engine=create_engine(SQLALCHEMY_DATABASE_URI)
    conn=engine.connect()
    dataset=conn.execute("select * from tasks")
    for data in dataset:
        tablebuild += "<tr><td>" + str(data[0]) + "</td><td>" + data[1] + "</td><td>" + "Not Completed" if str(data[2]) == "1" else "Completed" + "</td></tr>"

    msg = Message('Hello', sender = 'pbprathi@gmail.com', recipients = ['pbprathi@gmail.com'])
    msg.html = """ <html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;
    }th, td {padding: 5px;text-align: left;}</style></head><body><h2>Monthly Tasks</h2>
    <table style="width:100%">""" + tablebuild + """</table></body></html>"""

    mail.send(msg)
    return "Sent"

if __name__ == '__main__':
   app.run(debug = True)
