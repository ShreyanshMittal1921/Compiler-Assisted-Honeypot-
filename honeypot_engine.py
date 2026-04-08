def inject_honeypot(code_lines):
    injected_code = []

    for line in code_lines:
        injected_code.append(line)

        if "login" in line:
            trap = '''
print("Honeypot Active")

user_input = input("Enter value: ")

print("You entered:", user_input)

from logger import log_attack
log_attack(user_input)
'''
            injected_code.append(trap)

    return injected_code