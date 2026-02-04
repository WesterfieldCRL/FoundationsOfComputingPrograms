from functools import lru_cache

num_states = int(input())
num_transitions = int(input())

node_list: dict[str, dict[str, list[tuple[str, bool]]]] = {}

transition_set = set()

contains_epsilon_transitions = False

for i in range(num_transitions):
    nodefrom, transition, nodeto = input().split()
    epsilon_transition = False
    if transition == "eps":
        contains_epsilon_transitions = True
        epsilon_transition = True
    else:
        transition_set.add(transition)
    # If the key exists in the dictionary
    if nodefrom in node_list:
        if transition in node_list[nodefrom]:
            node_list[nodefrom][transition].append((nodeto, epsilon_transition))
        else:
            node_list[nodefrom][transition] = [(nodeto, epsilon_transition)]
    else:
        node_list[nodefrom] = {transition: [(nodeto, epsilon_transition)]}

num_final_states = int(input())

final_states = set()

for i in range(num_final_states):
    final_states.add(input())

@lru_cache(maxsize=num_states*10)
def NFA_simulator(input_string: str, curr_state: str) -> list[str]:
    
    return_states = []

    if not input_string:
        return_states = [curr_state]
        if node_list.get(curr_state, False):
            temp = node_list[curr_state].get("eps", False)
            if temp:
                potential_epsilon_states = temp

                for epsilon_state in potential_epsilon_states:
                    potential_end_states = NFA_simulator(input_string, epsilon_state[0])


                    return_states += potential_end_states
    else:
        potential_states = []

        if node_list.get(curr_state, False):
            
            temp = node_list[curr_state].get("eps", False)
            if temp:
                potential_states += temp
            
            temp = node_list[curr_state].get(input_string[0], False)
            if temp:
                potential_states += node_list[curr_state][input_string[0]]
                
        for state in potential_states:
            # Is this an epsilon transition?

            temp = []

            if not state[1]:
                temp = NFA_simulator(input_string[1:], state[0])
            else:
                # Need to check if already added this node to possible states
                temp = NFA_simulator(input_string, state[0])
            

            return_states += temp
        

    return return_states

def NFA_simulator_with_epsilons_and_knuckles(input_string: str, curr_state: str, visited_states: set[str] = None):

    if visited_states is None:
        visited_states = set()

    #print(f"curr_state = {curr_state}, input = {input_string}")
    if curr_state in visited_states:
        #print(f"{curr_state}, {visited_states}")
        return []
    else:
        #print(f"{curr_state}, {visited_states}")
        visited_states.add(curr_state)

    return_states = []

    if not input_string:
        return_states = [curr_state]
        if node_list.get(curr_state, False):
            temp = node_list[curr_state].get("eps", False)
            if temp:
                potential_epsilon_states = temp

                for epsilon_state in potential_epsilon_states:
                    potential_end_states = NFA_simulator_with_epsilons_and_knuckles(input_string, epsilon_state[0], visited_states)


                    return_states += potential_end_states
    else:
        potential_states = []

        if node_list.get(curr_state, False):
            
            temp = node_list[curr_state].get("eps", False)
            if temp:
                potential_states += temp
            
            temp = node_list[curr_state].get(input_string[0], False)
            if temp:
                potential_states += node_list[curr_state][input_string[0]]
                
        for state in potential_states:
            # Is this an epsilon transition?

            temp = []

            if not state[1]:
                temp = NFA_simulator_with_epsilons_and_knuckles(input_string[1:], state[0])
            else:
                # Need to check if already added this node to possible states
                temp = NFA_simulator_with_epsilons_and_knuckles(input_string, state[0], visited_states)
            

            return_states += temp
        

    return return_states

# Convert the NFA into a DFA to hopefully speed everything up

DFA_node_list: dict[str, dict[str, str]]  = {} # not using the tuple or the list but I don't feel like making the necessary changes to NFA_simulator to allow for that

set_of_all_states = set()

def NFA_to_DFA_inator(curr_state: str = "0"):

    
    # I know each transtion is one character which is why this works
    unflattened_states = curr_state.split("_")

    flattened_state_dict: dict[str, set[str]] = {}

    for state in unflattened_states:
        curr_node = node_list.get(state)
        if curr_node is not None:
            for transition in curr_node:
                #print(transition)
                if not transition == "eps": # Ignoring epsilon transitions because NFA_simulator should handle those

                    if DFA_node_list.get(curr_state) is None:
                        set_of_all_states.add(curr_state)
                        DFA_node_list[curr_state] = {}

                    if not contains_epsilon_transitions:
                        possible_state_list = NFA_simulator(transition, state)
                    else:
                        possible_state_list = NFA_simulator_with_epsilons_and_knuckles(transition, state)
                    #print(possible_state_list)
                    flattened_states: set[str] = set()
                    for possible_state in possible_state_list:
                        flattened_states.add(possible_state)
                    
                    # Needs to be sorted so that if other nodes output this combined node as a possible state then they point to the same node
                    # flattened_states = ''.join(sorted(flattened_states))

                    if flattened_state_dict.get(transition) is not None:
                        # flattened_state_dict[transition] = ''.join(sorted(flattened_states + flattened_state_dict[transition]))
                        flattened_state_dict[transition].update(flattened_states)
                    else:
                        flattened_state_dict[transition] = flattened_states

    for dict_transtion in flattened_state_dict:
        flattened_str = '_'.join(sorted(flattened_state_dict[dict_transtion]))
        if DFA_node_list[curr_state].get(dict_transtion) is None:
            DFA_node_list[curr_state][dict_transtion] = flattened_str
            set_of_all_states.add(flattened_str)
            #print(flattened_state_dict[dict_transtion])
            NFA_to_DFA_inator(flattened_str)
        

# Handle start state in case of epsilon on start state
if not contains_epsilon_transitions:
    possible_start_states = NFA_simulator("", "0")
else:
    possible_start_states = NFA_simulator_with_epsilons_and_knuckles("", "0")

flattened_start_states = '_'.join(sorted(possible_start_states))

NFA_to_DFA_inator(flattened_start_states)
#node_list = DFA_node_list

print(len(set_of_all_states))
print(sum(len(inner) for inner in DFA_node_list.values()))

renamed_states: dict[str, str] = {}
renamed_states[flattened_start_states] = "0"

renaming_index = 0

# print transitions
for state in DFA_node_list:
    from_state = state
    renamed_from_state = renamed_states.get(from_state)
    if renamed_from_state is not None:
        from_state = renamed_from_state
    else:
        renaming_index += 1
        new_from_state = str(renaming_index)
        renamed_states[from_state] = new_from_state
        from_state = new_from_state


    for transition in DFA_node_list[state]:
        to_state = DFA_node_list[state][transition]
        renamed_to_state = renamed_states.get(to_state)
        if renamed_to_state is not None:
            to_state = renamed_to_state
        else:
            renaming_index += 1
            new_to_state = str(renaming_index)
            renamed_states[to_state] = new_to_state
            to_state = new_to_state

        print(f"{from_state} {transition} {to_state}")

set_of_final_states = set()
for state in set_of_all_states:
    split_states = state.split("_")
    contains_final_state = False
    for result_state in split_states:
        if result_state in final_states:
            contains_final_state = True
    
    if not contains_final_state:
        set_of_final_states.add(state)

print(len(set_of_final_states))
for state in set_of_final_states:
    print(renamed_states[state])