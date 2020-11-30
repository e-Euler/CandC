from flask import Flask, render_template, send_from_directory, redirect, request, url_for, session
from pymongo import MongoClient
import os
import bcrypt
from classes.CandCdatabase import User_obj, Server_obj
import ifaddr
from classes.MicroServer import microServer
import random
import subprocess
from flask_socketio import SocketIO



client = MongoClient('localhost', 27017)
db = client['CandC']
currentUser = User_obj("","","",False)
app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio=SocketIO(app)


@app.route('/')
def login():
    return render_template('home.html', Name='e-Euler')

@app.route('/about')
def about():
    check()
    return "This is the about page"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/resources/background_img.png')
def background_img():
    return send_from_directory(os.path.join(app.root_path, 'resources'), 'background_img.png', mimetype='image/png')

@app.route('/dashboard')
def dashboard():
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    return render_template('dashboard.html', user=currentUser)

@app.route("/local", methods=["GET","POST"])
def local():
    output = "output area"
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    if request.method == "POST":
        command = request.form['command']
        cmdrun= subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        output = cmdrun.stdout.read().decode("utf-8")
    return render_template("local.html", user=currentUser,displayOut=output)


# Servers#################################################################
@app.route('/servers', methods=["POST","GET"])
def servers():
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    else:
        collection = db['CandC_servers']
        if request.method == "POST":
            if (request.form['server_type'] == "HTTP"):
                interface = request.form['interface']
                port = int(request.form['port'])
                servertype = request.form['server_type']
                microservice = microServer()
                microservice.runServer(interface,port)
                collection.insert({'server_id': random.randint(1000,9999), 'server_address': interface,'server_port':port, 'server_type':servertype})
            if (request.form['server_type'] == "tcp_shell"):
                print("****%s Still in Development****" % (request.form['server_type']))
            if (request.form['server_type'] == "SMB"):
                print("****%s Still in Development****" % (request.form['server_type']))
            if (request.form['server_type'] == "FTP"):
                print("****%s Still in Development****" % (request.form['server_type']))
            if (request.form['server_type'] == "HTTPS"):
                print("****%s Still in Development****" % (request.form['server_type']))

        addresses = []
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            for ip in adapter.ips:
                addresses.append(ip.ip)
        activeServers = collection.find()
        # interface = activeServers['server_id']
        # print("server interface is: %s" %(interface))
        return render_template('servers.html', user=currentUser, addresses=addresses,microservers=activeServers)
############################################################################

@app.route('/bots')
def bots():
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    return render_template('bots.html', user=currentUser)

#
# Administrative functions
#
#
@app.route('/administration')
def administration():
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    return render_template('administration.html', user=currentUser)

@app.route('/administration/adduser', methods=['POST'])
def adduser():
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    else:
        collection = db['CandC_auth']
        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        collection.insert({'username':request.form['username'],'password':hashpass,'role':request.form['role']})
    return redirect(url_for('administration'))

@app.route('/administration/deluser', methods=['POST'])
def deluser():
    logged_in = check()
    if logged_in is False:
        return redirect('/')
    else:
        collection = db['CandC_auth']
        collection.delete_one({'username':request.form['username']})
    return redirect(url_for('administration'))
#
# Authentication functions
#
#
def check():
    print("Checking active session: %s" %(session))
    logged_in = False
    try:
        if (session['username']) :
            logged_in = True
        else:
            logged_in = False
    except:
        return logged_in


#Authenticateion
@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    if request.method=='POST':
        collection = db['CandC_auth']
        #do some stuff for auth
        logging_user = collection.find_one({'username':request.form['username']}) 
        if logging_user is None:
            return("User %s Doesn't exist" %(request.form['username']))
        else:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), logging_user['password']) == logging_user['password']:
                currentUser.username = logging_user['username']
                currentUser.password = logging_user['password']
                currentUser.role = logging_user['role']
                currentUser.is_logged_in = True
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
        # credentials={'username':request.form['username'],'password':request.form['password']}
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    socketio.run(app, debug=True)
