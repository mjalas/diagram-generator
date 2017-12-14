

class ClassDiagramGenerator(object):

    def generate(self, data, output_path, single_class=False):
        output = self.__generate_output(data, single_class)
        with open(output_path, 'w') as dest:
            for line in output:
                dest.write(line + "\n")

    def __generate_output(self, data, single_class=False):
        output = ["@startuml", ""]
        dependencies_output = []
        errors = {"namespaces": 0, "classes": 0}
        for namespace, classes in data.items():
            if not namespace:
                errors["namespaces"] = errors["namespaces"] + 1
                continue
            output.append("namespace " + namespace + " {")
            for class_data in classes:
                if "name" not in class_data.keys():
                    errors["classes"] = errors["classes"] + 1
                    continue
                self.__add_class_content(class_data, output, dependencies_output)
                output.append("\t}")
                output.append("")

            for dependency in dependencies_output:
                output.append(dependency)
            output.append("}")
            output.append("")
        output.append("")
        output.append("' Empty namespaces: " + str(errors["namespaces"]))
        output.append("' Empty class names: " + str(errors["classes"]))
        output.append("@enduml")
        return output

    def __get_visibility_char(self, visibility):
        if visibility == "public":
            return "+"
        elif visibility == "protected":
            return "#"
        elif visibility == "private":
            return "-"
        return ""

    def __add_class_content(self, class_data, output, dependencies_output):
        output.append("\tclass " + class_data["name"] + "{")

        if "fields" in class_data.keys():
            self.__add_fields_content(class_data["fields"], output)
        output.append("\t\t---")

        if "methods" in class_data.keys():
            self.__add_methods_content(class_data["methods"], output)

        if "dependencies" in class_data.keys():
            self.__add_dependencies_content(class_data["name"], class_data["dependencies"], dependencies_output)

    def __add_fields_content(self, fields, output):
        for field in fields:
            line = self.__get_visibility_char(field["visibility"]) + field["name"]
            output.append("\t\t" + line)

    def __add_methods_content(self, methods, output):
        for method in methods:
            line = self.__get_visibility_char(method["visibility"]) + method["name"] + "("
            more_than_one = False
            param_line = ""
            for param in method["parameters"]:
                if more_than_one:
                    param_line = param_line + ", "
                parts = param.split(" ")
                if len(parts) == 2:
                    param_line = param_line + parts[1] + ":" + parts[0]
                else:
                    param_line = param_line + parts[0]
            line = line + param_line + ")"
            output.append("\t\t" + line)

    def __add_dependencies_content(self, class_name, dependencies, output):
        for dependency in dependencies:
            name = dependency.split("\\")[-1]
            if " as " in name:
                name = name.split(" as ")[0].strip()
            line = class_name + " --> " + name
            output.append("\t\t" + line)
        output.append("")
