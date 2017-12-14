# Diagram generator

The tool is still in very early development stages, which is why features are very limited.
The tool can currently be used for generating PlantUML code files from PHP files.
Generating diagram images is the main goal for the tool and will be available in the future.

It is also possible to generate a json file from the PHP code parsing result.
This feature is mostly used for debugging purposes, but might be useful for other purposes as well.


## Usage
Since the tool is still in early development,
the commands will change in the future.

To generate a plantuml code file run the follwing command:
```bash
python src/app.py <file or folder to parse> [output file path]
```

The output path should have an '.plantuml' extension for the diagram code to be generated.
If the output path is left out, then the program will print out the parsed data in the terminal.

The parsed data can also be generated into a json file by giving an output path with a '.json' extension.