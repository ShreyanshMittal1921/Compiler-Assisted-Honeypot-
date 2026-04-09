
# Dummy function to prevent crash
def login(user, password):
    print("Login function executed")
def login(user):
    print("Honeypot Active")
    user_input = input("Enter value: ")
    print("You entered:", user_input)
    from logger import log_attack
    log_attack(user_input)
    print("Welcome " + user)

# testing login inside comment

a = "login please"

login("admin")
print("Honeypot Active")
user_input = input("Enter value: ")
print("You entered:", user_input)
from logger import log_attack
log_attack(user_input)
