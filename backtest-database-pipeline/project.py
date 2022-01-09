
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from polygon import RESTClient
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy




    #importing the polygon client
key = "ozggTSfotBRqphmVTTL3tpakMp07rHMl"
client = RESTClient(key)
response = client.stocks_equities_aggregates('AAPL', multiplier = 1, timespan = 'hour', from_ = '2021-12-01', to = '2021-12-30')
data_frame = pd.DataFrame(response.results)
    #print(data_frame)
data_frame.to_csv('data/APPL.csv')
password = "password"
engine = create_engine('postgresql://postgres:{}@localhost/Project_Data'.format(password))
#temp_data = 'backtest-database-pipeline'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MOOIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Project_Data'
#app.debug = True
db = SQLAlchemy(app)



def create_table(symbol):
    df = pd.read_csv('{}/{}.csv'.format('data', symbol))
    #v,vw,o,c,h,l,t,n   
    df = df[['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n']]
    df['t'] = pd.to_datetime(df['t'])
    df = df.fillna(0)

    df.to_sql('prices', engine, if_exists = 'replace', index = False)


create_table('APPL')

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


#put link that is given in postman, and add /test at the end
@app.route('/test', methods = ['GET'])
def test():
    return {
        'test': 'testing'
    }
@app.route('/list', methods = ['GET'])
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
@app.route('/list', methods = ['POST'])
def postList():
    listData = request.get_json()
    listData['t'] = pd.to_datetime(listData['t'])
    x = listing(v = listData['v'], vw = listData['vw'], o = listData['o'], c = listData['c'], h = listData['h'], l = listData['l'], t = listData['t'], n = listData['n'])
    #x = listing(listData['v'], listData['vw'], listData['o'], listData['c'], listData['h'], listData['l'], listData['t'], listData['n'])
    #print(listData[0])
    db.session.add(x)
    db.session.commit()
    return jsonify(listData)

db.create_all()
app.run()


