# --- collecting all .csv files from folder and concatenate
import pandas as pd
import sqlite3
from glob import glob
from datetime import datetime
crime = sorted(glob('*.csv'))
df = pd.concat((pd.read_csv(file).assign(filename=file) for file in crime), ignore_index=True)

# --- cleaning date
df['Month']= pd.to_datetime(df['Month'],format="%Y-%m")
df['Year']= pd.DatetimeIndex(df['Month']).year
df['Quarter']= pd.DatetimeIndex(df['Month']).quarter
df['Month']= pd.to_datetime(df['Month'],format="%Y-%m").dt.strftime("%y-%m")

# --- cleaning text data

df['Location']=df['Location'].str.replace('On or near','')
df['LSOA name'] = df['LSOA name'].str.replace('\d+[A-Z]', '')

del df["filename"]
del df['Crime ID']

print(df.info())
# --- Load into SQL table

conn = sqlite3.connect('crime')
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS london (Month text, Reported by text, Falls within text,
Longitude REAL, Latitude REAL, Location text, LSOA name text, Crime type text,
Last outcome category text, Context text, Year integer, Quarter Integer )""")
conn.commit()

df.to_sql('london', conn, if_exists='replace', index = False)



