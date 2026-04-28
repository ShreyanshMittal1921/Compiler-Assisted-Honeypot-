from parser import Module, FunctionDef, Block, Statement, Assignment, ReturnStatement

class CodeGenerator:
    def __init__(self):
        self.output = []

    def generate(self, ast_node):
        """Un-parse the AST back into string source code."""
        self.output = []
        self._visit(ast_node)
        return "".join(self.output)

    def _visit(self, node):
        if isinstance(node, Module):
            for child in node.body:
                self._visit(child)
                
        elif isinstance(node, FunctionDef):
            # Output the signature exactly as it was
            self._visit(node.signature)
            # Output the inner block
            self._visit(node.body)
            
        elif isinstance(node, Block):
            for child in node.statements:
                self._visit(child)
                
        elif isinstance(node, (Statement, Assignment, ReturnStatement)):
            self.output.append(node.raw_code)
