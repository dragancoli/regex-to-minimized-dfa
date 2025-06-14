from parse import *
from collections import deque

# Klasa za NFA
# Predstavlja nedeterministički konačni automat (NFA) s početnim stanjem, završnim stanjem i skupom stanja.
class NKA:
    def __init__(self, start_state, end_state, states):
        self.start_state = start_state
        self.end_state = end_state
        self.states = states
        self.state_mapping = {}
        self.current_index = 0

    # Metoda za mapiranje stanja
    # O(1)
    def map_state(self, state):
        if state not in self.state_mapping:
            self.state_mapping[state] = self.current_index
            self.current_index += 1
        return str(self.state_mapping[state])

    # Metoda za pretvaranje u dictonary
    # O(n * m), gdje je n broj stanja, a m broj prelaza po stanju.
    def to_dict(self):
        nfa_representation = {
            'startingState': self.map_state(self.start_state)
        }

        for state_name, transitions in self.states.items():
            state_id = self.map_state(state_name)
            nfa_representation[state_id] = {
                'isTerminatingState': state_id == self.map_state(self.end_state)
            }
            for symbol, next_states in transitions.items():
                transition_symbol = 'epsilon' if symbol == '' else symbol
                transition_states = [self.map_state(next_state) for next_state in next_states]
                nfa_representation[state_id][transition_symbol] = transition_states

        return nfa_representation

# Klasa za konstrukciju NKA
# prima listu AST cvorova
# vraca Nka
    
class ASTtoNFA:
    def __init__(self, ast):
        self.ast = ast

    # O(n), gdje je n broj čvorova u AST-u. Svaka specifična vrsta čvora (LiteralNode, SeqNode, OrNode, itd.) ima stalnu 
    # vremensku složenost za svoje specifične operacije, pod pretpostavkom da je kominovanje stanja linearno.
    def construct(self):
        start_state, end_state, states = self.construct_from_ast(self.ast)
        return NKA(start_state, end_state, states)

    def construct_from_ast(self, node):
        node_type = type(node).__name__
        if node_type == 'LiteralNode':
            start_state = object()
            end_state = object()
            if node.char == 'ε':
                states = {
                    start_state: {'': {end_state}},
                    end_state: {'': set()}
                }
                return start_state, end_state, states
            states = {
                start_state: {node.char: {end_state}},
                end_state: {'': set()}
            }
            return start_state, end_state, states

        elif node_type == 'SeqNode':
            left_start, left_end, left_states = self.construct_from_ast(node.left)
            right_start, right_end, right_states = self.construct_from_ast(node.right)
            states = {**left_states, **right_states, left_end: {'': {right_start}}}
            return left_start, right_end, states

        elif node_type == 'OrNode':
            left_start, left_end, left_states = self.construct_from_ast(node.left)
            right_start, right_end, right_states = self.construct_from_ast(node.right)
            start_state = object()
            end_state = object()
            states = {
                start_state: {'': {left_start, right_start}},
                **left_states, **right_states,
                left_end: {'': {end_state}},
                right_end: {'': {end_state}},
                end_state: {'': set()},
            }
            return start_state, end_state, states

        elif node_type == 'StarNode':
            sub_start, sub_end, sub_states = self.construct_from_ast(node.left)
            start_state = object()
            end_state = object()
            states = {
                start_state: {'': {sub_start, end_state}},
                **sub_states,
                sub_end: {'': {start_state, end_state}},
                end_state: {'': set()}
            }
            return start_state, end_state, states
        
        elif node_type == 'RepeatExactlyNode':
            sub_start, sub_final, sub_states = self.construct_from_ast(node.left)
            num = int(node.num)

            if num == 0:
                starting_state = object()
                final_state = object()
                states = {
                    starting_state: {'': {final_state}},
                    final_state: {'': set()}
                }
                return starting_state, final_state, states

            starting_state = object()
            states = {}
            previous_final = starting_state

            for _ in range(num):
                current_start, current_final, current_states = self.construct_from_ast(node.left)
                states.update(current_states)
                states[previous_final] = {'': {current_start}}
                previous_final = current_final

            final_state = previous_final
            states[final_state] = {'': set()}

            return starting_state, final_state, states
        
        elif node_type == 'RepeatBetweenNode':
            sub_start, sub_final, sub_states = self.construct_from_ast(node.left)
            num = int(node.high)

            starting_state = object()
            states = {}
            previous_final = starting_state

            final_state = object()
            for _ in range(num):
                current_start, current_final, current_states = self.construct_from_ast(node.left)
                states.update(current_states)
                if _ >= int(node.low):
                    states[previous_final] = {'' : {current_start, final_state}}
                else:
                    states[previous_final] = {'': {current_start}}
                previous_final = current_final
                
            states[previous_final] = {'': {final_state}}
            states[final_state] = {'': set()}

            return starting_state, final_state, states
        
        elif node_type == 'RepeatMinNode':
            sub_start, sub_final, sub_states = self.construct_from_ast(node.left)
            num = int(node.min)

            if num == 0:
                starting_state = object()
                final_state = object()
                states = {
                    starting_state: {'': {final_state}},
                    final_state: {'': set()}
                }
                return starting_state, final_state, states

            starting_state = object()
            states = {}
            previous_final = starting_state
            
            return_back = object()
            # Kreira prvi deo automata koji ponavlja 'num' puta
            for _ in range(num):
                current_start, current_final, current_states = self.construct_from_ast(node.left)
                states.update(current_states)
                return_back = current_start
                states[previous_final] = {'': {current_start}}
                previous_final = current_final

            final_state = object()
            states[previous_final] = {'': {return_back, final_state}}
            states[final_state] = {'': set()}

            return starting_state, final_state, states

# Funkcija za ispis stanja i prelaza za NKA
# O(n * m), gdje je n broj stanja, a m broj prelaza po stanju
def ilustrate_nka(nfa):
    print('Stanja NKA: \n')
    for key in nfa.keys():
        if key == 'startingState':
            continue
        if nfa[key]['isTerminatingState']:
            print(key + ' (krajnjeStanje)')
        else:
            print(key)
        
    print('\nPrelazi: \n')
    for key in nfa.keys():
        if key == 'startingState':
            continue
        for symbol in nfa[key].keys():
            if symbol == 'isTerminatingState':
                continue
            for next_state in nfa[key][symbol]:
                sy = symbol
                if symbol == 'epsilon':
                    sy = 'ε'
                print(key, ' ', sy, ' ', next_state)
    print('Pocetno stanje: ' +  nfa['startingState'])

# Test za pretvaranje AST u NFA        
def main():
    regex = 'εaε'
    print('NKA za regex: ', regex + '\n')
    rl = Lexer(regex, {'a', 'b', 'c', 'd', 'e'})
    try:
        tokenStream = rl.lexer()
    except Exception as e:
        print(e)
        return
    
    pR = Parser(tokenStream)
    # Pokušaj da se uhvate izuzetci
    throwException = False
    try:
        AST = pR.parse()
    except Exception as e:
        print(e)
        throwException = True
    if throwException:
        print('Nevažeći regex')
        return
    nka = ASTtoNFA(AST).construct().to_dict()
    ilustrate_nka(nka)

if __name__ == "__main__":
    main()
