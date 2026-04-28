class ASTNode:
    pass

class Module(ASTNode):
    def __init__(self, body):
        # body is a list of ASTNode
        self.body = body

class FunctionDef(ASTNode):
    def __init__(self, name, body_block):
        self.name = name
        self.body = body_block

class Block(ASTNode):
    def __init__(self, statements):
        # statements is a list of ASTNode
        self.statements = statements

class Statement(ASTNode):
    def __init__(self, raw_code):
        self.raw_code = raw_code

class ReturnStatement(ASTNode):
    def __init__(self, raw_code, return_value_str=""):
        self.raw_code = raw_code
        self.return_value_str = return_value_str

class Assignment(ASTNode):
    def __init__(self, raw_code, target, value_str=""):
        self.raw_code = raw_code
        self.target = target
        self.value_str = value_str
def get_indent(line_str):
    """Returns the leading whitespace string of a line."""
    return line_str[:len(line_str) - len(line_str.lstrip('\t '))]

class Parser:
    def __init__(self, tokens, source_code):
        self.tokens = tokens
        self.lines = source_code.splitlines(True) # Keep newlines
        
        # Group tokens by line number
        self.tokens_by_line = {}
        for t in self.tokens:
            if t.line not in self.tokens_by_line:
                self.tokens_by_line[t.line] = []
            self.tokens_by_line[t.line].append(t)

    def parse(self):
        """Builds and returns the Module AST."""
        body = []
        i = 0
        total_lines = len(self.lines)
        
        while i < total_lines:
            line_str = self.lines[i]
            line_num = i + 1
            
            # Skip empty lines or purely whitespace lines
            if not line_str.strip():
                body.append(Statement(line_str))
                i += 1
                continue
                
            line_tokens = self.tokens_by_line.get(line_num, [])
            
            # Check for Function Definition: 'def' <name>
            is_func_def = False
            func_name = None
            
            if len(line_tokens) >= 2:
                # Discard NEWLINE and COMMENT tokens at start of line
                sig_tokens = [t for t in line_tokens if t.type not in ('NEWLINE', 'COMMENT')]
                if len(sig_tokens) >= 2:
                    if sig_tokens[0].type == 'IDENTIFIER' and sig_tokens[0].value == 'def':
                        if sig_tokens[1].type == 'IDENTIFIER':
                            is_func_def = True
                            func_name = sig_tokens[1].value
            
            if is_func_def:
                # We found a function definition.
                # Find its block by looking at indentation of subsequent lines.
                def_indent = get_indent(line_str)
                block_statements = []
                
                # The function definition line itself needs to be retained visually or we can regenerate it.
                # We'll regenerate it cleanly in codegen, so we only need to capture the block.
                # Let's save the exact definition signature if we want, but since we are simple, 
                # we only need to regenerate `def name(...):`. Wait, we might lose arguments!
                # Better solution: our generic Statement node for the `def` line, and the Block node attached to FunctionDef.
                # Actually, our AST logic:
                # FunctionDef will hold the raw signature as a string so we don't lose params!
                signature_stmt = Statement(line_str)
                
                i += 1
                while i < total_lines:
                    next_line_str = self.lines[i]
                    if not next_line_str.strip():
                        # Blank lines inside a function are part of its block
                        block_statements.append(Statement(next_line_str))
                        i += 1
                        continue
                        
                    next_indent = get_indent(next_line_str)
                    
                    # If the next line has strictly greater indentation, it's inside the function.
                    # Or if it's a comment with same or greater indentation.
                    # Simplest check: startswith def_indent + at least one space/tab
                    if len(next_indent) > len(def_indent) and next_line_str.startswith(def_indent):
                        # Inside block
                        block_statements.append(self._parse_line_statement(next_line_str, i+1))
                        i += 1
                    else:
                        break # End of block
                
                func_node = FunctionDef(func_name, Block(block_statements))
                func_node.signature = signature_stmt
                body.append(func_node)
            else:
                # Normal Statement
                body.append(self._parse_line_statement(line_str, line_num))
                i += 1
                
        return Module(body)

    def _parse_line_statement(self, line_str, line_num):
        """Helper to parse a single line into a more specific statement type."""
        line_tokens = self.tokens_by_line.get(line_num, [])
        # Filter out comments and newlines
        sig_tokens = [t for t in line_tokens if t.type not in ('NEWLINE', 'COMMENT')]
        
        if not sig_tokens:
            return Statement(line_str)
            
        # Check for Return
        if sig_tokens[0].type == 'IDENTIFIER' and sig_tokens[0].value == 'return':
            val_str = " ".join([t.value for t in sig_tokens[1:]])
            return ReturnStatement(line_str, val_str)
            
        # Check for Assignment (var = value)
        if len(sig_tokens) >= 3 and sig_tokens[0].type == 'IDENTIFIER' and sig_tokens[1].type == 'SYMBOL' and sig_tokens[1].value == '=':
            target = sig_tokens[0].value
            val_str = " ".join([t.value for t in sig_tokens[2:]])
            return Assignment(line_str, target, val_str)
            
        # Default fallback
        return Statement(line_str)

