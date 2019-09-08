#!/usr/bin/python3
"""
Created on Sun Sep 8 2:06:19 2019
@author: Pavel Semenov

Copy it but remember me

Thanks to Wes McKinnes and pandas.pydata.org for coding corrections. 
"""

import pandas as pds 
import numpy as np
import matplotlib.pyplot as mplot
#import seaborn as sn
#import statistics as sta #may be useful
#import pymongo # not availble so not pip installed so next best sql. 
import sqlite3 # will use sqlite3 with real SQLanguage instead of pymongo 

data = pds.read_csv('movie_metadata.csv')
col_start = 1
col_end = len(data)
df = pds.DataFrame(data,index=list(range(col_start,col_end)),columns=["director_name","genres","gross","budget"])
dfa = pds.DataFrame(data,index=list(range(col_start,col_end)),columns=list(data[0:]))

# 1. Import the file into a local db
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False) 
dfa.to_sql('MovieDB', con=engine)
#print(engine.execute("SELECT director_name, genres, budget FROM MovieDB").fetchall())

# b. Compute the top 10 genres in decreasing order by their profitability.
print(pds.read_sql_query('SELECT director_name, genres, budget, gross, (gross - budget) as profit FROM MovieDB GROUP BY genres ORDER BY profit DESC LIMIT 11', engine))

TopTenDescProfithtml = pds.read_sql_query('SELECT director_name, genres, budget, gross, (gross - budget) as profit FROM MovieDB GROUP BY genres ORDER BY profit DESC LIMIT 11', engine).to_html()
#print(TopTenDescProfit)

#print("\n\n Favorite Genras")
#print(pds.read_sql_query('SELECT director_name, genres, budget, gross, (gross - budget) as profit FROM MovieDB WHERE genres LIKE "%Sci-Fi" GROUP BY genres ORDER BY profit DESC LIMIT 11', engine))

def RESTapiserv(TopTenDescProfit):
  import socket
  port = 80
  host = '0.0.0.0'
  table=str(TopTenDescProfit)
  sitehtml='<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><body><h1>Act </h1>'+table+'</body></html>'
  site_length=str(len(sitehtml))
  on_RESTGET_send='HTTP/1.0 200 OK\r\nContent-Length: '+site_length+'\r\n\r\n '+sitehtml
  sitebytes=bytes(on_RESTGET_send, 'utf-8')
  sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock.bind((host,port))
  sock.listen(5)
  while port:
      conn, addr = sock.accept()
      conn.send(sitebytes)
      sock.close()

RESTapiserv(TopTenDescProfithtml)



