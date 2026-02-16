num_rules = int(input())

# key is produced value, value is all variables that produce that value, i.e. [production, head]
what_produces_characters: dict[str, set[str]] = {}
what_produces_variables: dict[tuple[str,str], set[str]] = {} # using a tuple to avoid lots of string concatenation

start_variable = ""

for i in range(num_rules):
    head, production = input().split()

    if len(start_variable) < 1:
        start_variable = head

    if len(production) > 1:
        # production is a pair of variables
        if what_produces_variables.get((production[0], production[1])) is not None:
            what_produces_variables[(production[0], production[1])] = {head}
        else:
            what_produces_variables[(production[0], production[1])].add(head)
    else:
        # production is a symbol
        if what_produces_characters.get(production) is not None:
            what_produces_characters[production] = {head}
        else:
            what_produces_characters[production].add(head)

def CYK_parser(s: str) -> bool:

    str_len = len(s)

    # initialize the 2d list
    CFG_table: list[list[set[str]]] = [
        [set() for _ in range(str_len)]
        for _ in range(str_len)
    ]

    # first row of table
    for j in range(str_len):
        CFG_table[0][j].update(what_produces_characters[s[j]])
    
    # second row of the table
    for j in range(str_len-1):
        first_variables = CFG_table[0][j]
        second_variables = CFG_table[0][j+1]

        productions = (
            what_produces_variables.get((A, B), set())
            for A in first_variables
            for B in second_variables
        )

        CFG_table[1][j].update(*productions)


    # rest of the table
    for i in range(2, str_len):
        for j in range(str_len-i):

            for pair in range(0, i):
                x1 = pair
                y1 = j
                x2 = (i-1) - pair
                y2 = (j + 1) + pair

                first_variables = CFG_table[x1][y1]
                second_variables = CFG_table[x2][y2]

                productions = (
                    what_produces_variables.get((A, B), set())
                    for A in first_variables
                    for B in second_variables
                )

                CFG_table[i][j].update(*productions)
                

    if start_variable in CFG_table[str_len-1][0]:
        return True

    return False

num_strings = int(input())

for i in range(num_strings):
    string = input()

    if CYK_parser(string):
        print("yes")
    else:
        print("no")
