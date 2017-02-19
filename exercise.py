#from graphviz import Digraph
import re
import itertools
import random
import string

EMPTY_WORD = ''
EMPTY_WORD_PRINTABLE = '#'

MESSAGES = {
    'correct-response': "That's right!",
    'invalid-response': "Please revise your answer.",
}



def main():
    exercise_first_tutorial()

    lvl = 1

    while 'q' != raw_input('Press Enter to continue.'):
        print
        print '=== Level %d ===' % lvl
        print 

        grammar = gen_grammar_for_lvl(lvl)

        print_grammar(grammar)

        exercise_first(grammar)

        exercise_follow(grammar)

        exercise_ll1(grammar)

        lvl += 1



def gen_grammar_for_lvl(lvl):
    assert lvl > 0

    coeff = 2

    n_nonterminals = 2 + lvl / coeff

    rhs_per_nonterminal = (1, 2 + lvl / coeff)

    nonterminals_per_rhs = (0, 1 + lvl / coeff)

    terminals_per_rhs = (0, 2 + coeff)

    grammar = gen_grammar(n_nonterminals,
                          rhs_per_nonterminal,
                          nonterminals_per_rhs,
                          terminals_per_rhs)

    return grammar


def isterminal(x):
    return x in string.lowercase

def is_string_of_terminals(s):
    for x in s:
        if not isterminal(x):
            return False

    return True

def isnonterminal(x):
    return x in string.uppercase


def exercise_ll1(grammar):

    answer_obtained = False
    user_answer = None
    while not answer_obtained:
        user_input = raw_input('Can this grammar be parsed by a backtrack-free LL(1) parser? (y/n): ')
        
        if not user_input in ['y', 'n']:
            print MESSAGES['invalid-response']
        else:
            user_answer = 'y' == user_input
            answer_obtained = True
            
    
    is_ll1_grammar = is_ll1(grammar)

    if user_answer == is_ll1_grammar:
        print "Correct!"
    else:
        print "Wrong!"
        
        if is_ll1_grammar:
            print "It CAN be parsed by a backtrack-free LL(1) parser."
        else:
            print "It cannot be parsed by a backtrack-free LL(1) parser."



def exercise_first_tutorial():
    print '=== Tutorial ==='
    print
    print 'In this exercise you are asked to determine FIRST sets.'
    print 'Study the following grammar.'
    print 'The empty word is represented by the symbol %s.' \
        % EMPTY_WORD_PRINTABLE
    print 'Capital letters represent non-terminals, whereas lower-case letters represent terminal symbols.'
    print

    grammar = gen_grammar()

    print_grammar(grammar)

    label_empty = lambda x: \
                  EMPTY_WORD_PRINTABLE if x == EMPTY_WORD else x

    print
    print 'The FIRST sets are as follows:'

    firstsets = first(grammar)

    for lhs in grammar.viewkeys():

        pretty_firstset = \
            string.join(map(label_empty, firstsets[lhs]), ', ')
        
        print 'FIRST(%s) = {%s}' % \
            (lhs, pretty_firstset)
    
    print 'The answer needs to be entered as follows, without any punctuation or separating spaces.'

    for lhs in grammar.viewkeys():

        pretty_firstset = \
            string.join(map(label_empty, firstsets[lhs]), '')
        
        print 'FIRST(%s) = %s' % \
            (lhs, pretty_firstset)
    
    




def exercise_first(grammar):

    answer_re = re.compile('\A[a-z\%s]*\Z' % EMPTY_WORD_PRINTABLE)

    firstsets = first(grammar)

    for lhs in grammar.viewkeys():
            
        assert isnonterminal(lhs)

        answer_obtained = False
        while not answer_obtained:
            answer = raw_input('FIRST(%s) = ' % lhs)

            if answer_re.match(answer):
                answer_obtained = True
            else:
                print MESSAGES['invalid-response']

        user_firstset = set(answer)

        if EMPTY_WORD_PRINTABLE in user_firstset:
            user_firstset.remove(EMPTY_WORD_PRINTABLE)
            user_firstset.add(EMPTY_WORD)

        user_incorrect = user_firstset.difference(firstsets[lhs])

        if EMPTY_WORD in user_incorrect:
            user_incorrect.remove(EMPTY_WORD)
            user_incorrect.add(EMPTY_WORD_PRINTABLE)

        if len(user_incorrect) > 0:
            user_incorrect_pretty = string.join(user_incorrect, ', ')
            print 'These are not in the FIRST set:',\
                user_incorrect_pretty



        user_missing = firstsets[lhs].difference(user_firstset)

        if EMPTY_WORD in user_missing:
            user_missing.remove(EMPTY_WORD)
            user_missing.add(EMPTY_WORD_PRINTABLE)

        if len(user_missing) > 0:
            user_missing_pretty = string.join(user_missing, ', ')
            print 'You have forgotten these:',\
            user_missing_pretty

        if user_firstset == firstsets[lhs]:
            print MESSAGES['correct-response']


