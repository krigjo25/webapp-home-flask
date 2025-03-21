#   Importing repositories
import logging
import requests
from typing import Optional,Tuple

from dotenv import load_dotenv
load_dotenv()

#   errorHandler
from errorHandler import OperationalError

#   Requests repositories
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

#   Configuring the logger
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    handlers=[logging.FileHandler("test-base-log.log"), 
              logging.StreamHandler()])

class DataBase():

    """ Base: What would includes in several databases"""
    def __init__(self, database: str, port: Optional[int] = None, host: Optional[str] = None):

        self.host = host
        self.port = port
        self.db = database
        self.statements = ['CREATE', "ALTER", 'DROP', 'INSERT', 'SELECT']

    
    def configure_columns(self,  table:str, statement:str, columns:list | tuple):
        
        #   Initialize variables
        row = []
        rows = []
        column = []
        tmp = ""

        if statement.upper() == "INSERT":

            for data in columns:

                for key, value in data.items():

                    #   Ensure that the key does not exists in column
                    if key not in column: column.append(key)
                    
                
            for data in columns:
                for key, value in data.items():

                    if type(value) == list or type(value) == tuple:
                        for i in value:
                            tmp += i
                        
                            row.append(i)
                    else:
                        row.append(value)

                    if len(row) == len(column):
                        rows.append(tuple(row))
                        row = []


            query = f"{statement} INTO {table}{tuple(column)} VALUES("
 
            for i in range(len(column)): 
                query+= "?," if i+1 < len(column) else f"?);"
        elif statement.upper() == "SELECT":

            for i in range(len(columns)):
                column += {columns[i]} if i != columns[-1] else columns[i]
            
            columns = column
            column = ""

            for i in range(len(columns)):
                column += columns[i] + "," if i +1 < len(columns) else f"{columns[i]}"
            
            query = f"{statement} {column} FROM {table};"

            return query

        #   Sweep memory
        del table, statement, columns
        del column,  row

        return [query, rows]
    
    def configure_table(self, table:str, statement:str, columns: dict | dict=None):

        #   Ensure that statement is equal to the listed  statement

        if statement in self.statements and bool(columns):
            query = f"{statement} TABLE IF NOT EXISTS {table}("

            #   Ensure that there is values in columns
            for key, value in columns.items():

                #   Append data
                query += f"{key} {value}"

                #   Ensure the list is not at end
                query += ',' if list(columns)[-1] != key else ');'

        #   Sweep data
        del table, statement, columns

        return query

    #  Universal methods
    def delete_row(self, table:str, column:str, value:str): return self.cur.execute(f"DELETE FROM {table} WHERE {column} = {value};")
    def drop_table(self, table:str): return self.cur.execute(f'DROP table IF EXISTS {table}')
    def drop_database(self, db:str): return self.cur.execute(f'DROP DATABASE IF EXISTS {self.db}')  

class APIConfig(object):

    def __init__(self, URL, KEY=None, GET = "GET", POST = "POST", PUT='PUT', PATCH='PATCH', DELETE = 'DELETE'):
        self.GET = GET
        self.POST = POST
        self.PUT = PUT
        self.PATCH = PATCH
        self.DELETE = DELETE
        self.API_KEY = KEY
        self.API_URL = URL

    def ApiCall(self, endpoint: str, head: dict):
        """
            Calling the API
        """
        r = requests.get(f"{endpoint}", timeout=30, headers=head)

        try:
            
            #   Ensure that the status code is 200 / 201
            if r.status_code in [200, 201]: 
                return r.json()
            
            #   Ensure that the status code is 401 / 403
            elif r.status_code in [401, 403]: 
                raise ConnectionError(f'Unauthorized Access')
            
            #   Ensure that the status code is 404
            elif r.status_code in [404]: 
                raise HTTPError(f'Resource not found')
            

        except (HTTPError, ConnectionError, Timeout, RequestException) as e: 

            error = f"Error {r.status_code}: {e}"
            logging.error(f"An error occured while attempting to call the api\n{error}")
            
            return error
        
    def ApiStatus(self, endpoint: str, head: dict):
        """
            Calling the API
        """
        r = requests.get(f"{endpoint}", timeout=30, headers=head)

        return r.status_code
