import sys
import os


class PHPParser(object):

    def __init__(self):
        self.data = {}

    def parse_file(self, filename):
        with open(filename) as src:
            for line in src:
                #line = line.strip()
                if line.strip() in os.linesep:
                    continue
                self.parse_line(line)

    def get_visibility(self, line):
        if "public" in line:
            return "public"
        elif "protected" in line:
            return "protected"
        elif "private" in line:
            return "private"

    def remove_visibility_from_function(self, line):
        output = line.replace("public", "")
        output = output.replace("private", "")
        return output.replace("protected", "")

    def get_function_name(self, line):
        name = self.remove_visibility_from_function(line)
        name = name.replace("function", "")
        name = name.strip()
        params_start = name.index("(")
        name = name[:params_start]
        return name

    def get_function_parameters(self, line):
        params_start = line.index("(")
        params_end = line.index(")") + 1
        params = line[params_start:params_end]
        return params

    def parse_function(self, line):
        function_data = {}
        function_data["visibility"] = self.get_visibility(line)
        function_data["name"] = self.get_function_name(line)
        function_data["parameters"] = self.get_function_parameters(line)
        return function_data

    def parse_line(self, line):
        if self.is_beginning_of_class_line(line):
            class_name = self.get_class_name(line)
            self.data["class"] = class_name
        elif self.is_function_line(line):
            if "methods" not in self.data.keys():
                self.data["methods"] = []
            function_data = self.parse_function(line)
            self.data["methods"].append(function_data)

    def get_class_name(self, line):
        name = line.replace("class", "")
        name = name.replace("{", "")
        name = name.strip()
        return name

    def is_beginning_of_class_line(self, line):
        return line.startswith("class")

    def is_end_of_class_line(self, line):
        return line.startswith("}")

    def is_function_line(self, line):
        return "function" in line and "__construct" not in line and "=" not in line

