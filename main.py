#!/usr/bin/env python

from pprint import pprint
import graph_engine
import sys


def main():
    ''' Converting list of links to a graph '''
    print('input the graph')
    print('\n\n\n')
    if sys.argv[0] and sys.argv[0] == '-from_console':
        srg = graph_engine.StringRepresentationGraph(tmp=(tmp := input()))
    elif (file := sys.argv[1]) and sys.argv[1].endswith('.txt'):
        srg = graph_engine.StringRepresentationGraph(file))
    else:
        srg = graph_engine.StringRepresentationGraph()
    print('\n\n\n')
    print(str(srg))
    with open('output.txt', 'w') as file:
        file.write(str(srg))

if __name__ == '__main__':
    main()
