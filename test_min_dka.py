import pytest
from parse import *
from dka import DKA, NKAtoDKAKonvertor, ASTtoNFA
from min_dka import DKAMinimizer

def test_make_partition():
    regex = 'abc'
    rl = Lexer(regex, {'a', 'b', 'c'})
    tokenStream = rl.lexer()
    pR = Parser(tokenStream)
    AST = pR.parse()
    nka = ASTtoNFA(AST).construct().to_dict()
    converter = NKAtoDKAKonvertor(nka)
    dka = converter.convert().to_dict()
    MinDKAConv = DKAMinimizer(dka)
    minDKA = MinDKAConv.to_dict()
    partition = MinDKAConv.make_partition(minDKA)
    assert len(partition) == 4


def test_minimize_dfa():
    regex = 'ab+a'
    rl = Lexer(regex, {'a', 'b'})
    tokenStream = rl.lexer()
    parser = Parser(tokenStream)
    ast = parser.parse()
    nka = ASTtoNFA(ast).construct().to_dict()
    converter = NKAtoDKAKonvertor(nka)
    dka = converter.convert().to_dict()
    minimizer = DKAMinimizer(dka)
    minimized_dka = minimizer.to_dict()
    
    assert ( minimized_dka['startingState'] == '2' and minimized_dka['2']['a'] == '0' and
             minimized_dka['0']['b'] == '1' and minimized_dka['1']['isTerminatingState'] == True and
             minimized_dka['0']['isTerminatingState'] == True) or ( minimized_dka['startingState'] == '2' and
             minimized_dka['2']['a'] == '1' and minimized_dka['1']['b'] == '0' and
             minimized_dka['1']['isTerminatingState'] == True and minimized_dka['0']['isTerminatingState'] == True) 
    
if __name__ == '__main__':
    pytest.main()