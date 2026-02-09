num_states = int(input())
num_transitions = int(input())

node_list: dict[str, dict[str, set[str]]] = {}

transition_set = set()

set_of_all_transitions = set()

for i in range(num_transitions):
    nodefrom, transition, nodeto = input().split()
    # transition_set.add(transition)
    # If the key exists in the dictionary
    if not transition == "eps":
        set_of_all_transitions.add(transition)

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


def epsilon_handler(curr_state: str) -> set[str]:
    
    new_nodes = [curr_state]
    for state in new_nodes:
        curr_node = node_list.get(state)
        if curr_node is not None:
            epsilon_transitions = curr_node.get("eps", set())
            #return_set = return_set.union(epsilon_transitions)
            for new_node in epsilon_transitions:
                if new_node not in new_nodes:
                    new_nodes.append(new_node)


    return set(new_nodes)

def NFA_simulator(input_string: str, curr_state: str) -> set[str]:

    return_states = set()
    potential_states = set()

    curr_state_with_epsilon_expansion = epsilon_handler(curr_state)

    if not input_string:
        return_states = curr_state_with_epsilon_expansion
    else:
        for curr_state_expanded in curr_state_with_epsilon_expansion:
            if not ((node_list.get(curr_state_expanded) is None) or (node_list[curr_state_expanded].get(input_string[0]) is None)):
                potential_states = potential_states.union(node_list[curr_state_expanded][input_string[0]])
    
    for state in potential_states:
        return_states = return_states.union(NFA_simulator(input_string[1:], state))

    return return_states

# Convert the NFA into a DFA to hopefully speed everything up

DFA_node_list: dict[str, dict[str, set[str]]]  = {} # not using the list but I don't feel like making the necessary changes to NFA_simulator to allow for that

set_of_all_states = set()

def NFA_to_DFA_inator(curr_state: str = "0"):

    
    # I know each transtion is one character which is why this works
    unflattened_states = curr_state.split("_")

    flattened_state_dict: dict[str, set[str]] = {}

    for state in unflattened_states:
        curr_node = node_list.get(state)
        if curr_node is not None:
            for transition in curr_node:
                #print(f"{transition} in {state}")
                if not transition == "eps": # Ignoring epsilon transitions because NFA_simulator should handle those

                    if DFA_node_list.get(curr_state) is None:
                        set_of_all_states.add(curr_state)
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
                        #print(f"before: {flattened_state_dict[transition]}")
                        flattened_state_dict[transition].update(flattened_states)
                        #print(f"after: {flattened_state_dict[transition]}")
                    else:
                        flattened_state_dict[transition] = flattened_states

    for dict_transtion in flattened_state_dict:
        flattened_str = '_'.join(sorted(flattened_state_dict[dict_transtion]))
        #print(f"{flattened_str} try1")
        if DFA_node_list[curr_state].get(dict_transtion) is None:
            DFA_node_list[curr_state][dict_transtion] = {flattened_str}

            set_of_all_states.add(flattened_str)

            NFA_to_DFA_inator(flattened_str)
        

possible_start_states = NFA_simulator("", "0")
#print(possible_start_states)
flattened_start_states = '_'.join(sorted(possible_start_states))

NFA_to_DFA_inator(flattened_start_states)
node_list = DFA_node_list
#node_list = DFA_node_list

number_of_states = len(set_of_all_states)
#print(number_of_states)
#print(sum(len(inner) for inner in DFA_node_list.values()))

renamed_states: dict[str, str] = {}
renamed_states[flattened_start_states] = "0"

renaming_index = 0

sorted_transitions_list = sorted(set_of_all_transitions)

print_list = []

# print transitions
for state in set_of_all_states:

    from_state = state
    renamed_from_state = renamed_states.get(from_state)
    if renamed_from_state is not None:
        from_state = renamed_from_state
    else:
        renaming_index += 1
        new_from_state = str(renaming_index)
        renamed_states[from_state] = new_from_state
        from_state = new_from_state


    for transition in sorted_transitions_list:
        if DFA_node_list.get(state) is not None and DFA_node_list[state].get(transition) is not None:
            to_state = DFA_node_list[state][transition]
            to_state = to_state.pop()
            renamed_to_state = renamed_states.get(to_state)
            if renamed_to_state is not None:
                to_state = renamed_to_state
            else:
                renaming_index += 1
                new_to_state = str(renaming_index)
                renamed_states[to_state] = new_to_state
                to_state = new_to_state

            print_list.append(f"{from_state} {transition} {to_state}")
        else:
            renamed_sink_state = renamed_states.get("sink")
            if renamed_sink_state is not None:
                print_list.append(f"{from_state} {transition} {renamed_sink_state}")
            else:
                renaming_index += 1
                new_sink_state = str(renaming_index)
                renamed_states["sink"] = new_sink_state
                print_list.append(f"{from_state} {transition} {new_sink_state}")

print_sink = renamed_states.get("sink")
if print_sink is not None:
    for transition in set_of_all_transitions:
        print_list.append(f"{print_sink} {transition} {print_sink}")
    print(number_of_states + 1)
else:
    print(number_of_states)
print_list.sort()

print(len(print_list))

for item in print_list:
    print(item)

set_of_final_states = set()
for state in set_of_all_states:
    split_states = state.split("_")
    contains_final_state = False
    for result_state in split_states:
        if result_state in final_states:
            contains_final_state = True
    
    if not contains_final_state:
        set_of_final_states.add(state)


if print_sink is not None:
    set_of_final_states.add("sink")

sorted_final_states = []
for state in set_of_final_states:
    sorted_final_states.append(renamed_states[state])

sorted_final_states.sort()
print(len(set_of_final_states))
for state in sorted_final_states:
    print(state)



