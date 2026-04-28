from parser import Module, FunctionDef, Block, Statement, get_indent

class ASTTransformer:
    def __init__(self, symtab):
        self.symtab = symtab

    def transform(self, ast_node):
        """Mutate the AST recursively."""
        self._visit(ast_node)
        return ast_node # Return the mutated AST

    def _visit(self, node):
        if isinstance(node, Module):
            for child in node.body:
                self._visit(child)
                
        elif isinstance(node, FunctionDef):
            # Check if this is the target function
            if node.name == "login":
                self._inject_trap(node)
                
            self._visit(node.body)
            
        elif isinstance(node, Block):
            for child in node.statements:
                self._visit(child)

    def _inject_trap(self, func_node):
        """Injects honeypot trap Statement nodes into the FunctionDef block."""
        # Determine base indentation for the block
        base_indent = ""
        if func_node.body.statements:
            first_stmt = func_node.body.statements[0].raw_code
            if first_stmt.strip():
                base_indent = get_indent(first_stmt)
                
        if not base_indent:
            # Fallback if function is completely empty
            def_indent = get_indent(func_node.signature.raw_code)
            base_indent = def_indent + "    "
            
        # The trap logic to inject
        trap_lines = [
            '    # [INJECTED BY AST TRANSFORMER] Honeypot Telemetry\n',
            '    import sys; from logger import log_attack\n',
            '    if locals().get("username") == "admin" or locals().get("user") == "admin":\n',
            '        payload = sys.argv[-1] if len(sys.argv) > 1 else "Unknown vector"\n',
            '        log_attack(payload)\n'
        ]
        
        # We model the injection by injecting new AST Statement nodes.
        # Notice how Code Transformation strictly operates on the node level.
        # We prepend base_indent to each line so it matches the block accurately.
        injected_nodes = []
        for line in trap_lines:
            # We enforce block scoping by appending the calculated indent
            injected_nodes.append(Statement(base_indent + line))
            
        # Prepend the trap to the start of the function block
        func_node.body.statements = injected_nodes + func_node.body.statements
        print(f"[COMPILER: TRANSFORMER] Injected honeypot trap into internal AST of '{func_node.name}'")
