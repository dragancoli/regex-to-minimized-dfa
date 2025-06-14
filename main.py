import min_dka
from lexer import Lexer
from parse import Parser
from nka import ASTtoNFA
from dka import NKAtoDKAKonvertor

def main():
    regexList = [
        'εa{7,6}',
        'a{2,6}*b+cde{2,4}',
        'εa{3,6}bdSTOPε',
        'STa*Bg{1,2}eε',
        'εAaa{1,3}be*a+de'
    ]
    alphabetList = [
        {'a'},
        {'a', 'b', 'c', 'd', 'e'},
        {'a', 'b', 'd', 'STOP'},
        {'ST', 'a', 'Bg', 'e'},
        {'A', 'aa', 'b', 'e', 'a', 'd', 'e'}
    ]

    throwException = False
    for i in range(len(regexList)):
        try:
            throwException = False
            regex = regexList[i]
            rl = Lexer(regex, alphabetList[i])
            tokenStream = rl.lexer()
            pR = Parser(tokenStream)
            AST = pR.parse()
            nka = ASTtoNFA(AST).construct().to_dict()
            converter = NKAtoDKAKonvertor(nka)
            dka = converter.convert().to_dict()
        except Exception as e:
            print(f'{e} {regexList[i]} nije validan.')
            throwException = True
        if throwException == False:
            print(f'{regex} je validan regularni izraz za koji se moze konstruisati minimalan DKA za alfabet {alphabetList[i]}')
        throwException = False

if __name__ == "__main__":
    main()
            
    