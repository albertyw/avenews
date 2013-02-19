import MySQLdb
import unicodedata 

'''
This is a class for interaction with the mysql database
'''
class Mysql():
    '''
    Initialize the connection
    '''
    def __init__(self):
        self.db=MySQLdb.connect(host="localhost",user="avenews",passwd="F6mfT5RM3fBQjE7J",db="avenews")
        self.db.autocommit(True)
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
    def escape_string(self, inputString, normalize_String = False):
        if normalize_String:
            inputString = unicodedata.normalize('NFKD', inputString) 
            inputString = u''.join([c for c in inputString if not unicodedata.combining(c)])
        inputString = inputString.encode('utf-8')
        return self.db.escape_string(inputString)
        
    '''
    Get the ID of the last row that was inserted
    '''
    def get_last_insert_id(self):
        return self.db.insert_id()
        
    """
    Keep on yielding the result until no more rows are found
    """
    def iterate_rows(self):
        while True:
            row = self.fetch()
            if row == {}:
                break
            yield row


'''
swoopo = SwoopoDB()
query = "INSERT INTO Auctions (auctionid) VALUES('1')"
query = "SELECT * FROM Auctions"
swoopo.query(query)
print swoopo.fetch()
print swoopo.fetch()
'''
