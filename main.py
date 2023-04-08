#!/usr/bin/env python

from pprint import pprint
import graph_engine


def main():
    ''' Converting list of links to a graph '''
    print('input the graph')
    tmp = input()
    print('\n\n\n')
    srg = graph_engine.StringRepresentationGraph(tmp=tmp).to_pythonic()
    print('\n\n\n')
    pprint(repr(srg))

if __name__ == '__main__':
    main()
