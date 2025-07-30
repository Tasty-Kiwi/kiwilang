import json
import argparse
from typing import Any
import math
import os
import time

parser = argparse.ArgumentParser(description="JSONLang interpreter")
parser.add_argument("file", type=str)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-r", "--repl", action="store_true")
parser.add_argument("-p", "--performance", action="store_true")

app_args = parser.parse_args()
global_variables: dict[str, Any] = {}


def strip_variable_sigil(name: str) -> str:
    if name.startswith(":"):
        return name[1:]
    elif name.startswith("$"):
        return name[1:]
    else:
        return name


class Variable:
    is_local: bool
    is_mutable: bool
    value: Any

    def __init__(self, value: Any, is_local: bool = False, is_mutable: bool = False):
        self.value = value
        self.is_local = is_local
        self.is_mutable = is_mutable

    def __repr__(self):
        return f"({f'local' if self.is_local else 'global'} {f'mutable' if self.is_mutable else 'immutable'}): {self.value}"


class Interpreter:
    debug: bool
    verbose: bool
    performance_metrics: bool
    global_variables: dict[str, Variable]
    node_count: int

    def __init__(
        self,
        debug: bool = False,
        verbose: bool = False,
        performance_metrics: bool = False,
    ):
        self.debug = debug
        self.verbose = verbose
        self.performance_metrics = performance_metrics
        self.global_variables: dict[str, Variable] = {}
        self.node_count: int = 0

    def set_global_variable(self, name: str, value: Any):
        self.global_variables[name] = Variable(value)

    def get_global_variable(self, name: str) -> Any:
        return self.global_variables[name].value

    def run_from_file(self, file: str):
        with open(file, "r", encoding="utf8") as f:
            data = json.load(f)
            self.run(data)

    def run_from_string(self, string: str):
        data = json.loads(string)
        self.run(data)

    def run(self, data: list[Any]):
        if self.performance_metrics:
            start_time = time.perf_counter()
            self.node_count = 0

        for node in data:
            self._evaluate_node(node)

        if self.debug:
            print(
                f"\n======\nDebug information:\n\nGlobal variables: {self.global_variables}\n======"
            )
        if self.performance_metrics:
            print(
                f"\n======\nPerformance metrics:\n\nExecution time: {time.perf_counter() - start_time:.6f} s\nNodes evaluated: {self.node_count}\n======"
            )

    def repl(self):
        print("\x1b[36mKiwiLang interactive REPL\x1b[0m")
        while True:
            try:
                line = input(">>> ")
                match line:
                    case "":
                        continue
                    case "help" | "h":
                        print("Available commands:")
                        print("  exit (q) - exit the interpreter")
                        print("  help (h) - show this help")
                        print("  debug - toggle debug mode")
                        print("  verbose - toggle verbose mode")
                        print("  performance (perf) - toggle performance metrics")
                        print("  clear - clear the screen")
                    case "exit" | "q":
                        print("\x1b[36mGoodbye!\x1b[0m")
                        break
                    case "clear":
                        if os.name == "nt":
                            os.system("cls")
                        else:
                            os.system("clear")
                    case "debug":
                        self.debug = not self.debug
                        print(f"Debug mode: {self.debug}")
                    case "verbose":
                        self.verbose = not self.verbose
                        print(f"Verbose mode: {self.verbose}")
                    case "performance" | "perf":
                        self.performance_metrics = not self.performance_metrics
                        print(f"Performance metrics: {self.performance_metrics}")
                    case _:
                        if line.startswith(":"):
                            if strip_variable_sigil(line) in self.global_variables:
                                print(
                                    f"{strip_variable_sigil(line)}: {self.global_variables[strip_variable_sigil(line)]}"
                                )
                            else:
                                print(f"\x1b[31mVariable {line} is not defined\x1b[0m")
                        else:
                            try:
                                data = json.loads(line)
                                self.run([data])
                            except json.JSONDecodeError:
                                print("\x1b[31mInvalid JSON\x1b[0m")
            except KeyboardInterrupt:
                print("\n\x1b[36mGoodbye!\x1b[0m")
                break
            except Exception as e:
                print(f"\x1b[31mError: {e}\x1b[0m")

    def _evaluate_node(self, node: Any, local_vars: dict[str, Any] = {}) -> Any:
        if self.verbose:
            print(
                "Evaluating node: ",
                node,
                "Local variables: ",
                local_vars,
                "Global variables: ",
                self.global_variables,
            )

        if self.performance_metrics:
            self.node_count += 1

        match node:
            case ["+", left, right]:
                return self._evaluate_node(left, local_vars) + self._evaluate_node(
                    right, local_vars
                )
            case ["-", left, right]:
                return self._evaluate_node(left, local_vars) - self._evaluate_node(
                    right, local_vars
                )
            case ["*", left, right]:
                return self._evaluate_node(left, local_vars) * self._evaluate_node(
                    right, local_vars
                )
            case ["/", left, right]:
                return self._evaluate_node(left, local_vars) / self._evaluate_node(
                    right, local_vars
                )
            case ["//", left, right]:
                return self._evaluate_node(left, local_vars) // self._evaluate_node(
                    right, local_vars
                )
            case ["%", left, right]:
                return self._evaluate_node(left, local_vars) % self._evaluate_node(
                    right, local_vars
                )
            case ["=", left, right]:
                return self._evaluate_node(left, local_vars) == self._evaluate_node(
                    right, local_vars
                )
            case ["!=", left, right]:
                return self._evaluate_node(left, local_vars) != self._evaluate_node(
                    right, local_vars
                )
            case ["<", left, right]:
                return self._evaluate_node(left, local_vars) < self._evaluate_node(
                    right, local_vars
                )
            case [">", left, right]:
                return self._evaluate_node(left, local_vars) > self._evaluate_node(
                    right, local_vars
                )
            case ["<=", left, right]:
                return self._evaluate_node(left, local_vars) <= self._evaluate_node(
                    right, local_vars
                )
            case [">=", left, right]:
                return self._evaluate_node(left, local_vars) >= self._evaluate_node(
                    right, local_vars
                )
            case ["^", left, right]:
                return self._evaluate_node(left, local_vars) ** self._evaluate_node(
                    right, local_vars
                )
            case ["fact", value]:
                return math.factorial(self._evaluate_node(value, local_vars))
            case ["sqrt", value]:
                return math.sqrt(self._evaluate_node(value, local_vars))
            case ["print", value]:
                print(self._evaluate_node(value, local_vars))
                pass
            case ["defn", name, value] if name.startswith(":"):
                if strip_variable_sigil(name) in self.global_variables:
                    raise Exception(f"Variable {name} is already defined")
                self.global_variables[strip_variable_sigil(name)] = Variable(
                    self._evaluate_node(value, local_vars), is_local=False
                )
            case ["defn", name, value] if name.startswith("$"):
                if strip_variable_sigil(name) in local_vars:
                    raise Exception(f"Variable {name} is already defined")
                local_vars[strip_variable_sigil(name)] = Variable(
                    self._evaluate_node(value, local_vars), is_local=True
                )
            case ["defn-mutable", name, value] if name.startswith(":"):
                if strip_variable_sigil(name) in self.global_variables:
                    raise Exception(f"Variable {name} is already defined")
                self.global_variables[strip_variable_sigil(name)] = Variable(
                    self._evaluate_node(value, local_vars),
                    is_local=False,
                    is_mutable=True,
                )
            case ["defn-mutable", name, value] if name.startswith("$"):
                if strip_variable_sigil(name) in local_vars:
                    raise Exception(f"Variable {name} is already defined")
                local_vars[strip_variable_sigil(name)] = Variable(
                    self._evaluate_node(value, local_vars),
                    is_local=True,
                    is_mutable=True,
                )
            case ["mutate", name, value] if name.startswith(":"):
                if strip_variable_sigil(name) not in self.global_variables:
                    raise Exception(f"Variable {name} is not defined")
                if not self.global_variables[strip_variable_sigil(name)].is_mutable:
                    raise Exception(f"Variable {name} is not mutable")
                self.global_variables[strip_variable_sigil(name)].value = (
                    self._evaluate_node(value, local_vars)
                )
            case ["mutate", name, value] if name.startswith("$"):
                if strip_variable_sigil(name) not in local_vars:
                    raise Exception(f"Variable {name} is not defined")
                if not local_vars[strip_variable_sigil(name)].is_mutable:
                    raise Exception(f"Variable {name} is not mutable")
                local_vars[strip_variable_sigil(name)].value = self._evaluate_node(
                    value, local_vars
                )
            case ["for-each", name, iterable, body] if name.startswith("$"):
                for item in self._evaluate_node(iterable, local_vars):
                    local_vars[strip_variable_sigil(name)] = Variable(
                        item, is_local=True
                    )
                    self._evaluate_node(body, local_vars)
            # TODO: add $ char recognition
            case ["lambda", arguments, body]:
                arguments = [strip_variable_sigil(arg) for arg in arguments]
                return lambda *args: self._evaluate_node(
                    body,
                    local_vars
                    | dict(
                        zip(
                            arguments,
                            tuple(
                                Variable(arg, is_mutable=False, is_local=True)
                                for arg in args
                            ),
                        )
                    ),
                )
            case ["list", *items]:
                return tuple(self._evaluate_node(item, local_vars) for item in items)
            case ["if", condition, truthy]:
                if self._evaluate_node(condition, local_vars):
                    return self._evaluate_node(truthy, local_vars)
            case ["if", condition, truthy, falsy]:
                if self._evaluate_node(condition, local_vars):
                    return self._evaluate_node(truthy, local_vars)
                else:
                    return self._evaluate_node(falsy, local_vars)
            case ["range", start, end, step]:
                return tuple(
                    range(
                        self._evaluate_node(start, local_vars),
                        self._evaluate_node(end, local_vars),
                        self._evaluate_node(step, local_vars),
                    )
                )
            case ["range", start, end]:
                return tuple(
                    range(
                        self._evaluate_node(start, local_vars),
                        self._evaluate_node(end, local_vars),
                    )
                )
            case ["range", end]:
                return tuple(range(self._evaluate_node(end, local_vars)))
            case [function, *arguments]:
                func = self._evaluate_node(function, local_vars)
                if not callable(func):
                    raise Exception(f"Unable to call {function}")
                return func(*map(self._evaluate_node, arguments))
            case _:
                if isinstance(node, str) and (
                    node.startswith(":") or node.startswith("$")
                ):
                    if (
                        node.startswith("$")
                        and strip_variable_sigil(node) in local_vars
                    ):
                        return local_vars[strip_variable_sigil(node)].value
                    elif (
                        node.startswith(":")
                        and strip_variable_sigil(node) in self.global_variables
                    ):
                        return self.global_variables[strip_variable_sigil(node)].value
                    else:
                        raise Exception(f"Variable {node} is not defined")
                else:
                    return node


interpreter = Interpreter(app_args.debug, app_args.verbose, app_args.performance)

if app_args.repl:
    interpreter.repl()
else:
    interpreter.run_from_file(app_args.file)
