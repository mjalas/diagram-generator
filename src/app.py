import sys
from php_parser import PHPParser


def main():
    print("Parsing input file")
    if len(sys.argv) >= 2:
        parser = PHPParser()
        parser.parse_file(sys.argv[1])
        print(str(parser.data))

if __name__ == '__main__':
    main()
