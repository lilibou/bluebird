import csv
import time
import os
import psycopg2 as pg
import json

class DataWriterInterface:
    """ Provides a common interface for writing to CSV/SQL 
    """

    def append(self, data):
        """ Adds a row of data.
        """
        raise NotImplementedError

    def stop(self):
        """ Closes the connection to the file
        """
        raise NotImplementedError

class CSVWriter(DataWriterInterface):
    def __init__(self, file_name=None, out_directory=None, row_names=None):
        """ file_name defaults to `bluebird_{current time}.csv` if not provided
        """
        is_new_file = False

        if file_name == None:
            assert(row_names)
            is_new_file = True
            current_time = int(time.time())
            file_name = "bluebird_{}.csv".format(current_time)  
        elif not os.path.isfile(file_name):
            # File the user has provided does not exist, and must be created
            is_new_file = True
            
            assert(row_names == None)

        if out_directory:
            file_name = os.path.join(out_directory, file_name)
           
            # Create the output directory if necessary
            if not os.path.isdir(out_directory):
                os.mkdir(out_directory)

        self.source_name = file_name
        self.row_names = row_names

        # "a" opens in append mode; creates the file if it does not exist
        self._file = open(self.source_name, "a", newline="", encoding="utf8")
        self.csv_writer = csv.writer(self._file)
        if new_file:
            # Write provided row names to the new file
            self.csv_writer.writerow(self.row_names)
        else:
            # Read row names of the existing file  
            reader = csv.reader(self._file)
            self.row_names = next(reader)

    def __del__(self):
        self._file.close() 

    def append(self, data):
        self.csv_writer.writerow(data)

class PSQLWriter:
    def __init__(self, db_config: str):
        """
        Connects to a PostgreSQL database described in the file passed 
        as `db_config`. Must contain the keys
         - host
         - port 
         - database
         - user
         - password
         - table
        All of these are standard save `table`, which is included since this
        script can't tell which one it should write to. The provided table must 
        have the correct column names (``, ``, ``, ``) otherwise it will break.
        """
        self._conn = None
        dbinfo = None

        with open(db_config) as json_file:
            dbinfo = json.load(json_file)

        self.TABLENAME = dbinfo["table"]

        try:
            self._conn = pg.connect(
                host=dbinfo["host"]
                database=dbinfo["database"],
                user=dbinfo["user"],
                password=dbinfo["password"],
                port=dbinfo["port"])
        except (Exception, pg.DatabaseError) as error:
            raise RuntimeError(f"Couldn't connect to the database: \n{error}")
            

    def __del__(self):
        if self._conn:
            self._conn.close()
            

