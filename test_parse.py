import pytest
from parse import Parser, LiteralNode, SeqNode, StarNode, OrNode, RepeatBetweenNode, RepeatExactlyNode, RepeatMinNode
from lexer import Lexer

def test_literal_character_node():
    regex = 'a'
    rl = Lexer(regex, {'a'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    assert isinstance(ast, LiteralNode)
    assert ast.char == 'a'

def test_sequence_node():
    regex = Lexer('ab', {'a','b'}) 
    tokenStream = regex.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    assert isinstance(ast, SeqNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'a'
    assert isinstance(ast.right, LiteralNode)
    assert ast.right.char == 'b'

def test_star_node():
    regex = Lexer('b*', {'b'})
    tokenStream = regex.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    assert isinstance(ast, StarNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'b'

def test_or_node():
    regex = Lexer('a+b', {'a','b'})
    tokenStream = regex.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    assert isinstance(ast, OrNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'a'
    assert isinstance(ast.right, LiteralNode)
    assert ast.right.char == 'b'

def test_repeat_exactly_node():
    regex = Lexer('a{2}', {'a'})
    tokens = regex.lexer()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast, RepeatExactlyNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'a'
    assert ast.num == '2'

def test_repeat_between_node():
    regex = Lexer('a{2,3}', {'a'})
    tokenStream = regex.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    assert isinstance(ast, RepeatBetweenNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'a'
    assert ast.low == '2'
    assert ast.high == '3'

def test_repeat_min_node():
    regex = Lexer('a{2,}', {'a'})
    tokens = regex.lexer()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast, RepeatMinNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'a'
    assert ast.min == '2'

def test_complex_regex():
    regex = Lexer('a+(b*){2,3}c', {'a', 'b', 'c'})
    tokens = regex.lexer()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast, OrNode)
    assert isinstance(ast.left, LiteralNode)
    assert ast.left.char == 'a'
    assert isinstance(ast.right, SeqNode)
    assert isinstance(ast.right.left, RepeatBetweenNode)
    assert isinstance(ast.right.left.left, StarNode)
    assert isinstance(ast.right.left.left.left, LiteralNode)
    assert ast.right.left.left.left.char == 'b'
    assert isinstance(ast.right.right, LiteralNode)
    assert ast.right.right.char == 'c'


if __name__ == "__main__":
    pytest.main()