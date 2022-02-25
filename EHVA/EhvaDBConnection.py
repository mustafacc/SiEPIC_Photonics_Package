
import pandas as pd
import mysql.connector

class EhvaDBConnection:
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        
    def connect(self):
        self.cnx = mysql.connector.connect(user = self.user,
                                       password = self.password,
                                           host = self.host,
                                       database = self.database)
        return self
        
        
    def query(self, command):
        cursor = self.cnx.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
        data = pd.DataFrame(result, columns=cursor.column_names)
        return data

    def disconnect(self):
        self.cnx.close()
        
    def __del__(self):
        self.disconnect()