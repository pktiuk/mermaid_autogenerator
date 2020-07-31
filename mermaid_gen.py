#!/usr/bin/env python3

import string
import CppHeaderParser
import sys
import string


class CppGraph:
    def __init__(self):
        # output string
        self.class_hierarhy_str = str()
        self.class_descriptions = str()
        # pre-defined signs and symbols
        self.PRIVATE_SIGN = '-'
        self.PUBLIC_SIGN = '+'

        # others
        self.all_of_classes = dict()
        self.set_of_classnames = set()

    def loadFile(self, header_file: str):
        self.cpp_header = CppHeaderParser.CppHeader(header_file)
        self.all_of_classes.update(self.cpp_header.classes)

    def generateClassDiagram(self):
        for className, classFile in self.all_of_classes.items():
            # only classes mentioned in files will be used for heneration of class hierarchy
            self.set_of_classnames.add(className)
            self.class_descriptions += "\tclass "+className+"{\n"

            for method in classFile["methods"]["public"]:
                self.loadMethod(method)
            for method in classFile["methods"]["private"]:
                self.loadMethod(method, False)

            for property in classFile["properties"]["public"]:
                self.loadProperty(property)
            for property in classFile["properties"]["private"]:
                self.loadProperty(property, False)

            self.class_descriptions += "\t}\n\n"

    def loadMethod(self, method, is_public: bool = True):
        if is_public:
            self.class_descriptions += "\t\t+" + method["name"]
        else:
            self.class_descriptions += "\t\t-" + method["name"]
        self.class_descriptions += "("
        for param in method["parameters"]:
            self.class_descriptions += param["name"] + ", "
        # remove excessive ", " if they were added
        if len(method["parameters"]) != 0:
            self.class_descriptions = self.class_descriptions[0:-2]

        self.class_descriptions += ")"

        if method["returns"].find("void") == -1:
            self.class_descriptions += ": " + method["returns"]
        self.class_descriptions += "\n"

    def loadProperty(self, property, is_public: bool = True):
        if is_public:
            self.class_descriptions += "\t\t+" + property["name"] + "\n"
        else:
            self.class_descriptions += "\t\t-" + property["name"] + "\n"

    def getOutput(self):
        return "classDiagram\n"+self.class_hierarhy_str+self.class_descriptions

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
    print(parsed_file.getOutput())

    pass
