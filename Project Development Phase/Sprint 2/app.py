import email
from email import message
from importlib.resources import contents
from tkinter import S
from turtle import title
from flask import Flask,redirect, render_template, request, session, url_for, flash
from pyexpat import model
from werkzeug.utils import secure_filename
import ibm_db
from flask_mail import Mail, Message
from markupsafe import escape



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mail = Mail(app)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yzp80326;PWD=cIVWGGyf0cUXp0L1",'','')
print(conn)
print("connection successful...")


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'santasanthosh7252@gmail.com'
app.config['MAIL_PASSWORD'] = '7397712457'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html',mes=message)


@app.route("/mail")
def mailing():
   msg = Message(
                'Hello',
                sender ='santasanthosh7252@gmail.com',
                recipients = ['yogeshkumark2101@gmail.com']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Sent'


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')


@app.route('/signup', methods = ['GET','POST'])
def signup():
    return render_template('signup.html')


@app.route('/complaint')
def complaint():
    return render_template('complaint.html')


@app.route('/agentreg')
def agentreg():
    return render_template('agentreg.html')


@app.route('/agentlogin')
def agentlogin():
    return render_template('agentlogin.html')


@app.route('/agenthome')
def agenthome():
    return render_template('agenthome.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    customer = []
    sql = "SELECT * FROM customer"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        customer.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    if customer:
        sql = "SELECT * FROM customer"
        stmt = ibm_db.exec_immediate(conn, sql)
        user = ibm_db.fetch_both(stmt)
         
    issues = []
    sql = "select * from issues"
    stmt = ibm_db.exec_immediate(conn, sql)
    dict = ibm_db.fetch_both(stmt)
    while dict != False:
        issues.append(dict)
        dict = ibm_db.fetch_both(stmt)
    if issues:
        sql = "SELECT * FROM issues"
        stmt = ibm_db.exec_immediate(conn, sql)
        count = ibm_db.fetch_both(stmt)


    agent = []
    sql = "SELECT * FROM agent"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        agent.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    if agent:
        sql = "SELECT * FROM agent"
        stmt = ibm_db.exec_immediate(conn, sql)
        cot = ibm_db.fetch_both(stmt)
    
    return render_template('admin.html', customer = customer, issues = issues, agent = agent)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        mail = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        sql = "SELECT * FROM customer WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,mail)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

    if account:
        return render_template('index.html', msg="You are already a member, please login using your details....")
      
    else:
      insert_sql = "INSERT INTO customer VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, uname)
      ibm_db.bind_param(prep_stmt, 2, mail)
      ibm_db.bind_param(prep_stmt, 3, phone)
      ibm_db.bind_param(prep_stmt, 4, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Student Data saved successfuly..")

app.route('/issues',methods =['GET','POST'] )
def issues():
    if request.method == "GET":
        customer_name = request.form['customer_name']
        mail = request.form['mail']
        phone = request.form['phone']
        date = request.form['date']
        topic = request.form['topic']
        description = request.form['description']

        insert = "INSERT INTO issues('customer_name','mail','phone','date','topic','description') VALUES (?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert)
        ibm_db.bind_param(prep_stmt, 1, customer_name)
        ibm_db.bind_param(prep_stmt, 2, mail)
        ibm_db.bind_param(prep_stmt, 3, phone)
        ibm_db.bind_param(prep_stmt, 4, date)
        ibm_db.bind_param(prep_stmt, 5, topic)
        ibm_db.bind_param(prep_stmt, 6, description)
        ibm_db.execute(prep_stmt)
        flash("Complaint added Successfully", "success")
        return render_template('dashboard.html')


@app.route('/agentform', methods=['GET', 'POST'])
def agentform():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        link = request.form['resume_link']

        sql = "SELECT * FROM agent WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,mail)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('index.html', msg="You are already a agent, please login using your agent details....")
      
        else:
            insert_sql = "INSERT INTO agent VALUES (?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, mail)
            ibm_db.bind_param(prep_stmt, 3, phone)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.bind_param(prep_stmt, 5, address)
            ibm_db.bind_param(prep_stmt, 6, city)
            ibm_db.bind_param(prep_stmt, 7, state)
            ibm_db.bind_param(prep_stmt, 8, link)
            ibm_db.execute(prep_stmt)
    
    return render_template('agentlogin.html', msg="Student Data saved successfuly..")



@app.route('/loginagent', methods=['GET', 'POST'])
def loginagent():
    app.secret_key = 'santhoshhesbf/.[[.;;ar'
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        print(mail,password)

        sql = f"select * from agent where email='{escape(mail)}' and password='{escape(password)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_both(stmt)
            
        if data:
            session["mail"] = escape(mail)
            session["password"] = escape(password)
            return redirect(url_for('agenthome'))

        else:
            return render_template('agentlogin.html', msg="Account does not exist or invalid Credentials")

    return "NOT WORKING!!??"



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    sec = ''
    if request.method == 'POST':
        
        mail = request.form['email']
        password = request.form['password']

        if mail == 'santhoshk088.cse@dgct.ac.in' and password == '1410':
            return redirect(url_for('admin'))
        
        elif mail == 'yogeshkumark2101@gmail.com' and password == '3004':
            return redirect(url_for('admin'))

        else:
            sql = f"select * from customer where email='{escape(mail)}' and password= '{escape(password)}'"
            
            stmt = ibm_db.exec_immediate(conn, sql)
            data = ibm_db.fetch_both(stmt)
            
            
        if data:
            session["mail"] = escape(mail)
            session["password"] = escape(password)
            return redirect(url_for('dashboard'))




        else:
            return render_template('login.html',msg = "Invalid email/ Password or Not registered!!?")
    
    return "not going to happen dickhead!!??" 



@app.route('/delete/<name>')
def delete(name):
    sql = f"SELECT * FROM Customer WHERE name='{escape(name)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    customer = ibm_db.fetch_row(stmt)
    # print ("The Name is : ",  customer)
    if customer:
        sql = f"DELETE FROM customer WHERE name='{escape(name)}'"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        flash("Delected Successfully", "success")

        customers = []
        sql = "SELECT * FROM customer"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            customers.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
        if customers:
            return redirect(url_for("admin"))



@app.route('/agentdelete/<email>')
def agentdelete(email):
    sql = f"select * from agent where email='{escape(email)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    student = ibm_db.fetch_row(stmt)
    if student:
        sql = f"delete from agent where email='{escape(email)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        users = []
        flash("Delected Successfully", "success")
        return redirect(url_for("admin"))


@app.route('/deletecomplaint/<mail>')
def deletecomplaint(mail):
    sql = f"SELECT * FROM issues WHERE mail='{escape(mail)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    cusdel = ibm_db.fetch_row(stmt)
    if cusdel:
        sql = f"delete from issues where mail='{escape(mail)}';"
        stmt = ibm_db.exec_immediate(conn, sql)
        return redirect(url_for("admin"))





@app.route('/completed/<DESCRIPTION>', methods=['GET', 'POST'])
def completed(DESCRIPTION):
    status ="Completed"
    try:

        sql = "UPDATE ISSUE SET STATUS = ? WHERE DESCRIPTION =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,status)
        ibm_db.bind_param(stmt,2,DESCRIPTION)
        ibm_db.execute(stmt)

        flash("Successful","success")
        return redirect(url_for('agentwelcome'))
    except:
        flash("No record found","danger")
        return redirect(url_for('agentwelcome'))




if __name__ == "__main__":
    app.run(debug=True)