import pytest
from lexer import TokenType, Token, Lexer, checkCocatenation

# Testovi za TokenType.getTokenType
@pytest.mark.parametrize("input_char, expected_type", [
    ('+', TokenType.OR),
    ('*', TokenType.STAR),
    ('(', TokenType.OPEN_PAREN),
    (')', TokenType.CLOSED_PAREN),
    ('{', TokenType.OPEN_BRACE),
    ('}', TokenType.CLOSED_BRACE),
    (',', TokenType.COMMA),
    ('a', TokenType.LITERAL),
    ('1', TokenType.LITERAL),
])
def test_get_token_type(input_char, expected_type):
    assert TokenType.getTokenType(input_char) == expected_type

# Testovi za TokenType.getTokenValue
@pytest.mark.parametrize("input_type, expected_value", [
    (TokenType.OR, '+'),
    (TokenType.STAR, '*'),
    (TokenType.OPEN_PAREN, '('),
    (TokenType.CLOSED_PAREN, ')'),
    (TokenType.OPEN_BRACE, '{'),
    (TokenType.CLOSED_BRACE, '}'),
    (TokenType.COMMA, ','),
    (TokenType.LITERAL, 'a'),
])
def test_get_token_value(input_type, expected_value):
    if input_type == TokenType.LITERAL:
        assert TokenType.getTokenValue('a') == 'a'
    else:
        assert TokenType.getTokenValue(input_type) == expected_value

# Test za checkCocatenation funkciju
@pytest.mark.parametrize("input_str, alphabet, pos, expected_result", [
    ('ab', {'a', 'b', 'ab'}, 2, True),
    ('abc', {'a', 'ab', 'abc'}, 3, True),
    ('a', {'a', 'b', 'c'}, 1, True),
    ('d', {'a', 'b', 'c'}, 1, False),
    ('abc', {'a', 'ab', 'abc'}, 2, True)
])
def test_check_concatenation(input_str, alphabet, pos, expected_result):
    assert checkCocatenation(input_str, alphabet, pos) == expected_result

# Testovi za regexLexer.lexer
def test_lexer_basic():
    rl = Lexer('a+b*', {'a', 'b'})
    tokenStream = rl.lexer()
    expected = [
        (TokenType.LITERAL, 'a'),
        (TokenType.OR, '+'),
        (TokenType.LITERAL, 'b'),
        (TokenType.STAR, '*')
    ]
    assert [(token.token_type, token.content) for token in tokenStream] == expected

def test_lexer_with_braces():
    rl = Lexer('a{2,3}', {'a'})
    tokenStream = rl.lexer()
    expected = [
        (TokenType.LITERAL, 'a'),
        (TokenType.OPEN_BRACE, '{'),
        (TokenType.META_CHAR, '2'),
        (TokenType.COMMA, ','),
        (TokenType.META_CHAR, '3'),
        (TokenType.CLOSED_BRACE, '}')
    ]
    assert [(token.token_type, token.content) for token in tokenStream] == expected

def test_lexer_invalid_char():
    rl = Lexer('a{2,d}', {'a'})
    with pytest.raises(Exception, match='Neispravna upotreba operatora za ponavljanje.'):
        rl.lexer()

def test_lexer_invalid_alphabet():
    rl = Lexer('a{2,b}', {'a', 'b'})
    with pytest.raises(Exception, match='Neispravna upotreba operatora za ponavljanje.'):
        rl.lexer()

def test_lexer_complex():
    rl = Lexer('abe{2,6}cd', {'a', 'abe', 'cd'})
    tokenStream = rl.lexer()
    expected = [
        (TokenType.LITERAL, 'abe'),
        (TokenType.OPEN_BRACE, '{'),
        (TokenType.META_CHAR, '2'),
        (TokenType.COMMA, ','),
        (TokenType.META_CHAR, '6'),
        (TokenType.CLOSED_BRACE, '}'),
        (TokenType.LITERAL, 'cd')
    ]
    assert [(token.token_type, token.content) for token in tokenStream] == expected

# Pokretanje testova
if __name__ == "__main__":
    pytest.main()
