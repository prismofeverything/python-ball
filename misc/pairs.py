def condition_list(atoms, conditions):
    final = 1

    for ato in atoms:
        for cond in conditions:
            final = cond(ato)
            if not final:
                break
        if not final:
            break

    return final

conditions = [lambda x: x != '\n',
              lambda x: x != '\t',
              lambda x: x != '\ ',
              lambda x: x > chr(64),
              lambda x: x < chr(123),
              lambda x: x < chr(91) or x > chr(96)]

def count_pairs(file):
    text = open(file).read()
    pairs = {}
    index = 0;
    
    while index < len(text) - 1:
        a = text[index]
        b = text[index + 1]
        
        if condition_list([a, b], conditions) and a != b:
            pair = '' + a.lower() + b.lower()

            if not pairs.has_key(pair):
                pairs[pair] = 0

            pairs[pair] += 1

        index += 1

    return pairs

def swap(ls, a, b):
    c = ls[a]
    ls[a] = ls[b]
    ls[b] = c

def sort_pairs(pairs):
    unsorted = pairs.items()
    sorted = []

    for pair in unsorted:
        balanced = 0
        pair_index = len(sorted)
        sorted.append(pair)
        pair_frequency = pair[1]

        while not balanced and pair_index > 0:
            sort = sorted[pair_index - 1]
            if pair_frequency > sort[1]:
                swap(sorted, pair_index, pair_index - 1)
                pair_index -= 1
            else:
                balanced = 1

    return sorted

def sort_count(file):
    return sort_pairs(count_pairs(file))

