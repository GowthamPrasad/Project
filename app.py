# Import required packages and libraries
import numpy as np
import string
import random
from flask import Flask, request, redirect, url_for, jsonify, render_template
import pickle
import speech_recognition as sr
# For timestamp
import datetime
# Calculating the hash in order to add digital fingerprints to the blocks
import hashlib
# To store data in our blockchain
import json
import sqlite3 as sql


# Blockchain class
class Blockchain:
	# This function is created
	# to create the very first
	# block and set it's hash to "0"
    
    # message = 'index'
    def __init__(self):
        
        self.chain = []
        self.create_block(message='alternate', proof=1, previous_hash='0')

	# This function is created
	# to add further blocks
	# into the chain
    
   
    
    def create_block(self, message, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'previous_hash': previous_hash,
                'message': message}
        self.chain.append(block)
        return block
	
	# This function is created
	# to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
	
	# This is the function for proof of work
	# and used to successfully mine the block
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
    

## characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate_random_password():
	## length of password from the user
	length = 10

	## shuffling the characters
	random.shuffle(characters)
	
	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	return("".join(password))
    
        
#---------------------------------------------------------------------------

# Flask app initialization and opening the pickle file
app = Flask(__name__)

# Rendering Home page - input_design.html
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/medtran')
def med():
    return render_template('sample.html')
    
    
@app.route('/transcribe',methods=['POST','GET'])
def transcribe():    
    # Python code
    #import library

   
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    
    if request.method == 'POST':
        myfile = request.files['file']
    

    with sr.AudioFile(myfile) as source:
    
        audio_text = r.listen(source)
    
        #import pickle
        #pickle.dump(r,open('model_r.pkl','wb')) 
        #model = pickle.load(open('model_r.pkl','rb'))
    
        #recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            #print(text)
     
        except:
             print('Sorry...run again...')
    
    #write transcribed text to a text file    
    with open("test.txt", "w") as fo:
        fo.write(text)
        
    user_name=None
    password=None
    password=generate_random_password()
    if request.method == 'POST':
        user_name=request.form['name']
        con = sql.connect('mt.db')
        print("Connected successfully")
        cur = con.cursor()
        cur.execute('INSERT INTO User(UserName,Password,File) VALUES (?,?,?)',(user_name,password,text))
        con.commit()
        print("Data inserted successfully")
        con.close()

    #return render_template('sample.html',transcribed_text=text)
    return redirect(url_for('mine_block',text=text))
    
        
    

@app.route('/read',methods=['GET','POST'])
def read():
    
    return render_template('read.html')


#Create the object
#of the class blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/block/<text>', methods=['GET','POST'])
def mine_block(text):
    msg = text
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    message = msg
    block = blockchain.create_block(message, proof, previous_hash)
	
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
    valid = blockchain.chain_valid(blockchain.chain)
	
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
    
    
#@app.route('/')
#def main():
    # fo = open("test.txt","wb")
    # fo.write("This is Test Data")
    #with open("test.txt", "w") as fo:
        #fo.write("This is Test Data")
    
    #return render_template('sample.html')
    
# Execution
if __name__ == "__main__":
    app.run(debug=True)