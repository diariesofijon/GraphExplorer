#!/usr/bin/env python

'''
The module cotains widle used clear functions that's based on functional
programming priciples.
'''

from typing import List, Tuple


def get_ids(name: str, separeter: str='-') -> List[int]:
    ''' Clear function that implement name to ids '''
    if len((tmp := name.split(separeter))) == 2:
        return list(range(int(tmp[0]), int(tmp[1])+1))
    return [int(name)]

def eisenhower_part_spliter(tmp: str) -> Tuple[str]:
    ''' Split eisenhower part's name to a Tuple '''
    if len((splited := tmp.split('.'))) == 1:
        return splited[0], ''
    return splited[0], splited[1]

# TODO: don't foget legace convert element and make the idea to
# TODO: uneffectable deletion legace come true
def separete_from_text_element(tmp: str, separeter: str=':'):
    ''' like that 12. A|B: 3(10), 4(13,46,118) '''
    match len((splited:=tmp.split(separeter))):
        case 0:
            return 'splited', 'splited'
        case 1:
            return splited, splited
        case _:
            return splited[0], splited[1]

def is_bipartite(edges: List):
    '''
    The function expects that the vertex has only two tops which
    indicate the best varienty of the graph.
    '''
    return len(edges) == 2 and edges[0] == edges[1]
