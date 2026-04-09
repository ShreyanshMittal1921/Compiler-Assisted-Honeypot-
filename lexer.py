class CompilerSyntaxError(Exception):
    def __init__(self, message, line):
        super().__init__(message)
        self.message = message
        self.line = line

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line})"

def tokenize(source_code):
    tokens = []
    i = 0
    length = len(source_code)
    line = 1
    
    while i < length:
        char = source_code[i]
        
        # Track line numbers
        if char == '\n':
            tokens.append(Token('NEWLINE', char, line))
            line += 1
            i += 1
            continue
            
        # Ignore other whitespace characters unless in strings
        if char.isspace() and char != '\n':
            i += 1
            continue
            
        # Comments
        if char == '#':
            start = i
            while i < length and source_code[i] != '\n':
                i += 1
            tokens.append(Token('COMMENT', source_code[start:i], line))
            continue
            
        # Strings (Triple and Single)
        if char in ('"', "'"):
            quote_type = char
            start = i
            start_line = line
            is_multiline = False
            
            # Check for multi-line triple strings
            if i + 2 < length and source_code[i:i+3] == quote_type * 3:
                is_multiline = True
                quote_type = quote_type * 3
                i += 3
            else:
                i += 1
                
            # Scan until matching quote
            while i < length:
                if source_code[i] == '\n':
                    line += 1
                    if not is_multiline:
                        # Syntax Error: Unclosed single-line string
                        raise CompilerSyntaxError("Unterminated string literal", start_line)
                
                # Check closing condition based on type
                if not is_multiline and source_code[i] == quote_type:
                    i += 1
                    break
                if is_multiline and i + 2 < length and source_code[i:i+3] == quote_type:
                    i += 3
                    break
                    
                i += 1
            else:
                raise CompilerSyntaxError("Unexpected EOF while parsing string", start_line)
                
            tokens.append(Token('STRING', source_code[start:i], start_line))
            continue
            
        # Identifiers (Variables, Function names, Keywords)
        if char.isalpha() or char == '_':
            start = i
            while i < length and (source_code[i].isalnum() or source_code[i] == '_'):
                i += 1
            tokens.append(Token('IDENTIFIER', source_code[start:i], line))
            continue
            
        # Numeric literals
        if char.isdigit():
            start = i
            while i < length and (source_code[i].isdigit() or source_code[i] == '.'):
                i += 1
            tokens.append(Token('NUMBER', source_code[start:i], line))
            continue
            
        # Generic Symbols (Operators, Bracket, Quotes)
        tokens.append(Token('SYMBOL', char, line))
        i += 1

    return tokens
