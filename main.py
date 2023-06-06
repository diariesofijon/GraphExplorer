#!/usr/bin/env python
# pylint: disable=C0103,C0114

'''
    TODO: make DFS step by step
        1. function as bound method for the graph which fitler them by tree belonging
        2. function as bound method for the graph which filter them by tree absent
        3. function that sort elements of the graph by the matrix's part belonging
        4. matrix data
        5. visualistaion
'''

from data_structures import StringByStringRegularExpressionMask
import cli


def main():
    ''' Converting list of links to a graph '''

    # TODO: make clear console interface
    srg = StringByStringRegularExpressionMask()

    with open('output.txt', 'w', encoding='utf8') as file:
        file.write(str(srg))

    cli.show_pretty_graph(srg, 3)

if __name__ == '__main__':
    print('input the graph')
    print('\n\n\n')
    main()
