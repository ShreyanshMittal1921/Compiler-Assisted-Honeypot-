from lexer import tokenize

def inject_honeypot(source_code):
    """
    Takes raw source_code string, tokenizes it to find lines containing actual
    'login' identifiers, and injects traps after those lines.
    """
    # 1. Lexical Analysis (from scratch tokenizer)
    tokens = tokenize(source_code)
    
    # 2. Find target lines (only targeting IDENTIFIER tokens)
    target_lines = set()
    for token in tokens:
        if token.type == 'IDENTIFIER' and token.value == 'login':
            target_lines.add(token.line)
            
    # 3. Code Generation / Injection
    original_lines = source_code.splitlines(True)
    injected_code = []
    
    trap = '''
print("Honeypot Active")
user_input = input("Enter value: ")
print("You entered:", user_input)
from logger import log_attack
log_attack(user_input)
'''

    for i, line in enumerate(original_lines):
        line_number = i + 1
        injected_code.append(line)
        
        if line_number in target_lines:
            # Determine the correct indentation for the trap
            leading_chars = len(line) - len(line.lstrip())
            indent = line[:leading_chars]
            if line.strip().endswith(':'):
                indent += '    '
                
            indented_trap = '\n'.join([indent + t_line if t_line.strip() else t_line for t_line in trap.strip('\n').split('\n')])
            
            # Inject the trap directly after the line containing 'login'
            if not line.endswith('\n'):
                injected_code.append('\n')
            injected_code.append(indented_trap + '\n')
            
    return injected_code