from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import pickle

app = Flask(__name__)
app.secret_key = 'mu$tRéMåiN$éC®eT'

# MySQL configurations
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'pass4739'
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Model
model = pickle.load(open('model.pkl','rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        hashed_password = generate_password_hash(password)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(username, password) VALUES(%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_details = request.form
        username = user_details['username']
        password = user_details['password']

        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * FROM user WHERE username = %s", [username])
        if result_value > 0:
            user = cur.fetchone()
            if check_password_hash(user[2], password):
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('predict'))
        cur.close()
    return render_template('login.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    result = ""
    if request.method == 'POST':
        gender=int(request.form['Gender'])
        married=int(request.form['Married'])
        dependents=float(request.form['Dependents'])
        education=int(request.form['Education'])
        self_employed=int(request.form['Self_Employed'])
        applicant_income=float(request.form['Applicant_Income'])
        coapplicant_income=float(request.form['Coapplicant_Income'])
        loan_amount=float(request.form['Loan_Amount'])
        loan_amount_term=float(request.form['Loan_Amount_Term'])
        credit_history=float(request.form['Credit_History'])
        property_area=int(request.form['Property_Area'])

        print(gender,married,dependents,education,self_employed,applicant_income,coapplicant_income,loan_amount,loan_amount_term,credit_history,property_area)
        
        prediction=model.predict([[gender,married,dependents,education,self_employed,applicant_income,coapplicant_income,loan_amount,loan_amount_term,credit_history,property_area]])
                
        if prediction[0] == 1:
            result="Congratulations. You are eligible for the loan!"
        else:
            result="Sorry. Your are not eligible for the loan...."
                
    return render_template('predict.html', message=result) 
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
