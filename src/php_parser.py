import sys
import os
import re


class PHPParser(object):

    def __init__(self):
        self.data = {}

    def reset(self):
        self.data = {}

    def parse_file(self, filename):
        with open(filename) as src:
            for line in src:
                #line = line.strip()
                if line.strip() in os.linesep:
                    continue
                self.parse_line(line)

    def get_dependency(self, line):
        name = ""
        return name

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

    def parse_function_parameters(self, parameters):
        params = parameters.split(',')
        return params

    def get_function_data(self, line):
        data = {}
        pattern = r"(?P<visibility>(public|private|protected)+) function (?P<name>[a-zA-Z_]+)\((?P<parameters>(([a-zA-Z]+)?\s?[$][a-zA-Z0-9_]+\,?\s?)*)\)"
        m = re.search(pattern, line)
        if m:
            data["visibility"] = m.group('visibility')
            data["name"] = m.group('name')
            data["parameters"] = self.parse_function_parameters(m.group('parameters'))
        return data

    def parse_line(self, line):
        if self.is_namespace_line(line):
            self.data["namespace"] = self.get_namespace_data(line)
        elif self.is_use_line(line):
            if "dependencies" not in self.data.keys():
                self.data["dependencies"] = []
            dependency = self.get_dependency_data(line)
            if dependency:
                self.data["dependencies"].append(dependency)
        elif self.is_beginning_of_class_line(line):
            class_data = self.get_class_data(line)
            if class_data:
                self.data["name"] = class_data["name"]
        elif self.is_field_line(line):
            if "fields" not in self.data.keys():
                self.data["fields"] = []
            field = self.get_field_data(line)
            if field:
                self.data["fields"].append(field)
        elif self.is_function_line(line):
            if "methods" not in self.data.keys():
                self.data["methods"] = []
            function_data = self.get_function_data(line)
            if function_data:
                self.data["methods"].append(function_data)

    def get_namespace_data(self, line):
        namespace = line.replace("namespace", "")
        namespace = namespace.replace(";", "")
        namespace = namespace.replace("{", "")
        namespace = namespace.strip()
        return namespace

    def get_dependency_data(self, line):
        dependency = line.replace("use", "")
        dependency = dependency.replace(";", "")
        dependency = dependency.strip()
        return dependency

    def get_class_data(self, line):
        data = {}
        pattern = r"^class (?P<name>[a-zA-Z]*)\s*[a-zA-z]*\{"
        m = re.match(pattern, line)
        if m:
            data["name"] = m.group('name')
            return data
        return data

    def get_field_data(self, line):
        data = {}
        pattern = r"(?P<visibility>(public|private|protected)?) [$](?P<name>[a-zA-Z0-9_]+)[;]"
        m = re.search(pattern, line)
        if m:
            data["name"] = m.group('name')
            data["visibility"] = m.group('visibility')
        return data

    def get_class_name(self, line):
        name = line.replace("class", "")
        name = name.replace("{", "")
        name = name.strip()
        return name

    def is_namespace_line(self, line):
        return line.startswith("namespace")

    def is_use_line(self, line):
        return line.startswith("use")

    def is_beginning_of_class_line(self, line):
        return line.startswith("class")

    def is_end_of_class_line(self, line):
        return line.startswith("}")

    def is_field_line(self, line):
        return "private $" in line or "protected $" in line or "public $" in line

    def is_function_line(self, line):
        return "function" in line and "__construct" not in line and "=" not in line

