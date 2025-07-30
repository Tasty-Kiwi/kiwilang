import json
import argparse
from typing import Any

parser = argparse.ArgumentParser(description="JSONLang interpreter")
parser.add_argument("file", type=str)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")

args = parser.parse_args()
global_variables: dict[str, Any] = {}

def evaluate_node(node: Any, local_vars: dict[str, Any] = {}) -> Any:
    global args
    global global_variables

    if args.verbose:
        print("Evaluating node: ", node, "Local variables: ", local_vars)

    if args.debug and local_vars:
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
            global_variables[name[1:]] = evaluate_node(value, local_vars)
        case ["defn", name, value] if name.startswith("$"):
            local_vars[name[1:]] = evaluate_node(value, local_vars)
        case ["for", name, iterable, body] if name.startswith("$"):
            for item in evaluate_node(iterable, local_vars):
                local_vars[name[1:]] = item
                evaluate_node(body, local_vars)
        # TODO: Fix this
        case ["lambda", arguments, body]:
            print("Lambda: ", arguments, body)
            print(**arguments)
            return lambda **arguments: evaluate_node(body, local_vars | arguments)
        case ["list", *items]:
            return [evaluate_node(item, local_vars) for item in items]
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
        # TODO: Fix this
        case [function, *arguments]:
            return evaluate_node(function, local_vars)(*[evaluate_node(arg, local_vars) for arg in arguments])
        case _:
            if isinstance(node, str) and node.startswith(":"):
                if node[1:] in global_variables:
                    return global_variables[node[1:]]
                else:
                    raise Exception(f"Variable {node[1:]} not found")
            elif isinstance(node, str) and node.startswith("$"):
                if node[1:] in local_vars:
                    return local_vars[node[1:]]
                else:
                    raise Exception(f"Local variable {node[1:]} not found")
            else:
                return node

def map_variable(name: str, value: Any):
    global_variables[name] = value

with open(args.file, "r") as file:
    data = json.load(file)
    map_variable("test", lambda x: x + 1)
    for node in data:
        evaluate_node(node)
    global_variables["add"](1, 2)
    if args.debug:
        print(f"\n======\nDebug information:\nGlobal variables: {global_variables}\n======")
