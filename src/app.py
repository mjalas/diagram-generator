import sys
import os
import glob
import pprint
import json

from php_parser import PHPParser
from class_diagram_generator import ClassDiagramGenerator


def handle_dir(dirname):
    data = {}
    for (dirpath, dirnames, filenames) in os.walk(dirname):
        for filename in filenames:
            if not filename.endswith('.php'):
                continue
            path = dirpath + os.sep + filename
            file_data = handle_file(path)
            if "namespace" not in file_data.keys():
                continue
            if file_data["namespace"] not in data.keys():
                data[file_data["namespace"]] = []
            data[file_data["namespace"]].append(file_data)
    return data


def handle_file(filename):
    parser = PHPParser()
    parser.parse_file(filename)
    return parser.data


def main():
    print("Parsing input file")
    if len(sys.argv) >= 3:
        path = sys.argv[1]
        if os.path.isdir(path):
            data = handle_dir(path)
        else:
            data = handle_file(path)
        if len(sys.argv) < 3:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(data)
        else:
            output_path = sys.argv[2]
            if output_path.endswith('.json'):
                content = json.dumps(data, indent=4, sort_keys=True)
                with open(output_path, 'w') as dest:
                    dest.write(content)
            elif output_path.endswith('.plantuml'):
                generator = ClassDiagramGenerator()
                generator.generate(data, output_path)


if __name__ == '__main__':
    main()
