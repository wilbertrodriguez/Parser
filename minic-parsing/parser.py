class Parser:
    """
    This class parses the token stream outputted from the lexical analyzer 
    into a parse tree or produces errors if the program is malformed.
    """
    def __init__(self, token_stream, parse_table_file):
        """
        Class constructor takes the token stream output from the 
        lexical analyzer as input. Appends $ to the end of the stream.
        """
        self.token_stream = token_stream
        self.parser_table = self.__read_parse_table(parse_table_file)
        # Append the end of file symbol to the end.
        self.token_stream.append(("$", "$"))

    def __read_parse_table(self, parse_table_file):
        """
        Reads the parse table from a file.
        @param parse_table_file The file path for the parse table csv file.
        @return A dictionary/map (state, symbol) -> action/goto.
        """
        raise NotImplementedError()

    def __has_next_token(self):
        """
        @return True if the token stream is not empty.
        """
        return len(self.token_stream) != 0

    def __get_next_token(self):
        """
        Fetches and consumes the next token in the input.
        @return tuple (token, type)
        """
        if self.__has_next_token():
            to_return = self.token_stream[0]
            self.token_stream.pop(0)
            return to_return
        return None

    def parse(self):
        print(self.__get_next_token())
        raise NotImplementedError()
