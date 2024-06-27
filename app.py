from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import sqlite3
import hashlib 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 
database = "Database.db" 
app.secret_key = os.urandom(24)  # Generating a secure secret key
def init_db(): 
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    # Create users_auth table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Check if login table exists and create if it doesn't
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_auth'")
    if not cursor.fetchone(): 
        cursor.execute("""
            CREATE TABLE admin_auth (
                id TEXT,
                Password TEXT
            ) 
        """)
        print("Admin Auth table is created.")
    else:
        print("Admin Auth already exists.")

    # Check if room table exists and create if it doesn't
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='room'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE room (
                roomNumber TEXT,
                availability TEXT,
                cleaningStatus TEXT,
                price TEXT,
                bedType TEXT
            )
        """)
        print("Room table created.")
    else:
        print("Room table already exists.")

    # Check if employee table exists and create if it doesn't
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE employee (
                name TEXT,
                age TEXT,
                gender TEXT,
                job TEXT,
                salary TEXT,
                phone TEXT,
                cnic TEXT,
                email TEXT
            )
        """)
        print("Employee table created.")
    else:
        print("Employee table already exists.")

    # Check if driver table exists and create if it doesn't
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='driver'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE driver (
                name TEXT,
                age TEXT,
                gender TEXT,
                carCompany TEXT,
                carName TEXT,
                availability TEXT,
                carLocation TEXT
            )
        """)
        print("Driver table created.")
    else:
        print("Driver table already exists.")

    # Check if customer table exists and create if it doesn't
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customer'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE customer (
                id TEXT,
                number TEXT,
                name TEXT,
                gender TEXT,
                country TEXT,
                roomNumber TEXT,
                checkedIn TEXT,
                deposit TEXT,
                pending TEXT
            )
        """)
        print("Customer table created.")
    else:
        print("Customer table already exists.")

    conn.commit()
    conn.close()
    

   
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    error_message1 = ""
    error_message2 = ""
    error_message3 = ""

    if request.method == 'POST':
        name = request.form['Name1']
        email = request.form['Email']
        password = request.form['Password']

        # Check for email duplication
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_auth WHERE email=?", (email,))
        user = cursor.fetchone()
        if user:
            error_message3 = "Email already exists."
            return render_template('signup.html', error_message1=error_message1, error_message2=error_message2, error_message3=error_message3)
        
        # Store user data in the database
        cursor.execute("INSERT INTO users_auth (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()

        return render_template('reception.html', user_name=name)

    return render_template('signup.html', error_message1=error_message1, error_message2=error_message2, error_message3=error_message3)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']

        # Retrieve user from the database
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_auth WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user[3] == hashed_password:
                session['email'] = email  # Store user's email in session
                conn.close()
                return render_template('admin_dash.html', user_name=user[1])
            else:
                conn.close()
                error = "Password is incorrect!"
                return render_template('login.html', error_message=error)
        else:
            conn.close()
            error = "User doesn't exist!"
            return render_template('login.html', error_message=error)

    return render_template('login.html') 

@app.route('/auth_adm', methods=['GET', 'POST'])
def auth_adm():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['Password']

        # Retrieve admin from the database
        conn = sqlite3.connect("Database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin_auth WHERE id=?", (id,))
        admin = cursor.fetchone()

        if admin:
            if admin[0]== password:
                session['id'] = id  # Store admin id in session
                conn.close()
                return redirect(url_for('redr'))
            else: 
                conn.close()
                error = "Admin Id or Password is incorrect!"
                return render_template('admin_Auth.html', error_message=error) 
        else: 
            conn.close()
            error = "Invalid Input"
            return render_template('admin_Auth.html', error_message=error)

    return render_template('admin_Auth.html')

@app.route('/Admi')
def Admi():   
    return render_template('admin_dash.html') 
 
@app.route('/redr')
def redr():
    return render_template('redirectPage.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

@app.route('/reception_')
def reception_():   
     
    return render_template('reception.html')

 
@app.route('/CustomerFoam', methods=["POST"])
def CustomerFoam():  
    return render_template('newCustomerFoam.html')
  
@app.route('/ViewRooms', methods=["POST"])
def ViewRooms():  
    return render_template('rooms.html')

@app.route('/Employees', methods=["POST"])
def Employees():  
    return render_template('Employees.html')

@app.route('/CustInfo', methods=["POST"])
def CustInfo():  
    return render_template('CustomersInfo.html')

@app.route('/MgrInfo', methods=["POST"])
def MgrInfo():   
    return render_template('ManagerInfo.html')

@app.route('/PickupServ', methods=["POST"])
def PickupServ():   
    return render_template('PickupService.html')

@app.route('/SearchRoom', methods=["POST"])
def SearchRoom():   
    return render_template('SearchRoom.html')

@app.route('/Check_inUp', methods=["POST"])
def Check_inUp():    
    return render_template('CheckinDetail.html')

@app.route('/Room_add', methods=["POST"])
def Room_add():    
    return render_template('Add_Room.html')

@app.route('/Employee_add', methods=["POST"])
def Employee_add():   
    return render_template('Add_Employee.html')

@app.route('/Driver_add', methods=["POST"])
def Driver_add():   
    return render_template('Add_Driver.html')


@app.route('/homePage')
def logged(): 
    nname = session.get('_name') 
    return render_template('homePage.html', user_name=nname)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)