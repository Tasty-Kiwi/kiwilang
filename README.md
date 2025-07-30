KiwiLang is a Lisp-like programming language written in Python.

Currently, it uses JSON as its syntax, but it will be changed to KiwiLang's own syntax in the future.

## Usage

```bash
python main.py test.json [-v] [-d]
```

- `-v` or `--verbose` - verbose output
- `-d` or `--debug` - debug output

## Syntax

```json
[
  ["print", "Hello, World!"],
  ["defn", ":x", 2],
  ["print", ":x"],
  ["defn", ":my_list", ["list", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
  ["print", ":my_list"],

  ["defn", ":y", 2],
  ["if", ["=", ":y", 2], 
    ["print", "y is 2"],
    ["print", "y is not 2"]
  ],

  ["print", ["range", 1, 10]],

  ["for", "$i", ["range", 1, 10], ["print", "$i"]],
  
  ["defn", ":test", ["lambda", ["$x"], ["print", "$x"]]],
  [":test", "Hello, test function!"]
]
```

## Features

- Variables
- Lambda functions
- Control flow
- Loops
- Lists