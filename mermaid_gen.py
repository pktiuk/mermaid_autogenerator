#!/usr/bin/env python3

import string
import CppHeaderParser
import sys
import string


class CppGraph:
    def __init__(self):
        # output string
        self.output = "classDiagram\n"
        # pre-defined signs and symbols
        self.PRIVATE_SIGN = '-'
        self.PUBLIC_SIGN = '+'

        # others
        self.all_of_classes = dict()

    def loadFile(self, header_file: str):
        self.cpp_header = CppHeaderParser.CppHeader(header_file)
        self.all_of_classes.update(self.cpp_header.classes)

    def generateClassDiagram(self):
        for className, classFile in self.all_of_classes.items():
            self.output += "\tclass "+className+"{\n"

            for method in classFile["methods"]["public"]:
                self.loadMethod(method)
            for method in classFile["methods"]["private"]:
                self.loadMethod(method, False)

            for property in classFile["properties"]["public"]:
                self.loadProperty(property)
            for property in classFile["properties"]["private"]:
                self.loadProperty(property, False)

            self.output += "\t}\n\n"

    def loadMethod(self, method, is_public: bool = True):
        if is_public:
            self.output += "\t\t+" + method["name"]
        else:
            self.output += "\t\t-" + method["name"]
        self.output += "("
        for param in method["parameters"]:
            self.output += param["name"] + ", "
        # remove excessive ", " if they were added
        if len(method["parameters"]) != 0:
            self.output = self.output[0:-2]

        self.output += ")"

        if method["returns"].find("void") == -1:
            self.output += ": " + method["returns"]
        self.output += "\n"

    def loadProperty(self, property, is_public: bool = True):
        if is_public:
            self.output += "\t\t+" + property["name"] + "\n"
        else:
            self.output += "\t\t-" + property["name"] + "\n"

    pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(-1)

    sys.argv.pop(0)  # remove script name
    parsed_file = CppGraph()
    for header_file in sys.argv:
        print("Parsing file: " + header_file)
        try:
            parsed_file.loadFile(header_file)
        except CppHeaderParser.CppParseError as e:
            print(e)
            sys.exit(1)

    parsed_file.generateClassDiagram()
    print(parsed_file.output)

    pass
