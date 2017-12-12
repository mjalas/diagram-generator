
import sys

def get_prefix(line):
    if "public" in line:
        return "+"
    elif "protected" in line:
        return "#"
    elif "private" in line:
        return "-"

def remove_visibility_from_function(line):
    output = line.replace("public", "")
    output = output.replace("private", "")
    return output.replace("protected", "")

def filter_function(line):
    name = remove_visibility_from_function(line)
    name = name.replace("function", "")
    name = name.replace("{", "")
    name = name.replace("$", "")
    name = name.strip()
    return name

def parse_function(line):
    prefix = get_prefix(line)
    name = filter_function(line)
    return "\t" + prefix + name

def parse_file(filename):
    with open(filename) as src:
        in_class = False
        for line in src:
            #line = line.strip()
            if line == "":
                continue
            elif line.startswith("class"):
                in_class = True
                print(line)
            elif "function" in line and "__construct" not in line and "=" not in line:
                name = parse_function(line)
                print(name)
            elif line.startswith("}"):
                in_class = False
                print(line)

def main():
    print("Parsing input file")
    if len(sys.argv) >= 2:
        parse_file(sys.argv[1])

if __name__ == '__main__':
    main()
