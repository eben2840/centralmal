
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, url_for,request
import urllib.request, urllib.parse
from flask_migrate import Migrate

from form import *


app=Flask(__name__)
app.config['SECRET_KEY']= 'ADKADKFJ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)





def sendtelegram(params):
    url = "https://api.telegram.org/bot5787281305:AAE1S8DSnMAyQuzAnXOHfxLq-iyvPwYJeAo/sendMessage?chat_id=-1001556929308&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    return content



class Person(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200))
    number= db.Column(db.String(200))
    comment= db.Column(db.String(200))
    def __repr__(self):
        return f"Person('{self.id}', {self.name}', {self.number})"




@app.route('/', methods=['POST','GET'])
def home():
    form = Form()
    
    
    if form.validate_on_submit():
            print('Success')
            new =Person(name=form.name.data, 
                        number=form.number.data, 
                        comment=form.comment.data)
            db.session.add(new)
            db.session.commit()
            print("New Program Added", "success")
           
            return redirect(url_for('/comment'))
    else:
        print(form.errors)
    return render_template('index.html', form=form)
   

@app.route('/comment')
def comment():
    persons=Person.query.order_by(Person.id.desc()).all()
    print(persons)
    return render_template("comment.html", persons=persons)

 




if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)