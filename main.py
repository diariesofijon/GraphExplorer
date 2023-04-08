#!/usr/bin/env python

from pprint import pprint
import graph_engine
import sys


def main():
    ''' Converting list of links to a graph '''
    print('input the graph')
    if sys.argv[0] == '-from_console':
        tmp = input()
    else:
        with open('graph_links.txt') as file:
            tmp = file.read()
    print('\n\n\n')
    srg = graph_engine.StringRepresentationGraph(tmp=tmp)
    print('\n\n\n')
    print(str(srg))
    with open('output.txt', 'w') as file:
        file.write(str(srg))

if __name__ == '__main__':
    main()
