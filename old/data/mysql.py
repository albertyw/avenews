import MySQLdb

'''
This is a class for interaction with the mysql database
'''
class Mysql():
    '''
    Initialize the connection
    '''
    def __init__(self):
        self.db=MySQLdb.connect(host="localhost",user="newsmap",passwd="J8jvEFyFTp5aqfGn",db="newsmap")
        pass
    '''
    Send a query to the database
    @param query: the query to send to the database
    '''
    def query(self, query):
        self.db.query(query)
        self.store_result = self.db.store_result()
        pass
    
    '''
    Fetch the next row returned from the database.  This assumes that the previous query was "SELECT"
    @return: a row in the database, as specified by the previous query
    '''
    def fetch(self):
        row = self.store_result.fetch_row(how=1)
        if len(row)==0:
            return dict({})
        else:
            return row[0]
        
    '''
    Escape special characters in a string for use in database
    @return: an escaped string
    '''
    def escape_string(self, inputString):
        return self.db.escape_string(inputString)

    '''
    Since mysql stores booleans as integers, this function converts integers back into booleans
    @param num: the mysql boolean
    @return: the Python (real) boolean
    '''
    def intToBoolean(self, num):
        if num==0:
            return False
        return True
    def booleanToInt(self, boolean):
        if boolean == True:
            return 1
        return 0
