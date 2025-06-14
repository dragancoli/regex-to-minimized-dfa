import pytest
from lexer import Lexer
from parse import Parser
from nka import NKA, ASTtoNFA

def test_literal_character_ast_node():
    regex = 'a'
    rl = Lexer(regex, {'a'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['a'] == ['1']
    assert nka['1']['isTerminatingState']

def test_epsilon_character_ast_node():
    regex = 'ε'
    rl = Lexer(regex, {'a'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['epsilon'] == ['1']
    assert nka['1']['isTerminatingState']

def test_or_ast_node():
    regex = 'a+b'
    rl = Lexer(regex, {'a','b'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['epsilon'] == ['2', '3'] or nka['0']['epsilon'] == ['3', '2']
    transitions_1 = set(nka['2'].keys()) - {'isTerminatingState'}
    transitions_2 = set(nka['3'].keys()) - {'isTerminatingState'}
    assert transitions_1 == {'a'} or {'b'}
    assert transitions_2 == {'a'} or {'b'}
    assert nka['5']['epsilon'] == ['1']
    assert nka['4']['epsilon'] == ['1']
    assert nka['1']['isTerminatingState']

def test_seq_ast_node():
    regex = 'ab'
    rl = Lexer(regex, {'a','b'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['a'] == ['2']
    assert nka['2']['epsilon'] == ['3']
    assert nka['3']['b'] == ['1']
    assert nka['1']['isTerminatingState']


def test_repeat_exactly_ast_node():
    regex = 'a{2}'
    rl = Lexer(regex, {'a'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['epsilon'] == ['1']
    assert nka['1']['a'] == ['3']
    assert nka['3']['epsilon'] == ['4']
    assert nka['4']['a'] == ['2']
    assert nka['2']['isTerminatingState']

def test_repeat_between_ast_node():
    regex = 'a{2,3}'
    rl = Lexer(regex, {'a'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['epsilon'] == ['1']
    assert nka['1']['a'] == ['3']
    assert nka['3']['epsilon'] == ['4']
    assert nka['4']['a'] == ['5']
    assert ( nka['5']['epsilon'] == ['2', '6'] or nka['5']['epsilon'] == ['6', '2'] )
    assert nka['6']['a'] == ['7']
    assert nka['7']['epsilon'] == ['2']
    assert nka['2']['isTerminatingState']

def test_repeat_min_ast_node():
    regex = 'a{2,}'
    rl = Lexer(regex, {'a'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    nka = ASTtoNFA(ast).construct().to_dict()
    assert nka['startingState'] == '0'
    assert nka['0']['epsilon'] == ['1']
    assert nka['1']['a'] == ['3']
    assert nka['3']['epsilon'] == ['4']
    assert nka['4']['a'] == ['5']
    assert ( nka['5']['epsilon'] == ['2', '4'] or nka['5']['epsilon'] == ['4', '2'] )
    assert nka['2']['isTerminatingState']

if __name__ == "__main__":
    pytest.main()