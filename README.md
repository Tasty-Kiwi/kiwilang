# KiwiLang

KiwiLang is a Lisp-like programming language written in Python.

Kiwilang is modular, allowing you write the syntax in JSON or KiwiLang's own, lisp-like syntax.

## Usage

```bash
python main.py examples/hello.json [-v] [-d] [-r] [-p]
```

```bash
python main.py examples/hello.klsp -c [-v] [-d] [-r] [-p]
```

- `-v` or `--verbose` - verbose output
- `-d` or `--debug` - debug output
- `-r` or `--repl` - run in interactive mode
- `-p` or `--performance` - enable performance metrics
- `-c` or `--compile` - use KiwiLang's compiler

## Syntax

### JSON
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

  ["for-each", "$i", ["range", 1, 10], ["print", "$i"]],
  
  ["defn", ":test", ["lambda", ["$x"], ["print", "$x"]]],
  [":test", "Hello, test function!"]
]
```

### KiwiLang
```scm
(defn :x 2)
(print :x)
(defn :my_list (list 1 2 3 4 5 6 7 8 9 10))
(print :my_list)

(defn :y 2)
(if (= :y 2)
    (print "y is 2")
    (print "y is not 2"))

(print (range 1 10))

(for-each $i (range 1 10) (print $i))

(defn :test (lambda ($x) (print $x)))
(:test "Hello, test function!")
```

## Features

- Variables
- Lambda functions
- Control flow
- Loops
- Lists