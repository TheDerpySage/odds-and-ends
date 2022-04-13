import sqlite3

# A Self Contained Database Wrapper

class Database:

    # Note: Primary Key ID's in SQLite start autoincrementing at 1

    def __init__(self, name=None):
        self.conn = None
        self.cursor = None
        if name:
            self.open(name)

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.close()

    def open(self,name):
        try:
            self.conn = sqlite3.connect(name);
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

    def close(self):
        '''Always remember to close properly for changes to be saved.'''
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def init(self,schema):
        '''Initializes the sqlite database using a schema file'''
        with open(schema) as fp:
            self.cursor.executescript(fp.read())

    def get_col(self,table,column,row):
        '''Gets and returns a single piece of data from the DB given:
        table = Name of the table
        column = Name of the column being read
        row = The number of the row (Primary Key ID)
        '''
        query = "SELECT %s FROM %s WHERE id = %s;" % (column, table, row)
        self.cursor.execute(query)
        data = list(self.cursor.fetchone())
        return data[0]

    def set_col(self,table,column,row,data):
        '''Sets a single piece of data from the DB given:
        table = Name of the table
        column = Name of the column being read
        row = The number of the row (Primary Key ID)
        data = The data to be written to this space'''
        query = "UPDATE %s SET %s = %s WHERE id = %s;" % (table, column, data, row)
        self.cursor.execute(query)

    def get_row(self,table,row):
        '''Gets and returns an entire row (in a list) of data from the DB given:
        table = Name of the table
        row = The number of the row (Primary Key ID)'''
        query = "SELECT * FROM %s WHERE id = %s;" % (table, row)
        self.cursor.execute(query)
        data = list(self.cursor.fetchone())
        return data

    def set_row(self,table,cols,data):
        '''Sets a brand new row of data from the DB given:
        table = Name of the table
        cols = A list of the names of the columns in the row
        data = A list of the new values to be written'''
        query = "INSERT INTO %s " % table
        query += "("
        for value in cols:
            query += ("%s, " % (value))
        query = query[:-2] + ") VALUES ("
        for value in data:
            query += ("'%s', " % (value))
        query = query[:-2] + ");"
        print(query)
        self.cursor.execute(query)

    def overwrite_row(self,table,cols,data,row):
        '''Overwrites a whole row of data from the DB given:
        table = Name of the table
        cols = A list of the names of the columns in the row
        data = A list of the new values to be written
        row = The number of the row (Primary Key ID)'''
        query = "UPDATE %s SET " % table
        for x in range(0, len(cols)):
            query += ("%s='%s', " % (cols[x],data[x]))
        query = query[:-2] + (" WHERE id = %s" % (row))
        print(query)
        self.cursor.execute(query)

    def query(self,sql):
        '''Executes a query based on a passed SQL Query:
        sql = A properly formatted SQL Query String'''
        self.cursor.execute(sql)

    def queryWithReturn(self,sql):
        '''Executes a query and returns 2D list based on a passed SQL Query:
        sql = A properly formatted SQL Query String'''
        self.cursor.execute(sql)
        temp = list(self.cursor.fetchall())
        for x in range(0, len(temp)):
            data[x] = list(temp[x])
        return data
