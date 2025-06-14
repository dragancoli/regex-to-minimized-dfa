from nka import *

# Klasa za DKA 
# Predstavlja deterministički konačni automat (DFA) s alfabetom, 
#stanjima, početnim stanjem, prihvaćajućim stanjima i prijelaznom funkcijom.
class DKA: 
    def __init__(self, alphabet, states, starting_state, accept_states, transition_function):
        self.alphabet = alphabet
        self.states = states
        self.starting_state = starting_state
        self.accept_states = accept_states
        self.transition_function = transition_function
        self.states_map = {}
        self.state_counter = 0
    
    # Funkcija za provjeravanje da li je trenutni niz susednih karaktera u alfabetu
    # O(m), gdje je m duzina ulaznog stringa
    def execute(self, input_string):
        current_state = self.starting_state
        index = 0
        while index < len(input_string):
            symbol = input_string[index]
            current_state = self.transition_function[current_state][symbol]
            index += 1
        return current_state in self.accept_states
    
    # Isto kao i kod NKA vraca broj stanja u DKA
    # O(1)
    def get_mapped_state_number(self, state):
        match self.states_map.get(state):
            case None:
                self.states_map[state] = self.state_counter
                self.state_counter += 1
            case _:
                pass
        return str(self.states_map[state])

    # Metoda za pretvaranje u dictionary
    # O(n * m) gdje je n broj stanja, a m broj prelaza po stanju
    def to_dict(self):
        dfa_dictionary = {}
        dfa_dictionary['startingState'] = self.get_mapped_state_number(self.starting_state)
    
        for state in self.states:
            match state:
                case 'frozenset()':
                    continue
                case _:
                    dfa_dictionary[self.get_mapped_state_number(state)] = {
                        "isTerminatingState": state in self.accept_states
                    }

            for symbol in self.alphabet:
                match symbol:
                    case 'isTerminatingState':
                        continue
                    case _:
                        if self.transition_function[state][symbol] != "frozenset()":
                            dfa_dictionary[self.get_mapped_state_number(state)][symbol] = self.get_mapped_state_number(self.transition_function[state][symbol]) 
        return dfa_dictionary
    

# Klasa za pretvaranje NKA u DKA
# prima NKA
# vraca DKA

class NKAtoDKAKonvertor:
    def __init__(self, nka):
        self.nka = nka
        self.dfa = self.convert()

    # Odredjenje epsilon-ciljnih stanja
    # O(n), gdje je n broj stanja u NFA
    def epsilon_closure(self, states):
        closure = set(states)
        queue = list(states)
        i = 0
        while i < len(queue):
            state = queue[i]
            if state in self.nka:
                self.next_states_closure(state, closure, queue)
            i += 1
        return frozenset(closure)
    
    # Metoda za pretvaranje epsilon-ciljnih stanja
    # O(m),gdje je m broj epsilon tranzicija iz stanja
    def next_states_closure(self, state, closure, queue):
        for next_state in self.nka[state].get("epsilon", []):           
            if next_state not in closure:
                closure.add(next_state)
                queue.append(next_state)

    # Metoda koja vrsi prijelaz po simbolu
    # O(n), gdje je n broj stanja u NFA
    def move(self, states, symbol):
        move_states = set()
        for state in states:
            if state in self.nka:
                #provjera da li je isTerminatingState
                if symbol == 'isTerminatingState':
                    continue
                for next_state in self.nka[state].get(symbol, []):
                    move_states.add(next_state)
        return frozenset(move_states)
    
    # Metoda za pretvaranje NKA u DKA
    # O(2^n * m), gdje je n broj stanja u NFA, a m velicina alfabeta
    def convert(self):
        alphabet = self.extract_alphabet()
        start_state = self.epsilon_closure([self.nka["startingState"]])
    
        dka_states, dka_accept_states, dka_transition_function = self.construct_dka(alphabet, start_state)
    
        dka_states = [str(state) for state in dka_states]
        start_state = str(start_state)
        dka_accept_states = [str(state) for state in dka_accept_states]
        dka_transition_function = {
            str(k): {symbol: str(v) for symbol, v in transitions.items()}
            for k, transitions in dka_transition_function.items()
        }
    
        return DKA(alphabet, dka_states, start_state, dka_accept_states, dka_transition_function)

    # Pomocne metode za convert metodu
    def convert_transition_function(self, queue, alphabet, dka_states, dka_accept_states, dka_transition_function):
        while queue:
            current_state = queue.pop(0)
            for symbol in alphabet:
                move_states = self.move(current_state, symbol)
                closure_states = self.epsilon_closure(move_states)

                if closure_states not in dka_states:
                    dka_states.append(closure_states)
                    queue.append(closure_states)

                dka_transition_function.setdefault(current_state, {})[symbol] = closure_states

            if any(self.is_terminating(state) for state in current_state):
                dka_accept_states.append(current_state)
    # O(n * m), gdje je n broj stanja, a m broj prelaza po stanju
    def extract_alphabet(self):
        alphabet = set()
        for state in self.nka.values():
            for symbol in state:
                if symbol != "epsilon":
                    alphabet.add(symbol)

        alphabet.discard("isTerminatingState")
        alphabet.discard(self.nka["startingState"])
        return alphabet
    
    # O(2^n * m), gdje je n broj stanja, a m broj prelaza po stanju
    def construct_dka(self, alphabet, start_state):
        dka_states = [start_state]
        dka_accept_states = []
        dka_transition_function = {}
        queue = [start_state]
        self.convert_transition_function(queue, alphabet, dka_states, dka_accept_states, dka_transition_function)
    
        return dka_states, dka_accept_states, dka_transition_function
    
    def is_terminating(self, state):
        return state in self.nka and self.nka[state].get("isTerminatingState", False)
    
    
# Ispisuje DKA
# O(n * m), gdje je n broj stanja, a m broj prelaza po stanju
def ilustrate_dka(dka):
    print('Pocetno stanje: ' +  dka['startingState'])
    print('\nStanja:\n')
    for key in dka.keys():
        if key == 'startingState':
            continue
        if dka[key]['isTerminatingState']:
            print(key + ' (krajnjeStanje)')
        else:
            print(key)
        
    print('\nPrelazi:\n')
    for key in dka.keys():
        if key == 'startingState':
            continue
        for symbol in dka[key].keys():
            if symbol == 'isTerminatingState':
                continue
            next_state= dka[key][symbol]   
            print(key, ' ', symbol, ' ', next_state)
    

# Test za pretvaranje DKA
def main():
    regex = 'εab*c+d{2,4}eε'
    print('DKA za regex: ', regex + '\n')
    rl = Lexer(regex, {'a', 'b', 'c', 'd', 'e'})
    tokenStream = rl.lexer()
    pR = Parser(tokenStream)
    # Pokusaj da se uhvate izuzetci
    throwException = False
    try:
        AST = pR.parse()
    except Exception as e:
        print(e)
        throwException = True
    if throwException:
        print('Nevazeci regex')
        return
    nka = ASTtoNFA(AST).construct().to_dict()
    converter = NKAtoDKAKonvertor(nka)
    dka = converter.convert().to_dict()
    ilustrate_dka(dka)

if __name__ == "__main__":
    main()