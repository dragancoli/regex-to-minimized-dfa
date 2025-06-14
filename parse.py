from lexer import TokenType, Lexer

# Osnovna klasa za sve cvorove
class INode():
    def __init__(self):
        pass

# Klasa za predstavljanje ILI operacije u AST
class OrNode(INode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

# Klasa za predstavljanje sekvence u AST
class SeqNode(INode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

# Klasa za predstavljanje operacije ponavljanja u AST
class StarNode(INode):
    def __init__(self, left):
        self.left = left

# Klasa za predstavljanje karaktera iz alfabeta u AST
class LiteralNode(INode):
    def __init__(self, char):
        self.char = char

# Klasa za predstavljanje operatora ponavljanja tacan broj puta u AST
class RepeatExactlyNode(INode):
    def __init__(self, left, num):
        self.left = left
        self.num = num

# Klasa za predstavljanje operatora ponavljanja izmedju granica u AST
class RepeatBetweenNode(INode):
    def __init__(self, left, low, high):
        self.left = left
        self.low = low
        self.high = high

# Klasa za predstavljanje operatora ponavljanja minimalan ili veci broj puta u AST
class RepeatMinNode(INode):
    def __init__(self, left, min):
        self.left = left
        self.min = min

# Ispisuje AST s odgovarajućim uvlačenjem.
# Asimptotska složenost: O(n), gdje je n broj čvorova u AST-u.
# idt - uvlacak relevantan samo za ispis
        
def print_ast(node, idt=0):
    node_type = type(node).__name__
    indent_str = ' ' * idt
    if node_type == 'OrNode':
        print(f"{indent_str}OR")
        print_ast(node.left, idt + 2)
        print_ast(node.right, idt + 2)
    elif node_type == 'SeqNode':
        print(f"{indent_str}SEQ")
        print_ast(node.left, idt + 2)
        print_ast(node.right, idt + 2)
    elif node_type == 'StarNode':
        print(f"{indent_str}STAR")
        print_ast(node.left, idt + 2)
    elif node_type == 'LiteralNode':
        print(f"{indent_str}LITERAL: {node.char}")
    elif node_type == 'RepeatExactlyNode':
        print(f"{indent_str}REPEAT_EXACTLY: {node.num}")
        print_ast(node.left, idt + 2)
    elif node_type == 'RepeatBetweenNode':
        print(f"{indent_str}REPEAT_BETWEEN: {node.low}-{node.high}")
        print_ast(node.left, idt + 2)
    elif node_type == 'RepeatMinNode':
        print(f"{indent_str}REPEAT_MIN: {node.min}")
        print_ast(node.left, idt + 2)
    else:
        raise Exception("Neocekivan tip AST cvora")

# Klasa za parser 
# Pretvara niz tokena u AST.
class Parser:
    def __init__(self, tokenStream):
        self.tokenStream = tokenStream
        self.currToken : int= 0
    
    #O(n), gdje je n broj tokena.
    def parse(self) -> INode:
        ast = self.expression()
        if self.currToken < len(self.tokenStream):
            raise Exception("Neocekivan token")
        return ast

    #O(n), gdje je n broj tokena.
    def expression(self):
        left_ast = self.term()
        if self.check(TokenType.OR):
            return OrNode(left_ast, self.expression())
        return left_ast
    
    #O(n), gdje je n broj tokena.
    def term(self):
        left_ast = self.character()
        while self.currToken < len(self.tokenStream):
            ttype = self.tokenStream[self.currToken].token_type
            if ttype not in [TokenType.LITERAL, TokenType.OPEN_PAREN]:
                break
            right_ast = self.term()
            left_ast = SeqNode(left_ast, right_ast)
        return left_ast

    #O(n), gdje je n broj tokena.
    def character(self):
        ast = None
        if self.check(TokenType.LITERAL):
            ast = LiteralNode(self.tokenStream[self.currToken - 1].content)
        elif self.check(TokenType.OPEN_PAREN):
            ast = self.expression()
            self.expect(TokenType.CLOSED_PAREN)
        else:
            raise Exception("Greska u parsiranju")
        if self.check(TokenType.OPEN_BRACE):
            left_ast = ast
            if self.tokenStream[self.currToken].token_type == TokenType.META_CHAR:
                if self.tokenStream[self.currToken + 1].token_type == TokenType.CLOSED_BRACE:
                    ast = RepeatExactlyNode(left_ast, self.tokenStream[self.currToken].content)
                    self.currToken += 1
                elif self.tokenStream[self.currToken + 1].token_type == TokenType.COMMA:
                    if self.tokenStream[self.currToken + 2].token_type == TokenType.META_CHAR:
                        ast = RepeatBetweenNode(left_ast, self.tokenStream[self.currToken].content, self.tokenStream[self.currToken + 2].content)
                        self.currToken += 3
                    elif self.tokenStream[self.currToken + 2].token_type == TokenType.CLOSED_BRACE:
                        ast = RepeatMinNode(left_ast, self.tokenStream[self.currToken].content)
                        self.currToken += 2
                self.check(TokenType.CLOSED_BRACE)
        if self.check(TokenType.STAR):
            ast = StarNode(ast)
        return ast

    # Provjerava da li je trenutni token ocekivani 
    # O(1)
    def check(self, token_type):
        if self.currToken < len(self.tokenStream): 
            currToken = self.tokenStream[self.currToken]
            if currToken.token_type == token_type:
                self.currToken += 1
                return True
            else:
                return False
        else:
            return False
    
    # Provjerava da li je naredni token ocekivani
    # Koristi se za ), } da ih predjemo u tokenStream-u
    # O(1)
    def expect(self, token_type):
        if self.check(token_type) == False:
            raise Exception(f"Ocekivan token {TokenType.getTokenValue(token_type)}")

# Test za parsiranje regexa
def main():
    regex = 'a+(b*){2,3}c+d'
    print('AST za regex:', regex)
    rl = Lexer(regex, {'a', 'b', 'c', 'd'})
    try:
        tokenStream = rl.lexer()
    except Exception as e:
        print(e)
        return

    for token in tokenStream:
        print(token.token_type, token.content)
    
    parser = Parser(tokenStream)
    try:
        ast = parser.parse()
    except Exception as e:
        print(e)
        print('Invalid regex')
        return
    print_ast(ast)

if __name__ == "__main__":
    main()
