import re
from typing import Any, List


class Compiler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tokens = []
        self.current_token = 0

    def tokenize(self, source: str) -> List[str]:
        # Process each line to handle comments
        processed_lines = []
        for line in source.split("\n"):
            # Handle full line comments
            if line.strip().startswith("#") or line.strip().startswith(";"):
                processed_lines.append("")  # Add empty line to preserve line numbers
                continue

            # Handle inline comments
            comment_start = -1
            in_string = False
            for i, char in enumerate(line):
                if char == '"':
                    in_string = not in_string
                elif not in_string and (char == "#" or char == ";"):
                    comment_start = i
                    break

            if comment_start >= 0:
                line = line[:comment_start].rstrip()

            processed_lines.append(line)

        # Join the processed lines and tokenize
        source = "\n".join(processed_lines)

        # Tokenize the source code
        token_pattern = r'"[^"]*"|\:[\w\d_]+|\$[\w\d_]+|[()]|[^\s()"]+'
        tokens = re.findall(token_pattern, source)

        # Filter out empty strings and whitespace
        return [token for token in tokens if token.strip()]

    def parse_expression(self) -> Any:
        if self.current_token >= len(self.tokens):
            return None

        token = self.tokens[self.current_token]

        if token == "(":
            # Start of a list
            self.current_token += 1
            result = []
            while (
                self.current_token < len(self.tokens)
                and self.tokens[self.current_token] != ")"
            ):
                result.append(self.parse_expression())

            # Skip the closing ')'
            if (
                self.current_token < len(self.tokens)
                and self.tokens[self.current_token] == ")"
            ):
                self.current_token += 1

            return result
        elif token == ")":
            # This should be handled by the list parsing above
            raise SyntaxError("Unexpected ')'")
        else:
            # Atom
            self.current_token += 1

            # Convert to appropriate Python type
            if token.startswith('"') and token.endswith('"'):
                return token[1:-1]  # String without quotes
            elif token.startswith(":") or token.startswith("$"):
                return token  # Keep variables as is
            elif token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
                return int(token)
            elif token.replace(".", "", 1).isdigit() or (
                token.startswith("-") and token[1:].replace(".", "", 1).isdigit()
            ):
                return float(token)
            elif token.lower() == "true":
                return True
            elif token.lower() == "false":
                return False
            elif token.lower() == "nil" or token.lower() == "null":
                return None
            else:
                return token  # Keep symbols as is

    def compile_to_list(self) -> list:
        """Compile the source file to a Python dictionary."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            source = f.read()

        self.tokens = self.tokenize(source)
        self.current_token = 0

        # Parse all top-level expressions
        expressions = []
        while self.current_token < len(self.tokens):
            expr = self.parse_expression()
            if expr is not None:
                expressions.append(expr)

        return expressions

    @staticmethod
    def pretty_print_list(data: list) -> str:
        """Convert the list to a nicely formatted string."""
        import json

        return json.dumps(data, indent=2, ensure_ascii=False)