def exercise_follow(grammar):

    answer_re = re.compile('\A[a-z]*\Z')

    followsets = follow(grammar)

    for lhs in grammar.viewkeys():
            
        assert isnonterminal(lhs)


        answer_obtained = False
        while not answer_obtained:
            answer = raw_input('FOLLOW(%s) = ' % lhs)

            if answer_re.match(answer):
                answer_obtained = True
            else:
                print MESSAGES['invalid-response']


        if not answer_re.match(answer):
            break

        user_followset = set(answer)

        user_incorrect = user_followset.difference(followsets[lhs])

        if len(user_incorrect) > 0:
            user_incorrect_pretty = string.join(user_incorrect, ', ')
            print 'These terminal symbols are not in the FOLLOW set:',\
                user_incorrect_pretty


        user_missing = followsets[lhs].difference(user_followset)

        if len(user_missing) > 0:
            user_missing_pretty = string.join(user_missing, ', ')
            print 'You have forgotten these terminal symbols:',\
            user_missing_pretty


        if user_followset == followsets[lhs]:
            print MESSAGES['correct-response']



def grammar_has_useless_rules(grammar):
    # FIXME TODO maybe the definition used
    # doesn't make sense

    firstsets = first(grammar)

    for firstset in firstsets.viewitems():
        if len(firstset) == 0:
            return True

    return False
        
        

def gen_grammar(n_nonterminals = 3,
                rhs_per_nonterminal = (1, 3),
                nonterminals_per_rhs = (0, 3),
                terminals_per_rhs = (0, 3)):


    # (min, max) rules a single non-terminal can have
    #rhs_per_nonterminal = (1, 3)

    # (min, max) non-terminals per rhs
    #nonterminals_per_rhs = (0, 2)

    # (min, max) terminals per rhs
    #terminals_per_rhs = (0, 3)

    assert type(n_nonterminals) == int
    assert type(rhs_per_nonterminal) == tuple
    assert type(nonterminals_per_rhs) == tuple
    assert type(terminals_per_rhs) == tuple

    assert n_nonterminals <= len(string.uppercase)
    assert n_nonterminals > 0

    nonterminals = string.uppercase[:n_nonterminals]
    terminals = string.lowercase

    assert len(nonterminals) == n_nonterminals

    # a dict for the grammar we're about to build
    grammar = {}

    for nonterminal in nonterminals:
        
        n_rhs = random.randint(*rhs_per_nonterminal)

        assert not grammar.has_key(nonterminal)

        grammar[nonterminal] = []

        for __ in itertools.repeat(None, n_rhs):

            current_rhs = ''

            remaining_nonterminals = random.randint(
                *nonterminals_per_rhs)

            remaining_terminals = random.randint(
                *terminals_per_rhs)

            while remaining_terminals > 0 \
                  or remaining_nonterminals > 0:
                
                # decide whether to add a non-terminal
                # or a terminal symbol
                add_nonterminal = True

                if remaining_terminals > 0 \
                   and remaining_nonterminals > 0:
                    
                    add_nonterminal = random.choice([True, False])

                elif remaining_nonterminals == 0:
                    add_nonterminal = False
        
                # depending on the decision made above,
                # either add a non-terminal or a terminal
                # symbol to the current production

                if add_nonterminal:
                    current_rhs += random.choice(nonterminals)
                    remaining_nonterminals -= 1

                else:
                    current_rhs += random.choice(terminals)
                    remaining_terminals -= 1

            grammar[nonterminal].append(current_rhs)

    return grammar
            

def print_grammar(g):
    label_empty = lambda x:\
                  EMPTY_WORD_PRINTABLE if x == EMPTY_WORD else x

    for lhs in g.viewkeys():
        pretty_rhs = string.join(map(label_empty, g[lhs]), ' | ')


        print lhs, '->', pretty_rhs


