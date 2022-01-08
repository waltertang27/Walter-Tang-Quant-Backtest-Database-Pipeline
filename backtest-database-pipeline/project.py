
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from polygon import RESTClient



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



def create_table(symbol):
    df = pd.read_csv('{}/{}.csv'.format('data', symbol))
    #v,vw,o,c,h,l,t,n   
    df = df[['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n']]
    df['t'] = pd.to_datetime(df['t'])
    df = df.fillna(0)

    df.to_sql('prices', engine, if_exists = 'replace', index = False)


create_table('APPL')


