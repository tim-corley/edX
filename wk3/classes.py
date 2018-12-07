#!/usr/bin/env python3

# classes are used to define/build new types (built-in types = strings, lists, boolean)
# to create a new tpye called "point":
# define a new class of things called Points
class Point:

    # init function saying "when I create a new point, what info is needed?"
    # self = variable representing the object (point) itself
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 5)
print(p.x)
print(p.y)
