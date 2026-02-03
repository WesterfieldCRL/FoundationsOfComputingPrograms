from functools import lru_cache

num_states = int(input())
num_transitions = int(input())

node_list: dict[str, dict[str, list[tuple[str, bool]]]] = {}

transition_set = set()

for i in range(num_transitions):
    nodefrom, transition, nodeto = input().split()
    epsilon_transition = False
    if transition == "eps":
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

num_given_strings = int(input())

#@lru_cache(maxsize=num_states*10)
def NFA_simulator(input_string: str, curr_state: str, visited_states: set[str] = None) -> list[str]:
    
    if visited_states is None:
        visited_states = set()

    return_states = []
    #print(f"curr_state = {curr_state}, input = {input_string}")
    if curr_state in visited_states:
        #print(f"{curr_state}, {visited_states}")
        return [curr_state]
    else:
        #print(f"{curr_state}, {visited_states}")
        visited_states.add(curr_state)

    if not input_string:
        return_states = [curr_state]
        if node_list.get(curr_state, False):
            temp = node_list[curr_state].get("eps", False)
            if temp:
                potential_epsilon_states = temp

                for epsilon_state in potential_epsilon_states:
                    potential_end_states = NFA_simulator(input_string, epsilon_state[0], visited_states)


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
                temp = NFA_simulator(input_string, state[0], visited_states)
            

            return_states += temp
        

    return return_states

# Convert the NFA into a DFA to hopefully speed everything up

DFA_node_list: dict[str, dict[str, list[tuple[str, bool]]]]  = {} # not using the tuple or the list but I don't feel like making the necessary changes to NFA_simulator to allow for that

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

                    possible_state_list = NFA_simulator(transition, state) # Get possible states from here, cant get them from node list because of epsilon transitions
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
            DFA_node_list[curr_state][dict_transtion] = [(flattened_str, False)]
            #print(flattened_state_dict[dict_transtion])
            NFA_to_DFA_inator(flattened_str)
        

# Handle start state in case of epsilon on start state
possible_start_states = NFA_simulator("", "0")

flattened_start_states = '_'.join(sorted(possible_start_states))

NFA_to_DFA_inator(flattened_start_states)
node_list = DFA_node_list

for i in range(num_given_strings):
    input_string = input()

    accepted = False
    #print("vibe check")
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