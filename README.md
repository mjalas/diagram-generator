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

## Data structure for code parsing result
The data parsed from code files are stored in specific data structure.
The tool can be extended to support other programming languages by implementing
a parser which returns the parsed data in the same data structure as below.
Types might be added in the future to make the data structure more convenient to use,
but it is not highly prioritized at the moment.


Below is an example of the data structure
outputted as json:
```json
{
    "<namespace>": [
        {
            "dependencies": [
                "dependency1",
                "dependency2"
            ],
            "fields": [
                {
                    "name": "field1",
                    "visibility": "private"
                },
                {
                    "name": "field2",
                    "visibility": "protected"
                },
                {
                    "name": "field3",
                    "visibility": "public"
                }
            ],
            "methods": [
                {
                    "name": "method1",
                    "parameters": [
                        "param1"
                    ],
                    "visibility": "public"
                },
                {
                    "name": "method2",
                    "parameters": [
                        "param1",
                        "param2"
                    ],
                    "visibility": "private"
                }
            ],
            "name": "Class1",
            "namespace": "<namespace>"
        },
        {
            "dependencies": [
            ],
            "fields": [
                {
                    "name": "field4",
                    "visibility": "public"
                },
                {
                    "name": "field5",
                    "visibility": "public"
                }
            ],
            "methods": [
                {
                    "name": "method3",
                    "parameters": [
                    ],
                    "visibility": "public"
                }
            ],
            "name": "Class2",
            "namespace": "<namespace>"
        }
    ]
}
```