def follow(g):
    followsets = {}

    firstsets = first(g)

    for lhs in g.viewkeys():
        followsets[lhs] = set()

    for n in range(0, 100):

        for lhs, alternatives in g.viewitems():

            assert isnonterminal(lhs)

            for rhs in alternatives:

                trailer = followsets[lhs]

                for symbol in reversed(rhs):
                
                    if isnonterminal(symbol):

                        #followsets[symbol] = followsets[symbol].union(trailer)

                        followsets[symbol].update(trailer)

                        if EMPTY_WORD in firstsets[symbol]:
                            trailer = trailer.union(firstsets[symbol])
                            trailer.discard(EMPTY_WORD)
                            
                        else:
                            trailer = set(firstsets[symbol])

                    else:
                        trailer = set([symbol])

    return followsets




def first(g):
    
    firstsets = {}


    for lhs in g.viewkeys():

        firstsets[lhs] = set()

        if EMPTY_WORD in g[lhs]:
            firstsets[lhs].add(EMPTY_WORD)


    for n in range(1, 20):

        for lhs, alternatives in g.viewitems():

            assert isnonterminal(lhs)

            for rhs in alternatives:

#                firstsets[lhs] = \
#                    first_rhs(rhs, firstsets).union(firstsets[lhs])
                
                firstsets[lhs].update(first_rhs(rhs, firstsets))



    return firstsets


def first_rhs(rhs, firstsets):
    
    assert type(rhs) == str
    assert type(firstsets) == dict

    firstset = set()

    if rhs == EMPTY_WORD:
        return set([EMPTY_WORD])

    for index, symbol in enumerate(rhs):

        if isterminal(symbol):
            firstset.add(symbol)
            break
        else:
            assert isnonterminal(symbol)

            unite = firstsets[symbol].copy()
            unite.discard(EMPTY_WORD)

            #firstset = firstset.union(unite)
            firstset.update(unite)

            is_last = index + 1 == len(rhs)

            if is_last and EMPTY_WORD in firstsets[symbol]:
                firstset.add(EMPTY_WORD)

            if EMPTY_WORD not in firstsets[symbol]:
                break


    return firstset


def first_plus(lhs, rhs, firstsets, followsets):

    firstset_rhs = first_rhs(rhs, firstsets)

    if EMPTY_WORD in firstset_rhs:

        assert lhs in followsets

        return followsets[lhs].union(firstset_rhs)

    else:

        return firstset_rhs

def is_ll1(grammar):
    
    firstsets = first(grammar)

    followsets = follow(grammar)

    for lhs in grammar.viewkeys():
        
        union_first_plus = set()

        for rhs in grammar[lhs]:
            
            first_plus_set = first_plus(lhs, rhs,
                                        firstsets, followsets)

            intersection_nonempty = \
                len(union_first_plus.intersection(first_plus_set)) > 0

            if intersection_nonempty:
                # the given grammar cannot be parsed
                # by a backtrack-free LL(1) parser
                return False
                
            union_first_plus.update(first_plus_set)

    # the given grammar can be parsed by a backtrack-free
    # LL(1) parser
    return True
                    

def get_equivalent_or_insert(container, new_element):
    if new_element in container:
        for element in container:
            if new_element == element: return element

        assert False

    else:
        container.add(new_element)
        return new_element
    

class item_set(set):

    def add(self, new_item):

        merged = False

        for item in super(item_set, self).__iter__():

            if item[:3] == new_item[:3]:
                
                if item[3] != new_item[3]:

                    super(item_set, self).discard(item)
                    
                    merged_item = (item[0],
                                   item[1],
                                   item[2],
                                   item[3].union(new_item[3]))

                    super(item_set, self).add(merged_item)

                    #assert not merged

                    merged = True

        if not merged:
            super(item_set, self).add(new_item)

    def update(self, new_items):
        if not isinstance(new_items, set):
            raise Exception('the argument to update() must ' \
                            'be a set')

        for new_item in new_items:
            self.add(new_item)
                

