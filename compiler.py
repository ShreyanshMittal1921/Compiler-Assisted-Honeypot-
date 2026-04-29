import os
from lexer import tokenize, CompilerSyntaxError
from parser import Parser, Module, FunctionDef, Block, Statement
from semantic import SemanticAnalyzer
from transformer import ASTTransformer
from codegen import CodeGenerator
from optimizer import ASTOptimizer

def dump_ast(node, indent=""):
    """Helper to convert the AST tree into a string showing the Grammar structure."""
    if isinstance(node, Module):
        res = f"{indent}Module:\n"
        for child in node.body:
            res += dump_ast(child, indent + "  ")
        return res
    elif isinstance(node, FunctionDef):
        res = f"{indent}FunctionDef (name='{node.name}'):\n"
        res += dump_ast(node.signature, indent + "  ")
        res += dump_ast(node.body, indent + "  ")
        return res
    elif isinstance(node, Block):
        res = f"{indent}Block:\n"
        for child in node.statements:
            res += dump_ast(child, indent + "  ")
        return res
    elif isinstance(node, Statement):
        # We need to import Assignment and ReturnStatement lazily or locally to avoid circulars, or just check class name
        class_name = node.__class__.__name__
        if class_name == 'Assignment':
            return f"{indent}Assignment (target='{node.target}', value='{node.value_str}')\n"
        elif class_name == 'ReturnStatement':
            return f"{indent}ReturnStatement (value='{node.return_value_str}')\n"
        return f"{indent}Statement: {repr(node.raw_code.strip())}\n"
    elif type(node).__name__ == 'Assignment':
        return f"{indent}Assignment: {repr(node.raw_code.strip())}\n"
    elif type(node).__name__ == 'ReturnStatement':
        return f"{indent}ReturnStatement: {repr(node.raw_code.strip())}\n"
    else:
        return f"{indent}UnknownNode: {type(node).__name__}\n"

