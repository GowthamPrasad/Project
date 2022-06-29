# IMPORT REQUIRED PACKAGES AND LIBRARIES
import numpy as np
import string # FOR WORKING WITH STRINGS
import random # FOR PASSWORD GENERATION
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template # FOR FLASK AND RELATED FEATURES
import pickle
import speech_recognition as sr # GOOGLE SPEECH RECOGNITION API
import datetime # FOR TIMESTAMP
import hashlib # CALCULATING THE HASH IN ORDER TO ADD DIGITAL FINGERPRINTS TO THE BLOCKS
import json # TO STORE DATA IN BLOCKCHAIN
import sqlite3 as sql # TO STORE THE DATA
import smtplib # TO SEND EMAIL
from email.message import EmailMessage # TO SEND EMAIL


# BLOCKCHAIN CLASS
class Blockchain:
	# This function is created to create the very first block and set it's hash to "0"
    def __init__(self):
        self.chain = []
        self.create_block(message='alternate', proof=1, previous_hash='0')

	# This function is created to add further blocks into the chain
    def create_block(self, message, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'previous_hash': previous_hash,
                'message': message}
        self.chain.append(block)
        return block
	
	# This function is created to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
	
	# This is the function for proof of work and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
		
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
				
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
		
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
			
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()
			
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
		
        return True
    
# This Function used to generate password
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate_random_password():
	length = 10

	# shuffling the characters
	random.shuffle(characters)

	password = []
	for i in range(length):
		password.append(random.choice(characters))

	random.shuffle(password)

	# converting the list to string and printing the list
	return("".join(password))
    
        
#-------------------------------------------------------------------------------------------#
# FLASK APP #

# Flask app initialization
app = Flask(__name__)
app.secret_key = "super secret key"


# Rendering Home page - index.html
@app.route('/')
def home():
    

    return render_template('index.html')

# Rendering Medical Transcription page - sample.html
@app.route('/medtran')
def med():
    return render_template('sample.html')
    
# Medical Transcription process route
@app.route('/transcribe',methods=['POST','GET'])
def transcribe():
    global text
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source, listening the audio file and store in audio_text variable
    
    if request.method == 'POST':
        myfile = request.files['file']
    
    with sr.AudioFile(myfile) as source:
        audio_text = r.listen(source)

        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            # print(text)
            notif="Audio file transcribed successfully and stored in Blockchain!"

     
        except:
             print('Sorry...run again...')
    
    # write transcribed text to a text file 
    with open("test.txt", "w") as fo:
        fo.write(text)
    
        
    # Insert patient name, password and transcribed text into 'mt.db' 
    user_name=None
    password=None
    email=None
    password=generate_random_password() # Calling Password Generation function
    if request.method == 'POST':
        user_name=request.form['name']
        email=request.form['email']
        con = sql.connect('mt.db')
        print("Connected successfully")
        cur = con.cursor()
        cur.execute('INSERT INTO User(UserName,Password,File,Email) VALUES (?,?,?,?)',(user_name,password,text,email))
        con.commit()
        print("Data inserted successfully")
        con.close()


    # Send password to patient email address
    # Initialise EmailMessage()
    msg = EmailMessage()
    # message to be sent
    msg.set_content('Your password to access the medical report: '+password)

    msg['Subject'] = 'Password to access Medical Report | ABC Hospital'
    msg['From'] = "gowthamprasads17mss018@skasc.ac.in"
    msg['To'] = email

    # creates SMTP session
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # Authentication
    server.login("gowthamprasads17mss018@skasc.ac.in", "good luck bro")
    server.send_message(msg)
    server.quit()
    print("Password mailed successfully")


    return render_template('sample.html',notification=notif)
    # return render_template('sample.html',transcribed_text=text)
    #return redirect(url_for('mine_block',text=text))

    

# Rendering Access Document page - read.html
@app.route('/read')
def read():
    return render_template('read.html')

@app.route('/access',methods=['POST','GET'])
def access():
    if request.method == 'POST':
        user_name=request.form['name']
        password=request.form['password']
        con = sql.connect('mt.db')
        print("Connected successfully")
        cur = con.cursor()
        # statement=f"select * from user where UserName='{user_name}' and Password='{password}';"
        # cur.execute(statement)
        # if not cur.fetchone():
        #     return render_template('read.html',transcribed_text=statement)
        # else:
        #     return render_template('read.html',transcribed_text=statement)

        # res = cur.execute("select * from user where UserName=user_name and Password=password")
        # return render_template('read.html', users=res.fetchall())

        res=con.execute('select UserName from user where UserName=? and Password=?', (user_name,password)).fetchall()
        res1=con.execute('select File from user where UserName=? and Password=?', (user_name,password)).fetchall()
        return render_template('read.html', transcribed_text=res1)
    
    # else:
    #     flash('Invalid password or username!')
    #     return render_template('read.html')


# OBJECT CREATION FOR BLOCKCHAIN CLASS
blockchain = Blockchain()

# Mining a new block
@app.route('/block/', methods=['GET','POST'])
def mine_block():
    msg = text
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof) # Calling proof_of_work function
    previous_hash = blockchain.hash(previous_block) # Calling hash function
    message = msg
    block = blockchain.create_block(message, proof, previous_hash) # Calling create_block function with parameters
	
    response = {'message': block['message'],
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash']}
	
    return jsonify(response), 200

# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
    return jsonify(response), 200

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain) # Calling the chain_valid function
	
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
    
    
    
# EXECUTION OF FLASK APP
if __name__ == "__main__":
    app.run(debug=True)