class state(object):

    def __init__(self, kernel_items, grammar, state_number):

        # item: (lhs, rhs, position of the dot)
        if not self.is_valid_item_set(kernel_items):
            raise Exception('invalid kernel item set')

        self.items = item_set()

        self.items = self.closure(kernel_items, grammar)

        self.grammar = grammar

        self.gotos = {}

        self.shifts = {}

        self.state_number = state_number#id(self)


    def shift(self, terminal, new_state_number):
        if not isterminal(terminal):
            raise Exception('argument not a terminal symbol')

        if terminal not in self.get_shiftable_terminals():
            raise Exception('cannot shift %s' % terminal)

        # the set of items that will form the kernel item
        # set of the new state
        new_kernel_items = item_set()

        for item in self.items:
            lhs, rhs, index_marker, lookahead = item

            if state.item_requires_shift(item) \
               and terminal == rhs[index_marker]:

                new_item = (lhs,
                            rhs,
                            index_marker + 1,
                            lookahead)

                new_kernel_items.add(new_item)

        if len(new_kernel_items) == 0:
            raise Exception('cannot shift "%s"' % terminal)

        new_state = state(new_kernel_items,
                          self.grammar,
                          new_state_number)

        return new_state

    def create_goto_states(self, existing_states):

        for nonterminal in self.get_closure_symbols():

            assert nonterminal in self.get_closure_symbols()

            new_state = get_equivalent_or_insert(
                existing_states,
                state.goto(self, nonterminal, len(existing_states))
            )

            self.gotos[nonterminal] = new_state

            assert nonterminal in self.get_closure_symbols()


    def create_shift_states(self, existing_states):

        for terminal in self.get_shiftable_terminals():
            
            new_state = get_equivalent_or_insert(
                existing_states,
                state.shift(self, terminal, len(existing_states))
            )

            self.shifts[terminal] = new_state
            

    def goto(self, nonterminal, new_state_number):

        if not isnonterminal(nonterminal):
            raise Exception('argument not a nonterminal')

        if not self.grammar.has_key(nonterminal):
            raise Exception('the grammar does not seem ' \
                            'to contain a ' \
                            'non-terminal "%s"' % nonterminal)

        if nonterminal not in self.get_closure_symbols():
            raise Exception('goto via %s not possible' \
                            % nonterminal)

        new_kernel_items = item_set()

        for item in self.items:
            lhs, rhs, index_marker, lookahead = item

            if state.marker_at_nonterminal_in_item(item) \
               and nonterminal == rhs[index_marker]:
                
                new_item = (lhs,
                            rhs,
                            index_marker + 1,
                            lookahead)

                new_kernel_items.add(new_item)

        if len(new_kernel_items) == 0:
            raise Exception('goto not possible')

        new_state = state(new_kernel_items,
                          self.grammar,
                          new_state_number)

        return new_state


    @staticmethod
    def item_get_html(item):
        lhs, rhs, marker_index, lookahead = item

        pretty_lookahead = string.join(lookahead, ', ')

        return '''<tr>
        <td border="0">%s &#8594; %s&bull;%s</td>
        <td border="0">&#123;%s&#125;</td>
        </tr>''' % (lhs, rhs[:marker_index], \
                    rhs[marker_index:], pretty_lookahead)



    def get_html(self, debug = False):
        
        s = '''<
        <table border="1">
        <tr>
        <td border="1" colspan="2">%d</td>
        </tr>''' % self.state_number

        for item in self.items:
            s += state.item_get_html(item)

        if debug:
            s += '''<tr>
            <td border="0" colspan="2">&#123;%s&#125;</td>
            </tr>
            <tr>
            <td border="0" colspan="2">&#123;%s&#125;</td>
            </tr>
            ''' % (string.join(self.get_closure_symbols(), ', '),
                   string.join(self.get_shiftable_terminals(), ', '))

        s += '</table>>'

        return s

    @staticmethod
    def is_valid_item_set(items):
        for lhs, rhs, index_marker, lookahead in items:
            if not isnonterminal(lhs):
                return False

            if index_marker not in range(0, len(rhs) + 1):
                raise False

            for rhs_symbol in rhs:
                if not isterminal(rhs_symbol) \
                   and not isnonterminal(rhs_symbol):
                    raise False


        return True

    
    @staticmethod
    def closure(kernel_items, grammar):

        items = item_set()

        items.update(kernel_items)

        new_items = item_set()

        # TODO FIXME merge items that have the 
        # same lhs, rhs and marker

        for ___ in range(0, 10):

            for item in items:

                if state.marker_at_nonterminal_in_item(item):

                    new_items.update(
                        state.closure_from_item(grammar, item))

            items.update(new_items)

        return items

    def get_shiftable_terminals(self):
        shiftable_terminals = set()

        for item in self.items:
            if state.item_requires_shift(item):
                terminal = \
                    state.get_symbol_at_marker_in_item(item)

                shiftable_terminals.add(terminal)

        return shiftable_terminals

    def get_closure_symbols(self):
        closure_symbols = set()

        for item in self.items:
            lhs, rhs, index_marker, lookahead = item

            if state.marker_at_nonterminal_in_item(item):
                closure_symbols.add(rhs[index_marker])
                
        return closure_symbols


    @staticmethod
    def closure_from_item(grammar, item):

        firstsets = first(grammar)

        assert state.marker_at_nonterminal_in_item(item)

        new_items = set()
        
        lhs, rhs, index_marker, lookahead = item

        closure_symbol = rhs[index_marker]

        assert grammar.has_key(closure_symbol)

        # the part of the rhs after the non-terminal
        # we'll need this to compute the new lookahead set
        rest = rhs[index_marker + 1:]

        new_lookahead = first_rhs(rest, firstsets)

        # if the 'rest' is nullable, then the new
        # lookahead is the union of the FIRST set
        # and the old lookahead
        if EMPTY_WORD in new_lookahead:
            new_lookahead.discard(EMPTY_WORD)
            new_lookahead.update(lookahead)

            
        for closure_symbol_rhs in grammar[closure_symbol]:
            
            new_item = (closure_symbol,
                        closure_symbol_rhs,
                        0, # index marker at the beginning
                        frozenset(new_lookahead))

            new_items.add(new_item)

        return new_items

    @staticmethod
    def get_symbol_at_marker_in_item(item):
        lhs, rhs, index_marker, lookahead = item

        if index_marker not in range(0, len(rhs)):
            raise Exception('the marker is at the end of the RHS')

        return rhs[index_marker]

    @staticmethod
    def item_requires_shift(item):
        lhs, rhs, index_marker, lookahead = item

        return len(rhs) > 0 \
            and index_marker in range(0, len(rhs)) \
            and isterminal(rhs[index_marker])

    @staticmethod
    def marker_at_nonterminal_in_item(item):
        lhs, rhs, index_marker, lookahead = item

        return len(rhs) > 0 \
            and index_marker in range(0, len(rhs)) \
            and isnonterminal(rhs[index_marker])


    def __eq__(self, other):
        if not isinstance(other, state):
            return False

        return self.items == other.items

    def __hash__(self):
        return hash(len(self.items))




