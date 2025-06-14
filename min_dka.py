from dka import *

# Klasa za minimizaciju DKA
# Minimizira DFA dijeljenjem stanja u grupe na temelju njihovog ponašanja i
# pogledu prihvaćanja i prelaza.
class DKAMinimizer:
    def __init__(self, dka_dict):
        self.states, self.start_state, self.alphabet, self.accept_states, self.reject_states, self.groups = self.extract_data(dka_dict)
        self.partition = self.make_partition(dka_dict)
        self.old_dka_dict = dka_dict
    
    # Ekstaktuje podatke iz DKA u obliku direktorija
    # O(n*m), gdje je n broj stanja, a m broj prelaza po stanju
    def extract_data(self, dka_dict):
        states = list(dka_dict.keys() - {'startingState'})
        start_state = dka_dict['startingState']
        
        alphabet = self.extract_alphabet(dka_dict)
        alphabet.remove(dka_dict['startingState'])
        accept_states = set([s for s in states if dka_dict[s]['isTerminatingState']])
        reject_states = set(states) - accept_states
        groups = [accept_states, reject_states]

        return states, start_state, alphabet, accept_states, reject_states, groups
    
    # Ekstarktuje alfabet iz DKA
    # O(n*m), gdje je n broj stanja, a m broj prelaza po stanju
    def extract_alphabet(self, dka_dict):
        alphabet = []
        for state in dka_dict.values():
            for key in state:
                if key != 'isTerminatingState':
                    alphabet.append(key)
        return list(set(alphabet))

    # Funkcija za formiranje particije na temelju ponašanja
    # O(n^2 * m), gdje je n broj stanja, a m broj prelaza po stanju
    def make_partition(self, dka_dict):
        a_s, r_s = self.accept_states, self.reject_states
        partition = [a_s, r_s]
        
        while True:
            new_partition = self.refine_partition(dka_dict, partition)
            if new_partition == partition:
                break
            partition = new_partition
        
        return partition
    
    # Ova funkcija rafinira particiju stanja dok se ne postigne stabilna particija koja se više ne menja
    # O(n^2 * m), gde je n broj stanja, a m broj prelaza po stanju
    def refine_partition(self, dka_dict, partition):
        group_to_idx = self.map_states_to_groups(partition)
        next_states = self.compute_next_states(dka_dict, partition, group_to_idx)
        
        new_partition = []
        for group in partition:
            if len(group) == 0:
                continue
            
            same_next_states = self.group_by_next_states(group, next_states)
            
            for same_states in same_next_states.values():
                new_partition.append(set(same_states))
        
        return new_partition
    
    # Ova funkcija mapira svako stanje na indeks grupe kojoj pripada
    # Koristi se za brzo pronalaženje kojoj grupi stanje pripada
    # O(n), gde je n broj stanja
    def map_states_to_groups(self, partition):
        group_to_idx = {}
        for i, group in enumerate(partition):
            for state in group:
                group_to_idx[state] = i
        return group_to_idx
    
    # Ova funkcija izračunava sledeća stanja za svako stanje i simbol u alfabetu
    # Ako prelaz ne postoji, stanje se mapira na 'stuck'
    #  O(n * m), gde je n broj stanja, a m broj prelaza po stanju
    def compute_next_states(self, dka_dict, partition, group_to_idx):
        next_states = {}
        for group in partition:
            for state in group:
                next_states[state] = {}
                for symbol in self.alphabet:
                    next_states[state][symbol] = group_to_idx.get(dka_dict[state].get(symbol, 'stuck'), 'stuck')
        return next_states

    # Ova funkcija grupiše stanja koja imaju ista sledeća stanja
    # O(n), gde je n broj stanja
    def group_by_next_states(self, group, next_states):
        same_next_states = {}
        for state in group:
            key = tuple(next_states[state].items())
            if key not in same_next_states:
                same_next_states[key] = []
            same_next_states[key].append(state)
        return same_next_states

    # Funkcija za pretvaranje minDKA u direkorij
    # O(n*m), gdje je n broj stanja, a m broj prelaza po stanju
    def to_dict(self):
        newStateNames = {}
        for state in self.states:
            for i, group in enumerate(self.partition):
                if state in group:
                    newStateNames[state] = i
                    break
        dka_dict = {"startingState": str(newStateNames[self.start_state])}

        for state in self.states:
            dka_dict[str(newStateNames[state])] = {
                "isTerminatingState": state in self.accept_states
            }
            for symbol in self.alphabet:
                self.define_transition(symbol, dka_dict, newStateNames, state)
        
        return dka_dict
    
    # Funkcija za definisanje prelaza
    # O(1)
    def define_transition(self, symbol, dka_dict, newStateNames, state):
        if symbol in self.old_dka_dict[state]:
                    dka_dict[str(newStateNames[state])][symbol] = str(newStateNames[self.old_dka_dict[state][symbol]])

# Ispisuje minimizirani DFA sa svim eksplicitno 
# definiranim prijelazima, uključujući prijelaze u mrtvo stanje.
# O(n * m), gdje je n broj stanja, a m broj simbola u alfabetu
def ilustrate_fully_defined_min_dka(dka, alphabet):
    alphabet = alphabet - {'ε'}
    print('Pocetno stanje: ' +  dka['startingState'])
    print('Stanja:')
    for key in dka.keys():
        if key == 'startingState':
            continue
        if dka[key]['isTerminatingState']:
            print(key + ' (krajnjeStanje)')
        else:
            print(key)
        
    print('\nPrelazi:\n')
    for key in dka.keys():
        symbols = []
        if key == 'startingState':
            continue
        for symbol in dka[key].keys():
            if symbol == 'isTerminatingState':
                continue
            next_state= dka[key][symbol]   
            print(key, ' ', symbol, ' ', next_state)
            symbols.append(symbol)
        
        for symbol in alphabet:
            if symbol not in symbols:
                print(key, ' ', symbol, ' ', 'DEAD_STATE')

# Ispisuje minimizirani DFA bez prijelaza u mrtvo stanje.
# O(n * k), gdje je n broj stanja, a k broj prijelaza po stanju
def ilustrate_min_dka_without_dead_states(dka):
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
        

# Test za pretvaranje Minimalnog DKA u DKA
def main():
    alphabet = {'A', 'AB', '1', '2'}
    regex = 'ε1A+(AB{1,2})*AABABA2ε'
    print('Minimalni DKA za regex: ', regex + '\n')
    rl = Lexer(regex, alphabet)
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
    MinDKAConv = DKAMinimizer(dka)
    minDKA = MinDKAConv.to_dict()
    #ilustrate_min_dka_without_dead_states(minDKA)
    ilustrate_fully_defined_min_dka(minDKA, alphabet)
    print(f"Za regex {regex}  moguce je konstruisati DKA. ")


if __name__ == "__main__":
    main()