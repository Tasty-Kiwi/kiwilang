import argparse
from interpreter import Interpreter

parser = argparse.ArgumentParser(description="JSONLang interpreter")
parser.add_argument("file", type=str)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-r", "--repl", action="store_true")
parser.add_argument("-p", "--performance", action="store_true")
parser.add_argument("-c", "--compile", action="store_true")

app_args = parser.parse_args()

interpreter = Interpreter(app_args.debug, app_args.verbose, app_args.performance, app_args.compile)

if app_args.repl:
    interpreter.repl()
else:
    interpreter.run_from_file(app_args.file)
