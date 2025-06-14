import pytest
from parse import *
from dka import DKA, NKAtoDKAKonvertor, ASTtoNFA

def test_dka_execute():
    alphabet = {'a', 'b'}
    states = {'q0', 'q1', 'q2'}
    start_state = 'q0'
    accept_states = {'q2'}
    transition_function = {
        'q0': {'a': 'q1'},
        'q1': {'b': 'q2'},
        'q2': {'a': 'q2', 'b': 'q2'},
    }
    dka = DKA(alphabet, states, start_state, accept_states, transition_function)
    
    assert dka.execute('ab') == True
    assert dka.execute('aba') == True
    assert dka.execute('ababb') == True
    assert dka.execute('a') == False


def test_nka_to_dka_conversion():
    regex = 'a+b'
    rl = Lexer(regex, {'a', 'b'})
    tokenStream = rl.lexer()
    pR = Parser(tokenStream)
    AST = pR.parse()
    nka = ASTtoNFA(AST).construct().to_dict()
    converter = NKAtoDKAKonvertor(nka)
    dka = converter.convert().to_dict()
    
    assert dka['startingState'] == '0'
    assert '1' in dka['0']['a'] or '1' in dka['0']['b']
    assert '2' in dka['0']['a'] or '2' in dka['0']['b']
    assert dka['1']['isTerminatingState'] == True or dka['2']['isTerminatingState'] == True

def test_nka_epsilon_closure():
    regex = 'ab'
    rl = Lexer(regex, {'a', 'b'})
    tokenStream = rl.lexer()
    pR = Parser(tokenStream)
    AST = pR.parse()
    nka = ASTtoNFA(AST).construct().to_dict()
    converter = NKAtoDKAKonvertor(nka)
    closure = converter.epsilon_closure(['0'])
    assert closure == frozenset({'0'})

def test_nka_move():
    regex = 'aa+bb'
    rl = Lexer(regex, {'a', 'b'})
    tokenStream = rl.lexer()
    pR = Parser(tokenStream)
    AST = pR.parse()
    nka = ASTtoNFA(AST).construct().to_dict()
    converter = NKAtoDKAKonvertor(nka)
    move_states = converter.move(['3'], 'a')
    
    assert move_states == frozenset({'4'}) or move_states == frozenset()


if __name__ == '__main__':
    pytest.main()