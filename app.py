from flask import Flask,jsonify,render_template,request
import os
import socket
app=Flask(__name__)

#find the hostname and machine ip


def findhostname():
    hostname=socket.gethostname()
    hostip=socket.gethostbyname_ex(hostname)
    return str(hostname),str(hostip)

def get_public_ip():
    
    response = request.get_data('https://api.ipify.org').text
    return response

def reverse_ip(ip):
    segments = ip.split('.')
    reversed_ip = '.'.join(reversed(segments))
    return reversed_ip

#public_ip = get_public_ip()
#reversed_ip = reverse_ip(public_ip)
#print(f'Public IP: {public_ip}')
#print(f'Reversed IP: {reversed_ip}')

@app.route("/")
def home():
    
    return("You are highly welcome to my page")

@app.route("/ip")
def getip():
    public_ip = get_public_ip()


    return render_template('show.html',finalip=public_ip)

@app.route("/reverse")
def reverseip():
    
     reversed_ip = reverse_ip()
     return render_template('reverse.html',finalip=reversed_ip)

@app.route("/details")
def hostme():
    myhost,myip=findhostname()
    return render_template('index.html',host=myhost,IP=myip)
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5010,host="0.0.0.0")