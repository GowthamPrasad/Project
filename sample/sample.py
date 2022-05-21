from flask import *  
import sqlite3  
from werkzeug import secure_filename

UPLOAD_FOLDER = 'C://Users/goutham/Documents/5th year/Project/sample'
app = Flask(__name__)

@app.route("/")  
def index():  
    return render_template("index.html");  
    
@app.route("/add")  
def add():   
    return render_template("add.html")  

############################################################################################    

# @app.route("/savedetails",methods = ['GET','POST'])  
# def saveDetails():  
    # msg = "msg"  
    # if request.method == "POST":
        # try:  
            # id = request.form["id"]  
            # name = request.form["name"]  
            # file = request.files["file"]
            # print(id)
            # print(name)
            # print(file)
            # # with open(file, 'rb') as files:
                # # blobData = files.read()
            # # print(blobData)
            # # filename = secure_filename(file.filename)
            # # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            
            # # with open("C://Users/goutham/Documents/5th year/Project/sample/file", 'r') as f:
                # # file_content = f.read()
            
            # with sqlite3.connect("sample.db") as con:  
                # cur = con.cursor()   
            # cur.execute("INSERT into sample (id, name, file) values (?,?,?)",(id,name,file))  
            # con.commit()  
            # msg = "Student successfully Added"   
        # except:  
            # con.rollback()  
            # msg = "We can not add the Student to the list"  
        # finally:  
            # return render_template("success.html",msg = msg)
    # con.close()
    
#############################################################################################

#############################################################################################

# @app.route("/savedetails",methods = ["GET", "POST"])
# def savedetails():  
    # msg = "msg"  
    # if request.method == "POST":  
        # try:  
            # sqliteConnection = sqlite3.connect("sample.db")
            # cur = sqliteConnection.cursor()
            # print("Connected to SQLitessssss")
            
            # id = request.form["id"]  
            # name = request.form["name"]  
            # file = request.files["file"]
            # print(id)
            # print(name)
            # print(file)
            # sqlite_insert_blob_query = "INSERT INTO sample (id, name, file) VALUES (?, ?, ?)"
            # # filename = secure_filename(file.filename) 
            # # file.save(os.path.join(app.config['UPLOAD_FOLDER'], (file.filename))
            
            
                                         
            # #record = convertToBinaryData(file)
            # with open(file, 'rb') as f:
                # file_content = f.read()
                
            # data_tuple = (id, name, file_content)
            
            # cur.execute(sqlite_insert_blob_query, data_tuple)
            # sqliteConnection.commit()
            # # with open(file, 'rb') as files:
                # # blobdata = files.read()
            
            # # binarray = ' '.join(format(ch, 'b') for ch in bytearray(blobdata))

            # # cur.execute("INSERT into sample (id, name, file) values (?,?,?)",(id,name,record))
            # # con.commit()
            # msg = "Student successfully Added"   
            # print("Image and file inserted successfully as a BLOB into a table")
            # cur.close()
            
        # # except sqlite3.Error as error:
            # # con.rollback()
            # # print("Failed to insert blob data into sqlite table", error)
        # # finally:
            # # return render_template("success.html",msg = msg)
            # # if sqliteConnection:
                # # sqliteConnection.close()
                # # print("the sqlite connection is closed")
        
        # except:  
            # con.rollback()  
            # msg = "We can not add the Student to the list"  
        # finally:  
            # return render_template("success.html",msg = msg) 
                


# def convertToBinaryData(filename):
    # # Convert digital data to binary format
    # with open(filename, 'rb') as files:
        # blobData = files.read()
    # return blobData
    
#############################################################################################

#############################################################################################

@app.route("/savedetails",methods = ["POST", "GET"])
def savedetails():

#############################################################################################

@app.route("/view", methods = ["GET"])  
def view():  
    con = sqlite3.connect("sample.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from sample")   
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)  

# @app.route("/delete")  
# def delete():  
# return render_template("delete.html")  

# @app.route("/deleterecord",methods = ["POST"])   
# def deleterecord():  
    # id = request.form["id"]  
        # with sqlite3.connect("Student.db") as con:  
            # try:  
                # cur = con.cursor()  
                # cur.execute("delete from Student where id = ?",id)  
                # msg = "record successfully deleted"   
            # except:  
                # msg = "can't be deleted"  
            # finally:  
                # return render_template("delete_record.html",msg = msg)  
                
if __name__ == "__main__":  
    app.run(debug = True)