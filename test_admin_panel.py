def secure_login(username, password):
    # This should be skipped by the AST transformer if it only looks for exact "login" name
    # OR it might be caught if we do a substring match. Good test case!
    if username == "admin":
        print("Admin verified")
        return True
    return False

def login(user, pswd):
    # This will definitively trigger the AST transformer
    if user == "sysadmin" and pswd == "hunter2":
        return "Session Started"
    
    return "Session Failed"
    
    # Dead code after return
    admin_session_token = "ey123.abc.456"
    print("Debug: Session token is", admin_session_token)

# Taint tracking target
user_input = "sysadmin"
login(user_input, "test")
secure_login(user_input, "test")
