class Lexer:
    """
    The class that will perform lexical analysis, given the proper inputs.
    """
    def __init__(self, source_code):
        """
        Sets the class variables for the tables and source code.
        """
        self.lexical_table = self.__read_scanning_table()
        self.token_table = self.__read_token_table()
        self.source_code = source_code + " "
        self.keywords_list = self.__read_keyword_list()

    def perform_analysis(self):
        """
        The function that performs the lexical analysis.
        @return: A list of tokens representing the token stream.
        """
        self.current_token = 0
        tokens = []
        black_list = ["whitespace", "comment"]
        while self.current_token < len(self.source_code):
            token = self.__get_token()
            if token[1] in black_list:
                continue
            tokens.append(token)
        return tokens

    def __get_token(self):
        """
        Gets a single token from the source code.
        @return: A single token.
        """
        remembered_chars = ""
        current_state = 0
        image = ""
        remembered_state = 0
        while True:
            current_character = self.__get_character()
            action = self.__choose_action(current_state, current_character)
            if action == 0: # move
                if current_state in self.token_table.keys():
                    # could be in a final state
                    remembered_state = current_state
                    remembered_chars = ""
                remembered_chars += current_character
                current_state = self.lexical_table[(current_state, current_character)]
            elif action == 1: # recognize
                token = self.token_table[current_state]
                if not self.current_token == len(self.source_code):
                    self.current_token -= 1 # unread last read token
                break
            else: # error
                if remembered_state != 0:
                    token = self.token_table[remembered_state]
                    self.current_token -= len(remembered_chars)
                    image = image[:-len(remembered_chars)]
                    break
                return ("error at lexem number " + str(self.current_token) + \
                    ": | current lexem " + str(current_character) + " | " \
                    "| current state " + str(current_state) + " | remembered state "\
                     + str(remembered_state) , "error")
            image += current_character
        token_tuple = (self.__strip_special_markers_from_image(image), token)
        token_tuple = self.__keyword_check(token_tuple)
        return token_tuple

    def __strip_special_markers_from_image(self, image):
        return image.replace("0x20", " ")

    def __choose_action(self, current_state, current_character):
        """
        Chooses an action. If the current state and current character map to a
        valid state, the action is a move. If not and the token table is a goal
        state, then we recognize. If none of these conditions are true, we flag
        an error state.
        @param current_state is an integer representing the current state.
        @param current_character is a character representing the current lexem.
        @return: 0 move, 1 recognize, or 2 error.
        """
        if (current_state, current_character) in self.lexical_table.keys():
            move = self.lexical_table[(current_state, current_character)]
            if move != "": # valid move, so we select the move action
                return 0
        # we did not get a valid move, so we try to recognize
        if current_state in self.token_table.keys() and \
            not self.token_table[current_state] == 'error':
            return 1
        # otherwise, we are in an error state
        return 2

    def __get_character(self):
        """
        Get a single character from the source code.
        @return: A character or 0 if the source code is exhausted.
        """
        if self.current_token < len(self.source_code):
            char = self.source_code[self.current_token]
            self.current_token += 1
            return self.__white_space_to_char_literal(char)
        else:
            self.current_token += 1
            return 0
    
    def __keyword_check(self, token_tuple):
        """
        Checks a given token literal is a keyword, and changes the label as
        needed.
        @param token_tuple: A tuple of the literal token and token label.
        @return: The token tuple, modified if need be.
        """
        if token_tuple[1] == "identifier" and token_tuple[0] in self.keywords_list:
            return (token_tuple[0], "keyword")
        return token_tuple
    
    def __read_scanning_table(self):
        table_string = self.__read_file_as_string("scanning_table.csv")
        scanning_table = {}
        rows = table_string.split("\n")
        firstRow = rows[0].split(",")
        
        for i in range(1, len(rows)):
            columns = rows[i].split(",")
            state_idx = int(columns[0])
            for j in range(1, len(columns)):
                column_idx = firstRow[j]
                # Bootleg solutions to bootleg problems.
                if column_idx == "comma":
                    column_idx = ","
                next_state = columns[j]
                if next_state != "":
                    scanning_table[(state_idx, column_idx)] = int(next_state)
        return scanning_table

    def __read_token_table(self):
        table_string = self.__read_file_as_string("token_table.csv")
        token_table = {}
        rows = table_string.split("\n")
        for row in rows:
            (state, token) = row.split(",")
            token_table[int(state)] = token
        return token_table

    def __read_keyword_list(self):
        return self.__read_file_as_string("keywords.csv").split("\n")

    def __read_file_as_string(self, filename):
        """
        Reads the provided file as a string.
        @param filename: Name of the file to read.
        @return: A string of the files contents.
        """
        with open(filename, 'r') as file_pointer:
            return file_pointer.read()

    def __white_space_to_char_literal(self, state_idx):
        if state_idx == " ":
            state_idx = "0x20"
        elif state_idx == "\t":
            state_idx = "0x09"
        elif state_idx == "\n":
            state_idx = "0x0a"
        elif state_idx == "\r":
            state_idx = "0x0d"
        return state_idx
