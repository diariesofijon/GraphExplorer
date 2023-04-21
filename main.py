#!/usr/bin/env python

from pprint import pprint
import graph_engine
import sys


def main():
    ''' Converting list of links to a graph '''
    print('input the graph')
    print('\n\n\n')
    if len(sys.argv) and sys.argv[0] == '-from_console':
        print(1)
        srg = graph_engine.StringByStringRegularExpressionMask(tmp=input())
    elif (len(sys.argv)-1) and (file := sys.argv[1]) and sys.argv[1].endswith('.txt'):
        print(2)
        srg = graph_engine.StringByStringRegularExpressionMask(file=file)
    else:
        print(3)
        srg = graph_engine.StringByStringRegularExpressionMask()
    print('\n\n\n')
    print(str(srg))
    with open('output.txt', 'w') as file:
        file.write(str(srg))

if __name__ == '__main__':
    main()
