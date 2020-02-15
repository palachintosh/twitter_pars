import os 
import os.path
import sqlite3

class SaveTweets:
    def __init__(self, name=None, path_to_db=None):
        self.name = name
        self.path_to_db = path_to_db

        if self.name == None:
            self.name = 'twitter.db'
        
        #Set standard path if variable path_to_db is None
        if self.path_to_db == None:
            self.path_to_db = '/home/lesha/Python/django_project/request_log/'
            #self.path_to_db = str(self.path_to_db[0])
        else:
            try:
                if not os.path.exists(self.path_to_db):
                    #self.path_to_db = os.path.split(self.path_to_db)
                    os.mkdir(self.path_to_db)
                    print("Directory created successfull..")
            except OSError:
                print("Cann't create a directory! {}".format(self.path_to_db))
        

    def create_db(self):
        """Creating database if does not exist"""
        create = input("Do you want create new Data Base? y/n: ")
        if create == "y" or create == "Y":
            try:
                conn = sqlite3.connect(self.path_to_db + self.name) #('/home/lesha/Python/django_project/request_log/twitter.db')
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE tweets (id INTEGER PRIMARY KEY, created_at timestamp, user_name text, geo text, full_text text)""")
                conn.close()
                print("Database has been created successfully")
                return 1
            except:
                return "Error"
        

    def check_db(self):
        """Checking is database exists or not"""
        try:
            conn = sqlite3.connect('file:{}?mode=rw'.format(self.path_to_db + self.name), uri=True)
            print("Reading database..\n", "Done")
            conn.close()
            return 1
        except:
            print("Error: unable to open database. File not exist!")
            if self.create_db():
                return 0


    def add_to_db(self, data):
        """Add receive tweets to table"""

        if self.check_db():
            conn = sqlite3.connect(self.path_to_db + self.name)
            cursor = conn.cursor()
            print(data)

            try:
                cursor.executemany("INSERT INTO tweets VALUES (null,?,?,?,?)", data)
                conn.commit()
                conn.close()
                return 1
            except sqlite3.Error as e:
                print("SQLError.. : ", e)
                return "Unexpected SQLError.."
    
    def select_time_from_db(self):
        """Get last time of tweets """

        try:
            conn = sqlite3.connect(self.path_to_db + self.name, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = conn.cursor()
            cursor.execute("SELECT created_at FROM tweets ORDER BY id DESC LIMIT 1")
            returned_timestamp = cursor.fetchone()[0]
            conn.close()
            return returned_timestamp

        except sqlite3.Error as e:
            return e




# if __name__ == "__main__":
#     d = SaveTweets(name="my_db", path_to_db="/home/my_tw_db/")
#     d.check_db()
    #d.select_time_from_db()
