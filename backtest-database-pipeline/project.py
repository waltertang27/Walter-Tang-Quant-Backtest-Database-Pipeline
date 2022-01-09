
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from polygon import RESTClient
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy




#importing the polygon client. 

key = "ozggTSfotBRqphmVTTL3tpakMp07rHMl"
client = RESTClient(key)
# reads the data from Polygon.io into a csv file (in this case, APPL wit one hour timespan from 12/1/2021 to 12/30/2021)
response = client.stocks_equities_aggregates('AAPL', multiplier = 1, timespan = 'hour', from_ = '2021-12-01', to = '2021-12-30')
data_frame = pd.DataFrame(response.results)

#converts to csv file. path contains name of csv file to be created
data_frame.to_csv('data/APPL.csv', index = False)
#password for PgAdmin4
password = "password"
engine = create_engine('postgresql://postgres:{}@localhost/Project_Data'.format(password))

#creates Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MOOIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Project_Data'
db = SQLAlchemy(app)


#creates the data table and sends to database
def create_table(symbol):
    df = pd.read_csv('{}/{}.csv'.format('data', symbol))
    #v,vw,o,c,h,l,t,n   
    df = df[['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n']]
    df['t'] = pd.to_datetime(df['t'])
    df = df.fillna(0)

    #sends to "prices" database
    df.to_sql('prices', engine, if_exists = 'replace', index = False)

#creates table for APPL csv file that we pulled earlier from polygon.io
create_table('APPL')

#class for intializing object for webserver
class listing(db.Model):
    __tablename__ = 'listings'
    v = db.Column(db.Float(), primary_key = True)
    vw = db.Column(db.Float(), nullable = False, default = 0)
    o = db.Column(db.Float(), nullable = False, default = 0)
    c = db.Column(db.Float(), nullable = False, default = 0)
    h = db.Column(db.Float(), nullable = False, default = 0)
    l = db.Column(db.Float(), nullable = False, default = 0)
    t = db.Column(db.DateTime(), nullable = False, default = 0)
    n = db.Column(db.BigInteger(), nullable = False, default = 0)
    
    def __init__(self, v, vw, o, c, h, l, t, n):
        self.v = v
        self.vw = vw
        self.o = o
        self.c = c
        self.h = h
        self.l = l
        self.t = t
        self.n = n


#TESTING: put link that is given in postman, and add /test at the end
@app.route('/test', methods = ['GET'])
def test():
    return {
        'test': 'testing'
    }

#used for posting/getting values to/from database

#put link that is given in postman, then add /list at the end
@app.route('/list', methods = ['GET'])
#get method; returns the current listings in the database
def getList():
    temp = listing.query.all()
    output = []
    for i in temp:
        curList = {}
        curList['v'] = i.v
        curList['vw'] = i.vw
        curList['o'] = i.o
        curList['c'] = i.c
        curList['h'] = i.h
        curList['l'] = i.l
        curList['t'] = i.t
        curList['n'] = i.n
        output.append(curList)
    return jsonify(output)
#post method, adds a listing into database
@app.route('/list', methods = ['POST'])
def postList():
    listData = request.get_json()
    listData['t'] = pd.to_datetime(listData['t'])
    x = listing(v = listData['v'], vw = listData['vw'], o = listData['o'], c = listData['c'], h = listData['h'], l = listData['l'], t = listData['t'], n = listData['n'])
    db.session.add(x)
    db.session.commit()
    return jsonify(listData)

db.create_all()
app.run()


