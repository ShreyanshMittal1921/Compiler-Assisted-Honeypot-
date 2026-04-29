def authenticate_user(username, password, mfa_token=None):
    # This is a different flavor of login function that should trigger the honeypot
    print(f"Authenticating {username}...")
    
    if username == "root" and password == "toor":
        return {"status": "success", "token": "jwt_token_here"}
    
    return {"status": "failed", "reason": "Invalid credentials"}
    
    # Optimizer should catch this dead code
    print("This should never execute")
    secret_internal_api_key = "sk_live_12345"

def login(user, passw):
    # A standard login wrapper
    return authenticate_user(user, passw)

# Execution payload
username = input("Enter API Username: ")
password = input("Enter API Password: ")
login(username, password)
