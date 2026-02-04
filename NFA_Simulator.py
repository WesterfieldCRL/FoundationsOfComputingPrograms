num_states = int(input())
num_transitions = int(input())

#node_list: dict[str, dict[str, list[tuple[str, bool]]]] = {}

node_list: dict[str, dict[str, set[str]]] = {}

transition_set = set()

for i in range(num_transitions):
    nodefrom, transition, nodeto = input().split()
    # transition_set.add(transition)
    # If the key exists in the dictionary
    if nodefrom in node_list:
        if transition in node_list[nodefrom]:
            node_list[nodefrom][transition].add(nodeto)
        else:
            node_list[nodefrom][transition] = {nodeto}
    else:
        node_list[nodefrom] = {transition: {nodeto}}

num_final_states = int(input())

final_states = set()

for i in range(num_final_states):
    final_states.add(input())

num_given_strings = int(input())

def NFA_simulator1(input_string: str, curr_state: str, visited_states: set[str] | None = None) -> list[str]:

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
            potential_epsilon_states = node_list[curr_state].get("eps")
            if potential_epsilon_states is not None:

                for epsilon_state in potential_epsilon_states:
                    potential_end_states = NFA_simulator1(input_string, epsilon_state[0], visited_states)

                    return_states += potential_end_states
    else:
        potential_states = set()

        if node_list.get(curr_state, False):
            
            temp = node_list[curr_state].get("eps")
            if temp is not None:
                potential_states = potential_states.union(temp)
            
            temp = node_list[curr_state].get(input_string[0], False)
            if temp:
                potential_states = potential_states.union(node_list[curr_state][input_string[0]])
                
        for state in potential_states:
            # Is this an epsilon transition?

            temp = []

            if not state[1]:
                temp = NFA_simulator1(input_string[1:], state[0])
            else:
                # Need to check if already added this node to possible states
                temp = NFA_simulator1(input_string, state[0], visited_states)
            

            return_states += temp
        

    return return_states

def epsilon_handler(curr_state: str) -> set[str]:
    return_set: set[str] = {curr_state}
    
    curr_node = node_list.get(curr_state)
    states_to_visit = []

    if curr_node is not None:
        possible_states = node_list[curr_state].get("eps")
        if possible_states is not None:
            return_set = return_set.union(possible_states)
            states_to_visit += possible_states
        
        possible_states = set()
        while True:
            if possible_states:
                state = states_to_visit.pop(0)
                if node_list.get(state) is not None:
                    possible_states = node_list[state].get("eps")
                    if possible_states is not None:
                        return_set = return_set.union(possible_states)
                        for state in possible_states:   
                            if state not in return_set:
                                states_to_visit.append(state)
            else:
                break

    return return_set

def NFA_simulator(input_string: str, curr_state: str) -> set[str]:

    return_states = set()
    potential_states = set()

    curr_state_with_epsilon_expansion = epsilon_handler(curr_state)
    #print(curr_state_with_epsilon_expansion)

    # epsilon time baby
    #print(f"currstate = {curr_state}, input = {input_string} potential_states = {potential_states}")

    if not input_string:
        return_states = curr_state_with_epsilon_expansion
    else:
        for curr_state_expanded in curr_state_with_epsilon_expansion:
            if not ((node_list.get(curr_state_expanded) is None) or (node_list[curr_state_expanded].get(input_string[0]) is None)):
                #return return_states
            # else:
                potential_states = node_list[curr_state_expanded][input_string[0]]
    
    for state in potential_states:
        return_states = return_states.union(NFA_simulator(input_string[1:], state))

    return return_states

# Convert the NFA into a DFA to hopefully speed everything up

DFA_node_list: dict[str, dict[str, set[str]]]  = {} # not using the list but I don't feel like making the necessary changes to NFA_simulator to allow for that

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
                        DFA_node_list[curr_state] = {}

                    possible_state_list = NFA_simulator(transition, state)
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
            DFA_node_list[curr_state][dict_transtion] = {flattened_str}
            #print(flattened_state_dict[dict_transtion])
            NFA_to_DFA_inator(flattened_str)
        

possible_start_states = NFA_simulator("", "0")
print(possible_start_states)
flattened_start_states = '_'.join(sorted(possible_start_states))

NFA_to_DFA_inator(flattened_start_states)
node_list = DFA_node_list

# print(node_list)

for i in range(num_given_strings):
    input_string = input()

    accepted = False
    for end_state in NFA_simulator(input_string, flattened_start_states):
        #print(f"end_state = {end_state}")
        split_states = end_state.split("_")
        for result_state in split_states:
            if result_state in final_states:
                accepted = True
                break

    if accepted:
        print("accept")
    else:
        print("reject")

# for node in node_list:
#     for transition in node_list[node]:
#         for result_node in node_list[node][transition]:
#             print(f"{node}: {transition}: {result_node[0]}")