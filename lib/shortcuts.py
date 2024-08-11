#!/usr/bin/env python

from typing import List, Tuple


def get_ids(name: str) -> List[int]:
    ''' Clear function that implement name to ids '''
    if len((tmp := name.split('-'))) == 2:
        return list(range(int(tmp[0]), int(tmp[1])+1))
    return [int(name)]

def eisenhower_part_spliter(tmp: str) -> Tuple[str]:
    ''' Split eisenhower part's name to a Tuple '''
    if len((splited := tmp.split('.'))) == 1:
        return splited[0], ''
    return splited[0], splited[1]

def separete_from_text_element(tmp: str):
    ''' like that 12. A|B: 3(10), 4(13,46,118) '''
    match len((splited:=tmp.split(':'))):
        case 0:
            return 'splited', 'splited'
        case 1:
            return splited, splited
        case _:
            return splited[0], splited[1]