def build_state_machine(grammar, start_symbol = 'S'):
    
    end_of_input_marker = '$'

    # complain if the grammar doesn't contain the start symbol
    if not grammar.has_key(start_symbol):
        raise Exception('the grammar is missing the ' \
                        'start symbol "%s"' % start_symbol)

    first_item = (
        'Z', # auxiliary non-terminal
        start_symbol, # the RHS consists of the start symbol only
        0, # the marker is at the beginning
        frozenset([end_of_input_marker]) # the initial lookahead
    )

    first_state = state(set([first_item]), grammar, 0)


    states = set([first_state])

    previously_existing_states = set()

    # keep processing new states until no new states are produced
    while True:

        assert states.issuperset(previously_existing_states)

        new_states = states.difference(previously_existing_states)

        # if no states have been added in the previous loop,
        # then quit
        if len(new_states) == 0:
            break

        previously_existing_states = set(states)

        for machine_state in new_states:
        
            machine_state.create_goto_states(states)

            machine_state.create_shift_states(states)

        

    return states

        
def make_graph_for_state_machine(states):
    s = Digraph('states',
                node_attr={'shape': 'plaintext'},
                format='svg')

    for crnt_state in states:
        
        s.node(str(id(crnt_state)), crnt_state.get_html())

        for nonterminal, goto_state in crnt_state.gotos.viewitems():

            s.edge(str(id(crnt_state)),
                   str(id(goto_state)),
                   label=nonterminal)
            


        for terminal, shift_state in crnt_state.shifts.viewitems():
            
            s.edge(str(id(crnt_state)),
                   str(id(shift_state)),
                   label=terminal)
    
    s.view()





#g={'S':['Aa'],'A':['b', 'Sx']}
#g = gen_grammar(2, (1,2), (0,2), (0,3))
#states = build_state_machine(g, 'A')
#make_graph_for_state_machine(states)

#print_grammar(g)

if '__main__' == __name__:
    main()
