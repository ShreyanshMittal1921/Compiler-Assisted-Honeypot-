from parser import Module, FunctionDef, Block, Assignment, ReturnStatement

class Scope:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.variables = {}  # var_name -> metadata dict

    def add_variable(self, name, is_sensitive=False):
        self.variables[name] = {
            "tainted": is_sensitive
        }

class SymbolTable:
    def __init__(self):
        self.functions = []
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scopes = [self.global_scope]

    def enter_scope(self, name):
        new_scope = Scope(name, parent=self.current_scope)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()

    def analyze(self, ast_node):
        """Walk the AST to extract semantic information into the SymbolTable."""
        self._visit(ast_node)
        return self.symtab

    def _visit(self, node):
        if isinstance(node, Module):
            for child in node.body:
                self._visit(child)
                
        elif isinstance(node, FunctionDef):
            # Record that this function is defined within the codebase scope
            self.symtab.functions.append(node.name)
            self.symtab.enter_scope(node.name)
            self._visit(node.body)
            self.symtab.exit_scope()
            
        elif isinstance(node, Block):
            for child in node.statements:
                self._visit(child)
                
        elif isinstance(node, Assignment):
            # Data Flow / Taint Analysis
            sensitive_keywords = ["password", "secret", "key", "token", "cred", "hash"]
            is_sensitive = any(kw in node.target.lower() for kw in sensitive_keywords)
            self.symtab.current_scope.add_variable(node.target, is_sensitive=is_sensitive)
