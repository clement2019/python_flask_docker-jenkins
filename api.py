from flask import Flask,render_template,redirect,url_for
from flask_mysqldb import MySQL
import requests  
import mysql.connector 

app=Flask(__name__)

#find the hostname and machine ip

# MySQL configuration
app.config['MYSQL_HOST'] = 'database-01.cgcqqlhk3z2h.us-east-1.rds.amazonaws.com'  # MySQL host (e.g., localhost)
app.config['MYSQL_USER'] = 'admin'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # MySQL password
app.config['MYSQL_DB'] = 'database-01'  # MySQL database name



# Initialize MySQL
mysql = MySQL(app)

# Create 'messages' table if it doesn't exist
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS database-01 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reverse_ip TEXT
        )
    ''')
    mysql.connection.commit()
    cur.close()

def get_public_ip():
    response = requests.get('https://api.ipify.org').text
    return response

def reverse_ip(ip):
    segments = ip.split('.')
    reversed_ip = '.'.join(reversed(segments))
    return reversed_ip

public_ip = get_public_ip()
reversed_ip = reverse_ip(public_ip)
print(f'Public IP: {public_ip}')
print(f'Reversed IP: {reversed_ip}')

@app.route("/")
def home():
    public_ip = get_public_ip()
    reversed_ip = reverse_ip(public_ip)
    return render_template('index.html', reversed_ip=reversed_ip)


@app.route('/showip')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT reverse_ip FROM database-01')
    collected_ip = cur.fetchall()
    cur.close()
    return render_template('show.html', reverse_ip=collected_ip)

@app.route('/submit', methods=['POST'])
def submit():
    new_ip = requests.form.get('reverse_ip')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO database-01 (reverse_ip) VALUES (%s)', [new_ip])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('hello'))

    
    
if __name__ == '__main__':
    app.run(debug=True, port=3000,host="0.0.0.0")