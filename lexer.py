from enum import Enum, auto

# Klasa za odredjivanje podataka o tokenu
# Moguce odrediti vrstu tokena i njegovu vrednost
class TokenType(Enum):
    OR = auto()
    STAR = auto()
    OPEN_PAREN = auto()
    CLOSED_PAREN = auto()
    LITERAL = auto()
    OPEN_BRACE = auto()
    CLOSED_BRACE = auto()
    META_CHAR = auto()
    COMMA = auto()

    # O(1)
    def getTokenType(token):
        match token:
            case '+':
                return TokenType.OR
            case '*':
                return TokenType.STAR
            case '(':
                return TokenType.OPEN_PAREN
            case ')':
                return TokenType.CLOSED_PAREN
            case '{':
                return TokenType.OPEN_BRACE
            case '}':
                return TokenType.CLOSED_BRACE
            case ',':
                return TokenType.COMMA
            case _:
                return TokenType.LITERAL

    #O(1)
    def getTokenValue(token):
        match token:
            case TokenType.OR:
                return '+'
            case TokenType.STAR:
                return '*'
            case TokenType.OPEN_PAREN:
                return '('
            case TokenType.CLOSED_PAREN:
                return ')'
            case TokenType.OPEN_BRACE:
                return '{'
            case TokenType.CLOSED_BRACE:
                return '}'
            case TokenType.COMMA:
                return ','
            case _:
                return token
            
# Klasa za reprezentaciju token
class Token:
    def __init__(self, token_type, content):
        self.token_type : TokenType = token_type
        self.content : str = content

# Funkcija za provjeravanje da li je trenutni niz susednih karaktera u alfabetu
# O(n*m) gdje je n broj simbola u alfabetu, a m je duzina podniza koji se provjerava.
def checkCocatenation(input, alphabet, pos):
    for symbol in alphabet:
        if input[0:pos] == symbol[0:pos]:
            return True
    return False


# Klasa za Lexer
# prima string
# vraca niz tokena
class Lexer:
    def __init__(self, regexStr, alphabet):
        self.regexStr = regexStr
        self.alphabet = alphabet
        self.alphabet.add('ε')

    # O(m * n * l), gdje je m duzina ulaznog niza, n je broj simbola u alfabetu, a l je duzina najdužeg simbola u alfabetu.
    def lexer(self):
        tokenStream = []
        i = 0
        while i < len(self.regexStr):
            # Provera da li se kombinacija susednih karaktera nalazi u alfabetu
            j = i
            #while j < len(self.regexStr) and self.regexStr[i:j+1] in self.alphabet:
            while j < len(self.regexStr) and checkCocatenation(self.regexStr[i:j+1],self.alphabet, j-i+1):
                j += 1
            # Ako se kombinacija nalazi u alfabetu, dodajemo je kao literal token
            if j > i and self.regexStr[i:j] in self.alphabet:
                token = Token(TokenType.LITERAL, self.regexStr[i:j])
                tokenStream.append(token)
                i = j
            else:
                if TokenType.getTokenType(self.regexStr[i]) == TokenType.LITERAL and self.regexStr[i] not in self.alphabet:
                    raise Exception(f'Ovaj karakter nije u alfabetu: {self.regexStr[i]}. ')
                token = Token(TokenType.getTokenType(self.regexStr[i]), TokenType.getTokenValue(self.regexStr[i]))
                tokenStream.append(token)
                i += 1
                # Ako je trenutni token { onda sledeci karakter tretiramo kao metakarakter
                if token.token_type == TokenType.OPEN_BRACE:
                    # Mora biti broj
                    if self.regexStr[i].isalpha():
                        raise Exception(f'Izmedju viticastih zagrada mora biti broj na poziciji {i}. ')
                    num = ''
                    while self.regexStr[i].isnumeric() and i < len(self.regexStr):
                        num += self.regexStr[i]
                        i += 1
                    token = Token(TokenType.META_CHAR, num)
                    old_num = num
                    tokenStream.append(token)
                    
                    if TokenType.getTokenType(self.regexStr[i]) == TokenType.COMMA and i < len(self.regexStr):
                        token = Token(TokenType.COMMA, ',')
                        tokenStream.append(token)
                        i += 1
                        if self.regexStr[i].isnumeric():
                            num = ''
                            while self.regexStr[i].isnumeric() and i<len(self.regexStr):
                                num += self.regexStr[i]
                                i += 1
                            if int(old_num) > int(num):
                                raise Exception(f'U operatoru ponavaljanja prvi broj mora biti veci od drugog na poziciji {i}. ')
                            token = Token(TokenType.META_CHAR, num)
                            tokenStream.append(token)
                            
                        if self.regexStr[i] != '}':
                            raise Exception(f'Neispravna upotreba operatora za ponavljanje na poziciji {i}. ')

                    
        return tokenStream
    
# Test primjer
def main():
    rl = Lexer('εa{7,6}', {'a', 'abe'})
    try:
        tokenStream = rl.lexer()
    except Exception as e:
        print(e)
        return
    for token in tokenStream:
        print(token.token_type, token.content)


if __name__ == "__main__":
    main()

