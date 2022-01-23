from re import search
from MySQLdb.cursors import CursorStoreResultMixIn
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from tabulate import tabulate
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash







#Username Login Model
#None<Special Characters> to returns None
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        

    def __repr__(self):
        return f'<User: {self.username}>'

#Creating an array
users = []
users.append(User(id=1, username='shihan', password='password'))
users.append(User(id=2, username='jinlong', password='password'))
users.append(User(id=3, username='rajesh', password='password'))
users.append(User(id=4, username='Alex', password='123'))



      
                                        




     



#Username Secret Key    
app = Flask(__name__)
app.secret_key = 'secretpassword'
#root:username, no password, sql_name: entiis
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'entiis'


#instantiate the data
mysql = MySQL(app)











class History:
     
    def __init__(self, id, username, pending):
        self.id = id
        self.username  = username
        self.pending = pending
        

    
    
def get_history_data():
    data = []
    data.append(History(id=1, username = 'shihan', pending='10'))
    data.append(History(id=2, username='Jinlong',  pending='7'))
    data.append(History(id=3, username ='Rajesh',  pending='11'))
    return data






#Basic method of the Pending Status in Python
class Pending():
    
    def __init__(self, id, username, days, pending, address):
        self.id = id
        self.username = username
        self.days = days
        self.pending = pending
        self.address = address
        
        


#Since i am able to Remove the pendings objects in the array, i can also add the pending object into the array
pendings = []
pendings.append(Pending(id=386, username='shihan', days= '6',pending='pending', address='Blk 345 #10-93'))
pendings.append(Pending(id=387, username='jinlong',days= '5',pending='pending', address='Apt 12'))
pendings.append(Pending(id=388, username='Rajesh', days= '5', pending='pending', address='Apt Jurong'))
pendings.append(Pending(id=389, username='Alex', days= '5', pending='pending', address='Powerhouse'))
pendings.append(Pending(id=390, username='Shi Han', days= '5', pending='pending', address='Hello World Tommorrow'))






def pending_status():
    
    return pendings



#pending = Pending.pending.(id)
#Pending.Remove
#Objective: Remove the Pending Page & Update the Pending Page
def get_pending_by_id(id):
    for pending in pendings:
        print("After Update: " + id)
        if(str(pending.id) == id):
            return pending













#Requesting Page Log In
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if users and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('summary'))

        return redirect(url_for('login'))
            

    return render_template('login.html')
        


@app.route('/summary')
def summary():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('profile.html')


@app.route('/subscribe')
def subscribe():
    return render_template("content_Page.html")


@app.route('/signup')  #define the sign up function
def register():
    if request.method == 'GET':

       return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')


@app.route('/signup', methods=['POST'])
def register_post():
    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
       id =  pendings.append(Pending(request.form['id']))
       username = pendings.append(Pending(request.form['username']))
       days = pendings.append(Pending(request.form['days']))
       pending = pendings.append(Pending(request.form['pending']))
       address = pendings.append(Pending(request.form['address']))
       cursor = mysql.connection.cursor()
       
       return render_template("database.html", f"Done!!")

    return render_template('form.html')










#This route is for deleting records for pending status
#Based on the ID Tag Number, remove the Tag Number
@app.route('/delete/<id_to_delete>/')
def delete(id_to_delete):
    #Function get_pending_by_id, For Loops the Pending Variable.For Loops the pending variable.
    #Compare ID, find the id object
    #Return Pending Object
    
    p1 = get_pending_by_id(id_to_delete)
    
    pendings.remove(p1)
    print("After remove: " + str(len(pendings)))
    print(p1.id)
    return render_template("database.html", pending = pending_status())


#Updating a route
#Do not put integer value to the id_update
@app.route('/update/<id_update>/', methods=['GET', 'POST'])
def update(id_update):
    p1 = get_pending_by_id(id_update)
    p1.username = request.form['username']
    p1.days = request.form['days']
    return render_template("database.html", pending = pending_status())
    
@app.route('/submit/pending')
def database():   
    all_data = pending_status()
    print(type(all_data))
    return render_template("database.html", pending = all_data)


@app.route('/history')
def history():
    return render_template("History.html", data=get_history_data())



if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)


