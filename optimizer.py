from parser import Module, FunctionDef, Block, Assignment, ReturnStatement, Statement

class ASTOptimizer:
    """
    Compiler Optimization Phase.
    Implements Dead Code Elimination (DCE).
    """
    def __init__(self):
        self.eliminated_count = 0

    def optimize(self, ast_node):
        """Walk the AST and apply optimizations inline."""
        self.eliminated_count = 0
        self._visit(ast_node)
        return ast_node, self.eliminated_count

    def _visit(self, node):
        if isinstance(node, Module):
            for child in node.body:
                self._visit(child)
                
        elif isinstance(node, FunctionDef):
            self._visit(node.body)
            
        elif isinstance(node, Block):
            # Dead Code Elimination:
            # If we see a ReturnStatement, we delete everything after it in the same block.
            new_statements = []
            for stmt in node.statements:
                self._visit(stmt)
                new_statements.append(stmt)
                if isinstance(stmt, ReturnStatement):
                    # How many statements are we dropping?
                    dropped = len(node.statements) - len(new_statements)
                    self.eliminated_count += dropped
                    if dropped > 0:
                        print(f"[COMPILER: OPTIMIZER] Dead Code Elimination: removed {dropped} unreachable statement(s) after a return.")
                    break # Stop appending to new_statements once we hit a return
            
            node.statements = new_statements
