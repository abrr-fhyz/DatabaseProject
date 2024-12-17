import oracledb

class Config:
    def __init__(self, user, password, host, port, service_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name
    
    def get_connection(self):
        try:
            connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=f"{self.host}:{self.port}/{self.service_name}"
            )
            print("Oracle DB connection established.")
            return connection
        except oracledb.DatabaseError as e:
            print("Error connecting to the Oracle database:", e)
            raise

database_config = Config(
    user="c##project",
    password="project",
    host="localhost",        
    port="1521",                
    service_name="xe"
)
