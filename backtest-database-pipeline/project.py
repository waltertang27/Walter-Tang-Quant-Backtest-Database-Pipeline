
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from polygon import RESTClient
from flask import Flask, render_template
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Project_Data'
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
    v = db.Column(db.Float, primary_key = True)
    vw = db.Column(db.Float)
    o = db.Column(db.Float)
    c = db.Column(db.Float)
    h = db.Column(db.Float)
    l = db.Column(db.Float)
    t = db.Column(db.DateTime)
    n = db.Column(db.BigInteger)
    
def __init__(self, v, vw, o, c, h, l, t, n):
    self.v = v
    self.vw = vw
    self.o = o
    self.c = c
    self.h = h
    self.l = l
    self.t = t
    self.n = n

@app.route('/test', methods = ['GET'])
def test():
    return {
        'test': 'testing'
    }
db.create_all()
app.run()


