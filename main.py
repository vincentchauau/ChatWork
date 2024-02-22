import os, json, re, sqlite3, pandas
from flask_sslify import SSLify
from lxml import etree
from flask import Flask, render_template,  send_file, request, json
from werkzeug.utils import secure_filename
app = Flask(__name__, template_folder='', static_folder='')
sslify = SSLify(app)
app.secret_key = "supersekrit"
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
#request.form/values - urlencoded #request.data - text/plain #request.args/files/json - json, file #json.loads(json.dumps(json object))
database = 'data.db'
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # Update UI with data
        con = sqlite3.connect(database)
        cur = con.cursor()
        try:
            values = request.values.to_dict()
            if values["command"] == "tables":
                data = getTables()
            elif values["command"] == "columns":
                data = getColumns(values["table"])
            elif values["command"] == "get":
                cur.execute(values["sql"])
                data = cur.fetchall()
            elif values["command"] == "insert":
                number = int(values["number"])
                for i in range(number):
                    cur.execute(values["sql"])
                cur.execute("SELECT LAST_INSERT_ROWID()")
                data = cur.fetchone()
            elif values["command"] == "delete":
                ids = values["id"].split(";")
                for id in ids:
                    cur.execute(values["sql"] + id)
            elif values["command"] == "set":
                sqls = values["sql"].split(";")
                for sql in sqls:
                    cur.execute(sql)
                data = ""
        except Exception as e:
            data = ""
        con.commit()
        con.close()
        return json.dumps(data)
    else: # Load UI without data
        return render_template('index.html')
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # app.root_path = os.path.dirname(app.instance_path)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.dirname(app.instance_path) +'\\upload\\' + secure_filename(file.filename))
            # return redirect(url_for(os.path.join('/upload/', filename)))
    return ""
def excel2sqlite(excel, sqlite):
    book = pandas.ExcelFile(excel)
    con = sqlite3.connect(sqlite)
    for sheet in book.sheet_names:
        df = pandas.read_excel(excel, sheet_name = sheet)
        df.to_sql(sheet,con, index = False, if_exists = "replace")
    con.commit()
    con.close()
@app.route('/loadexcel', methods = ['GET', 'POST'])
def loadexcel():
    if request.method == 'POST': # app.root_path = os.path.dirname(app.instance_path)
        file = request.files['file']
        if file:
            excel = os.path.dirname(app.instance_path) +'\\upload\\' + secure_filename(file.filename)
            file.save(excel)
            excel2sqlite(excel, database)
    return ""
def getTables():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT name from sqlite_master where type= "table"')
    result = []
    for member in cur.fetchall():
        if member[0] != "sqlite_sequence":
            result.append(member[0])
    con.close()
    return result
def getColumns(table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    result = [member[0] for member in cur.description]
    con.close()
    return result
def getValues(table, column):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT " + column + " FROM " + table)
    data = cur.fetchall()
    con.close()
    return data
def getRows(table, row):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    data = cur.fetchall()
    con.close()
    return data
@app.route('/<path:path>')
def dir_listing(path):
    path = os.path.abspath("./" + path)
    if os.path.isfile(path):
        return send_file(path)
    else:
        files = os.listdir(path)
        return render_template('files.html', files=files)
if __name__ == '__main__':
    app.run(port=5000, debug=True)