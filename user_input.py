import min_dka
from lexer import Lexer
from parse import Parser
from nka import ASTtoNFA
from dka import NKAtoDKAKonvertor

def main():
    regex = input('Unesite regularni izraz: ')
    alphabet = input('Unesite alfabet(Znak po znak odvojen razmakom): ')
    alphabet = alphabet.split(' ')
    alphabet = set(alphabet)
    try:
        throwException = False
        regex = regex
        rl = Lexer(regex, alphabet)
        tokenStream = rl.lexer()
        pR = Parser(tokenStream)
        AST = pR.parse()
        nka = ASTtoNFA(AST).construct().to_dict()
        converter = NKAtoDKAKonvertor(nka)
        dka = converter.convert().to_dict()
    except Exception as e:
        print(f'{e} {regex} nije validan.')
        throwException = True
    if throwException == False:
        print(f'{regex} je validan regularni izraz za koji se moze konstruisati minimalan DKA za alfabet {alphabet}')

if __name__ == "__main__":
    main()
            
    