import psycopg2
import psycopg2.extras

class DatabaseHandler:
    def __init__(self):
        #set up db- credentials
        self.hostname ="127.0.0.1"
        self.database = "dmv_bot"
        self.username = "postgres"
        self.pwd = "postgres"
        self.port_id = 5432
        self.conn = None
        self.cur = None

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(
                host = self.hostname,
                dbname = self.database,
                user = self.username,
                password = self.pwd,
                port = self.port_id
            )
            self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

            #clean up db to drop the table 
            self.cur.execute('DROP TABLE IF EXISTS record')
            self.cur.execute('DROP TABLE IF EXISTS member')


            #create table- member
            create_member_script = '''CREATE TABLE IF NOT EXISTS member(
                                id bigint UNIQUE,
                                name varchar(30) NOT NULL,
                                email varchar(80) NOT NULL UNIQUE)'''

            create_record_script = '''CREATE TABLE IF NOT EXISTS record(
                                member_id bigint UNIQUE,
                                input_date date NOT NULL,
                                input_zipcode int NOT NULL,
                                mile int,
                                FOREIGN KEY (member_id) REFERENCES member (id) ON DELETE CASCADE)'''

            self.cur.execute(create_member_script)
            self.cur.execute(create_record_script)

            self.conn.commit()
            print("it's connecting to the database.....")

        except Exception as error:
            print(error)


    def run_query(query):
        self.cur.execute(query)


    def get_db_cursor(self):
        return self.cur
        
    def close_db(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        print("Database connection closed")

    #create a member
    def insert_member(self,user_id,email,name):
        print("insert_member check cur and conn: ", self.conn, self.cur)
        try:
            #insert data in table
            insert_script = 'INSERT INTO member (id,name,email) VALUES(%s,%s,%s)'
            insert_values=[(user_id,name,email)]
            for val in insert_values:
                self.cur.execute(insert_script,val)
                self.conn.commit()
            print("insert successfully!!", email , name)
        except Exception as error:
            print("insert_member error: ",error)

    #create a record
    def insert_record(self,user_id,input_date, input_zipcode, mile=0):
        print("insert_record--user_id,input_date, input_zipcode, mile: ",type(user_id),type(input_date), type(input_zipcode), type(mile))
        print("insert_record check cur and conn: ", self.conn, self.cur)
        try:
            insert_script = 'INSERT INTO record (member_id,input_date,input_zipcode,mile) VALUES(%s,%s,%s,%s)'
            insert_values=(user_id,input_date, input_zipcode, mile)
            self.cur.execute(insert_script,insert_values)
            self.conn.commit()
            print("insert_record successfully!!")
        except Exception as error:
            print("insert_record error: ",error)

    
    #find a member
    def find_the_member(self, user_id):
        print("find_the_member check cur and conn: ", self.conn, self.cur)

        print("find_the_member user_id: ",user_id, type(user_id))
        self.cur.execute('SELECT * FROM member WHERE id = %s',(user_id,))
        member = self.cur.fetchone()
        print("find the member: ", member)
        if member is not None:
            return True
        else:
            return False

    #find record
    def find_member_record(self, user_id):
        print("find_member_record check cur and conn: ", self.conn, self.cur)

        print("view_user_record user_id: ",user_id, type(user_id))
        self.cur.execute('SELECT * FROM record WHERE member_id = %s',(user_id,))
        record = self.cur.fetchone()
        print("what i get from record: ", record)
        if record is not None:
            return True
        return False
    