def compile_code(input_file):
    print(f"\n--- Starting Compilation of {input_file} ---")
    trace = []
    
    # Create directory to save physical phase outputs
    steps_dir = "compiler_steps"
    os.makedirs(steps_dir, exist_ok=True)
    
    with open(input_file, "r", encoding="utf-8") as f:
        code_string = f.read()

    # == Phase 1: Lexical Analysis ==
    print("[1/6] Lexical Analysis...")
    tokens = tokenize(code_string)
    
    # Dump output
    out1_str = "=== LEXER TOKENS ===\nFormat: Token(TYPE, VALUE) at line#\n\n"
    for t in tokens:
        out1_str += f"Token({t.type}, {repr(t.value)}) @line {t.line}\n"
        
    with open(os.path.join(steps_dir, "step1_tokens.txt"), "w", encoding="utf-8") as f:
        f.write(out1_str)
            
    trace.append({
        "phase": "[1/6] LEXICAL ANALYSIS",
        "detail": f"Successfully mapped {len(tokens)} language tokens. Output saved to step1_tokens.txt",
        "output": out1_str
    })


    # == Phase 2: Parsing (AST Generation) ==
    print("[2/6] Parsing & AST Construction...")
    parser = Parser(tokens, code_string)
    ast = parser.parse()
    
    # Dump output
    out2_str = "=== ABSTRACT SYNTAX TREE (GRAMMAR) ===\n\n" + dump_ast(ast)
    with open(os.path.join(steps_dir, "step2_ast_grammar.txt"), "w", encoding="utf-8") as f:
        f.write(out2_str)

    trace.append({
        "phase": "[2/6] AST CONSTRUCTION",
        "detail": "Abstract Syntax Tree successfully built. Output saved to step2_ast_grammar.txt",
        "output": out2_str
    })


    # == Phase 3: Semantic Analysis (Symbol Table) ==
    print("[3/6] Semantic Analysis...")
    semantic_analyzer = SemanticAnalyzer()
    symtab = semantic_analyzer.analyze(ast)
    print(f"      -> Found Functions: {symtab.functions}")
    funcs_str = ", ".join(symtab.functions) if symtab.functions else "None detected"
    
    # Dump output
    out3_str = "=== SYMBOL TABLE & DATA FLOW ===\n\n"
    out3_str += f"Detected Function Signatures in Scope:\n"
    for func in symtab.functions:
        out3_str += f" - {func}()\n"
        
    out3_str += "\nVariables & Taint Analysis:\n"
    for scope in symtab.scopes:
        out3_str += f" Scope '{scope.name}':\n"
        for var, meta in scope.variables.items():
            taint_str = "[SENSITIVE/TAINTED]" if meta.get("tainted") else "[Clean]"
            out3_str += f"   * {var}: {taint_str}\n"
        if not scope.variables:
            out3_str += "   (none)\n"
            
    with open(os.path.join(steps_dir, "step3_semantic_symtab.txt"), "w", encoding="utf-8") as f:
        f.write(out3_str)

    trace.append({
        "phase": "[3/6] SEMANTIC ANALYSIS",
        "detail": f"Symbol Table & Taint Scope Extracted. Saved to step3_semantic_symtab.txt",
        "output": out3_str
    })

    # == Phase 4: AST Optimization ==
    print("[4/6] AST Optimization (Dead Code Elimination)...")
    optimizer = ASTOptimizer()
    ast, eliminated = optimizer.optimize(ast)
    
    out4_str = "=== OPTIMIZED ABSTRACT SYNTAX TREE ===\n\n"
    out4_str += f"Optimization Results: {eliminated} dead statement(s) removed.\n\n"
    out4_str += dump_ast(ast)
    with open(os.path.join(steps_dir, "step4_optimized_ast.txt"), "w", encoding="utf-8") as f:
        f.write(out4_str)

    trace.append({
        "phase": "[4/6] AST OPTIMIZATION",
        "detail": f"Optimization Pass (DCE) completed. Removed {eliminated} unreachable nodes. Saved to step4_optimized_ast.txt",
        "output": out4_str
    })

    # == Phase 5: AST Transformation (Instrumentation) ==
    print("[5/6] AST Transformation...")
    transformer = ASTTransformer(symtab)
    modified_ast = transformer.transform(ast)
    
    # Dump output
    out5_str = "=== TRANSFORMED ABSTRACT SYNTAX TREE ===\n\n"
    out5_str += "Notice the injected logic inside the function block below:\n"
    out5_str += dump_ast(modified_ast)
    with open(os.path.join(steps_dir, "step5_transformed_ast.txt"), "w", encoding="utf-8") as f:
        f.write(out5_str)

    if "login" in symtab.functions:
        trans_detail = "Injected zero-day Honeypot trap directly into the internal AST block of 'login'. Saved to step5_transformed_ast.txt"
    else:
        trans_detail = "Target 'login' not found. AST remained un-instrumented."
    trace.append({
        "phase": "[5/6] AST TRANSFORMATION",
        "detail": trans_detail,
        "output": out5_str
    })


    # == Phase 6: Code Generation ==
    print("[6/6] Code Generation...")
    codegen = CodeGenerator()
    final_code = codegen.generate(modified_ast)
    
    # Dump dummy function string as well
    dummy_function = ""
    if "login" not in symtab.functions:
        dummy_function = '''
# Dummy function to prevent crash
def login(user, password):
    print("Login function executed")

'''

    # We save final output to the expected file
    output_path = "output_program.py"
    final_output_str = dummy_function + final_code
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output_str)
        
    trace.append({
        "phase": "[6/6] HONEYPOT INJECTED CODE",
        "detail": f"Tree un-parsed. Generated {len(final_code.splitlines())} lines of source code. Honeypot injected! Saved to {output_path}",
        "output": final_output_str
    })

    print("--- Compilation completed! --- \n")
    return trace