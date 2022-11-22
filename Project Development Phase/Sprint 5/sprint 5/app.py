from importlib.resources import contents
from tkinter import S
from turtle import title
from flask import Flask,redirect, render_template, request, session, url_for, flash
from pyexpat import model
from werkzeug.utils import secure_filename
import ibm_db
from markupsafe import escape



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yzp80326;PWD=cIVWGGyf0cUXp0L1",'','')
print(conn)
print("connection successful...")



@app.route('/')
def home():
    return render_template('index.html')



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


@app.route('/usercomplaints')
def usercomplaints():
    return render_template('usercomplaints.html')


@app.route('/myusercomp',methods = ['GET','POST'])
def myusercomp():
    if request.method == 'POST':
        mail = request.form['email']

        issues = []
        sql = f"select * from issues where email = '{escape(mail)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        dict = ibm_db.fetch_both(stmt)
        while dict != False:
            issues.append(dict)
            dict = ibm_db.fetch_both(stmt)

         
        return render_template('myusercomp.html',issues = issues)


@app.route('/dashboard')
def dashboard():
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
    return render_template('dashboard.html',issues=issues)


@app.route('/agenthome')
def agenthome():

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
        return render_template('agenthome.html',issues=issues)



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
    
    return render_template('login.html', msg="User Data saved successfuly..")

@app.route('/issues',methods =['GET','POST'] )
def issues():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        mail = request.form['mail']
        phone = request.form['Phone']
        date = request.form['date']
        topic = request.form['topic']
        description = request.form['description']

        insert = "INSERT INTO issues(customername,email,phone,date,topic,description) VALUES (?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert)
        ibm_db.bind_param(prep_stmt, 1, customer_name)
        ibm_db.bind_param(prep_stmt, 2, mail)
        ibm_db.bind_param(prep_stmt, 3, phone)
        ibm_db.bind_param(prep_stmt, 4, date)
        ibm_db.bind_param(prep_stmt, 5, topic)
        ibm_db.bind_param(prep_stmt, 6, description)
        ibm_db.execute(prep_stmt)
        flash("Complaint added Successfully", "success")
        return redirect(url_for('dashboard'))


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
    
    return render_template('agentlogin.html', msg="User Data saved successfuly..")



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

        if mail =='sathish@gmail.com' and password =='1610':
            return redirect(url_for('admin'))
        
        elif mail =='santhoshk088.cse@dgct.ac.in' and password =='3004':
            return redirect(url_for('admin'))

        else:
            sql = f"select * from customer where email='{escape(mail)}' and password= '{escape(password)}'"
            stmt = ibm_db.exec_immediate(conn, sql)
            data = ibm_db.fetch_both(stmt)
                       
        if data:
            session["loggedin"] = True
            session["mail"] = escape(mail)
            session["password"] = escape(password)
            return redirect(url_for('dashboard'))

        else:
            return render_template('login.html',msg = "Invalid email/ Password or Not registered!!?")
    
    return "not going to happen!!??" 



@app.route('/delete/<name>')
def delete(name):
    sql = f"SELECT * FROM Customer WHERE name='{ escape(name) }'"
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
        user = []
        flash("Deleted Successfully", "success")
    return redirect(url_for("admin"))


@app.route('/deletecomplaint/<email>')
def deletecomplaint(email):
    sql = f"SELECT * FROM issues WHERE email='{escape(email)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    cusdel = ibm_db.fetch_row(stmt)
    if cusdel:
        sql = f"delete from issues where email='{escape(email)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
    return redirect(url_for("admin"))



@app.route('/completed/<email>', methods=['GET', 'POST'])
def completed(email):
    status ="Completed"
    try:

        sql = "UPDATE issues SET STATUS = ? WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,status)
        ibm_db.bind_param(stmt,2,email)
        ibm_db.execute(stmt)

        flash("Successful","success")
        return redirect(url_for('agenthome'))
    except:
        flash("No record found","danger")
        return redirect(url_for('agenthome'))


@app.route('/agentalloc',methods = ['GET','POST'])
def agentalloc():
    status = "agent assigned"
    if request.method == 'POST':
        mail = request.form['email']
        amail = request.form['agentmail']

        sql = "select * from issues where email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,mail)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)

    if data:
        sql = "UPDATE issues SET serviceagent = ?, status = ? WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,amail)
        ibm_db.bind_param(stmt,2,status)
        ibm_db.bind_param(stmt,3,mail)
        ibm_db.execute(stmt)
        return redirect(url_for('admin'))

        
    else:
        flash("No complaint found", "success")
    return redirect(url_for('admin'))


@app.route('/viewmine',methods =['GET','POST'])
def viewmine():
    if request.method == 'POST':
        email = request.form['email']

        issues = []
        sql = f"select * from issues where serviceagent = '{escape(email)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        dict = ibm_db.fetch_both(stmt)
        while dict != False:
            issues.append(dict)
            dict = ibm_db.fetch_both(stmt)
    if issues:    
     return render_template('mycom.html',issues=issues)


@app.route('/sendmail',methods =['GET','POST'])
def sendmail():
    return redirect(url_for('viewmine'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('mail', None)
    session.pop('password', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run( debug=True, port = 5000,host='0.0.0.0' )