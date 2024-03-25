"""
Main entry point.
"""
import sys
from parser import Parser
from lexer import Lexer
from string import ascii_lowercase

def read_file_as_string(filename):
    """
    Reads the provided file as a string.
    @param filename: Name of the file to read.
    @return: A string of the files contents.
    """
    with open(filename, 'r') as file_pointer:
        return file_pointer.read()

# Ensure the right amount of arguments are provided.
if len(sys.argv) != 2:
    print("python3 main.py [sourceCode.*]")
    exit(0)

# Extract file names from the program arguments.
source_code_filename = sys.argv[1]

source_code = read_file_as_string(source_code_filename)

# Manually build the scanning table and token table.
lexical_table = {}

# Le'finite status machinem.
for c in ascii_lowercase:
    lexical_table[(0, c)] = 1
    lexical_table[(1, c)] = 1

lexical_table[(0, '=')] = 3
lexical_table[(0, '+')] = 2
lexical_table[(0, ' ')] = 4
lexical_table[(0, '\n')] = 4
lexical_table[(0, '\r')] = 4
lexical_table[(0, '\t')] = 4
lexical_table[(4, ' ')] = 4
lexical_table[(4, '\n')] = 4
lexical_table[(4, '\r')] = 4
lexical_table[(4, '\t')] = 4

# Table for token classes at accepting states.
token_table = {}
token_table[1] = "id"
token_table[2] = "+"
token_table[3] = "="
token_table[4] = "whitespace"

# Construct the lexer from the parsed file outputs from the parser.
lexer = Lexer(lexical_table, token_table, source_code)
# Perform the lexical analysis.
token_stream = lexer.perform_analysis()

# Perform the parse.
parser = Parser(token_stream, "parse_table.csv")
parser.parse()
