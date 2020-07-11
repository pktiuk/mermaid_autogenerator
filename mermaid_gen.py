#!/usr/bin/env python

import string
import CppHeaderParser
import sys


if __name__ == "__main__":
    if len(sys.argv) == 0:
        sys.exit(-1)
    
    for header_file in sys.argv:
        try:
            cppHeader = CppHeaderParser.CppHeader("SampleClass.h")
        except CppHeaderParser.CppParseError as e:
            print(e)
            sys.exit(1)

        print("Parsing file: "+ header_file)
        



    pass
