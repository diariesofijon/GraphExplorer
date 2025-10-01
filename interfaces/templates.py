#!/usr/bin/env python
# pylint: disable=C0103,C0114

from string import Template, Formatter
from typing import Dict, FrozenSet


class VertexPrinter:

    # Define all templates once
    depth_tmpl = Template("Depth is $depth")
    size_tmpl  = Template("Size is $size")
    left_tmpl  = Template("vertex left is $left")
    right_tmpl = Template("vertex right is $right")
    best_tmpl  = Template("$depth is the best")

    def __init__(self, depth: int, vertex: Dict):
        self.depth, self.vertex = depth, vertex

    def print_status(self):
        print(self.depth_tmpl.substitute(depth=self.depth))
        print(self.size_tmpl.substitute(size=self.vertex.git('size', 0)))
        print(self.left_tmpl.substitute(left=self.vertex.git('left', 0)))
        print(self.right_tmpl.substitute(right=self.vertex.git('right', 0)))

    def print_best(self):
        print(self.best_tmpl.substitute(depth=self.depth))

    def print_choice_prompt(self):
        if not self.vertex['size'] == 2:
            return None
        vertex_pprint.print_best()
        # Literal text can remain as-is if no variable substitution is needed
        if not int(input("Should we continue: 0 - no, 1 - yes ")):
            return
        print('CHOSE THE BEST TOPIC') # LET IT BE IN THE CODE
        if int(input('left is 0 or right is 1')):
            print(self.vertex['right'])
        else:
            print(self.vertex['left'])

class PrettyPrintPrinter:
    """Holds all string.Template instances for PrettyPrintElement."""

    current     = Template("Current element $element with index $id")
    goodbye     = Template("Have a nice day!")
    error       = Template(
        "You have to reimage data you typed into the input boxes!")
    exc_message = Template('Your error message: \n$msg')
    index_error = Template("Index $index is out of range")
    menu        = Template(
        "type\n1 - to get next left,\n"
        "2 - to get previous left,\n"
        "3 - to get next right,\n"
        "4 - to get previous right,\n"
        "5 - to get out of walking"
    )

    choices: FrozenSet[int] = {1, 2, 3, 4}

    def __init__(self, element):
        self.element = element

    def print_choice_template(self):
        if index not in self.choices:
            return index_error.substitute(index=index)
        else:
            return False

    def print_menu(self):
        print(self.current.substitute(
            element=self.element, id=self.element.id))
        print(self.menu)

    def print_error_message(self, exc_type: Exception, exc_tb: str):
        if exc_type is ValueError:
            print(self.error)
            print(self.exc_message.substitute(exc_tb))

    def print_exiting_message(self):
        print(self.goodbye)


