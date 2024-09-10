class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"  # Added token type for multiplication
    DIV = "DIV"  # Added token type for division
    LPAREN = "LPAREN"  # Added token type for left parenthesis
    RPAREN = "RPAREN"  # Added token type for right parenthesis
    EOF = "EOF"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":  # Added handling for multiplication symbol
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":  # Added handling for division symbol
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":  # Added handling for left parenthesis
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":  # Added handling for right parenthesis
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise Exception("Lexical error")

        return Token(TokenType.EOF, None)

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Syntax error")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        # Method to handle numbers and expressions in parentheses
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:  # If left parenthesis, parse expression
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)  # Expect right parenthesis after expression
            return node

    def term(self):
        # Added support for multiplication and division operations
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        # Modified to support new operation hierarchy
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        if isinstance(node, Num):
            return self.visit_Num(node)
        elif isinstance(node, BinOp):
            return self.visit_BinOp(node)

    def visit_Num(self, node):
        return node.value

    def visit_BinOp(self, node):
        # Added handling for multiplication and division operations
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:  # Handling multiplication
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:  # Handling division
            return self.visit(node.left) / self.visit(node.right)

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

def main():
    while True:
        try:
            text = input('Enter expression (or "exit" to quit): ')
            if text.lower() == "exit":
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
