from honeypot_engine import inject_honeypot

def compile_code(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        code = f.readlines()

    modified_code = inject_honeypot(code)

    # Add dummy login function at top
    dummy_function = '''
# Dummy function to prevent crash
def login(user, password):
    print("Login function executed")
'''

    with open("output_program.py", "w", encoding="utf-8") as f:
        f.write(dummy_function)
        f.writelines(modified_code)

    print("Compilation completed!")