def login(username, password):
        # [INJECTED BY AST TRANSFORMER] Honeypot Telemetry
        import sys; from logger import log_attack
        if locals().get("username") == "admin" or locals().get("user") == "admin":
            payload = sys.argv[-1] if len(sys.argv) > 1 else "Unknown vector"
            log_attack(payload)
    # This is a honeypot target function
    print("Welcome " + username)
    secret_token = "admin123"
    
    return True
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
