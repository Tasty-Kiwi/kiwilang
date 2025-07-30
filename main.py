import json
import argparse
from typing import Any

parser = argparse.ArgumentParser(description="JSONLang interpreter")
parser.add_argument("file", type=str)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")

app_args = parser.parse_args()
global_variables: dict[str, Any] = {}

def strip_variable_sigil(name: str) -> str:
    if name.startswith(":"):
        return name[1:]
    elif name.startswith("$"):
        return name[1:]
    else:
        return name

def evaluate_node(node: Any, local_vars: dict[str, Any] = {}) -> Any:
    global app_args
    global global_variables

    if app_args.verbose:
        print("Evaluating node: ", node, "Local variables: ", local_vars)

    if app_args.debug and local_vars:
        print("Local variables: ", local_vars)

    match node:
        case ["+", left, right]:
            return evaluate_node(left, local_vars) + evaluate_node(right, local_vars)
        case ["-", left, right]:
            return evaluate_node(left, local_vars) - evaluate_node(right, local_vars)
        case ["*", left, right]:
            return evaluate_node(left, local_vars) * evaluate_node(right, local_vars)
        case ["/", left, right]:
            return evaluate_node(left, local_vars) / evaluate_node(right, local_vars)
        case ["//", left, right]:
            return evaluate_node(left, local_vars) // evaluate_node(right, local_vars)
        case ["%", left, right]:
            return evaluate_node(left, local_vars) % evaluate_node(right, local_vars)
        case ["=", left, right]:
            return evaluate_node(left, local_vars) == evaluate_node(right, local_vars)
        case ["print", value]:
            print(evaluate_node(value, local_vars))
        case ["defn", name, value] if name.startswith(":"):
            global_variables[strip_variable_sigil(name)] = evaluate_node(value, local_vars)
        case ["defn", name, value] if name.startswith("$"):
            if strip_variable_sigil(name) in global_variables or strip_variable_sigil(name) in local_vars:
                raise Exception(f"Variable {name} is already defined")
            local_vars[strip_variable_sigil(name)] = evaluate_node(value, local_vars)
        case ["for", name, iterable, body] if name.startswith("$"):
            for item in evaluate_node(iterable, local_vars):
                local_vars[strip_variable_sigil(name)] = item
                evaluate_node(body, local_vars)
        # TODO: add $ char recognition
        case ["lambda", arguments, *bodies]:
            arguments = [strip_variable_sigil(arg) for arg in arguments]
            return lambda *args : [evaluate_node(body, local_vars | dict(zip(arguments, args))) for body in bodies]
        case ["list", *items]:
            return tuple(evaluate_node(item, local_vars) for item in items)
        case ["if", condition, truthy]:
            if evaluate_node(condition, local_vars):
                return evaluate_node(truthy, local_vars)
        case ["if", condition, truthy, falsy]:
            if evaluate_node(condition, local_vars):
                return evaluate_node(truthy, local_vars)
            else:
                return evaluate_node(falsy, local_vars)
        case ["range", start, end, step]:
            return tuple(range(evaluate_node(start, local_vars), evaluate_node(end, local_vars), evaluate_node(step, local_vars)))
        case ["range", start, end]:
            return tuple(range(evaluate_node(start, local_vars), evaluate_node(end, local_vars)))
        case ["range", end]:
            return tuple(range(evaluate_node(end, local_vars)))
        case [function, *arguments]:
            if global_variables.get(strip_variable_sigil(function)):
                return global_variables[strip_variable_sigil(function)](*arguments)
            else:
                raise Exception(f"Unable to call {function}")
        case _:
            if isinstance(node, str) and node.startswith(":"):
                if strip_variable_sigil(node) in global_variables:
                    return global_variables[strip_variable_sigil(node)]
                else:
                    raise Exception(f"Variable {node} is not defined")
            elif isinstance(node, str) and node.startswith("$"):
                if strip_variable_sigil(node) in local_vars:
                    return local_vars[strip_variable_sigil(node)]
                else:
                    raise Exception(f"Variable {node} is not defined")
            else:
                return node

def map_variable(name: str, value: Any):
    global_variables[name] = value

with open(app_args.file, "r") as file:
    data = json.load(file)
    for node in data:
        evaluate_node(node)
    if app_args.debug:
        print(f"\n======\nDebug information:\nGlobal variables: {global_variables}\n======")
