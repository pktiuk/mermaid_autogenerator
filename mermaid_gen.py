#!/usr/bin/env python

import string
import CppHeaderParser
import sys
import string


output = "classDiagram\n"


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(-1)

    sys.argv.pop(0)  # remove script name

    for header_file in sys.argv:
        print("Parsing file: " + header_file)
        try:
            cppHeader = CppHeaderParser.CppHeader(header_file)
        except CppHeaderParser.CppParseError as e:
            print(e)
            sys.exit(1)
        for className, classFile in cppHeader.classes.items():
            print(className)
            output += "\tclass "+className+"{\n"

            for method in classFile["methods"]["public"]:
                output += "\t\t+" + method["name"] + "\n"
            for method in classFile["methods"]["private"]:
                output += "\t\t-" + method["name"] + "\n"

            for field in classFile["properties"]["private"]:
                output += "\t\t-" + field["name"] + "\n"
            for field in classFile["properties"]["public"]:
                output += "\t\t+" + field["name"] + "\n"

    pass
