def login(username, password):
    # This is a honeypot target function
    print("Welcome " + username)
    secret_token = "admin123"
    
    return True
    
    # This is dead code and should be removed by the Optimizer!
    print("This will never print")
    dead_var = "deleted"

def process_data(data):
    # Testing Taint Tracking on non-login functions
    db_password = "super_secret_db_pass"
    user_key = data
    return "processed"

# Main execution
a = "login please"
input_user = input("Username: ")
input_pass = input("Password: ")
login(input_user, input_pass)
