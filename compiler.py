from honeypot_engine import inject_honeypot
from lexer import CompilerSyntaxError

def compile_code(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        code_string = f.read()

    # The lexer inside will throw CompilerSyntaxError if syntax is malformed
    modified_code = inject_honeypot(code_string)

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