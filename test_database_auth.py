class DatabaseAuth:
    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "admin"
        
    def login(self, username, password):
        # The AST Transformer should identify this class method as a target
        print(f"Connecting to database {self.db_host}...")
        
        if username == "admin":
            return "Admin Access Granted"
        else:
            return "Access Denied"
            
        # Dead code to be stripped
        db_password = "super_secret_db_password_123"
        self.db_host = "192.168.1.100"

def init_system():
    auth_system = DatabaseAuth()
    # The compiler's taint tracking should pick this up
    admin_creds = "admin"
    auth_system.login(admin_creds, "password123")

init_system()
