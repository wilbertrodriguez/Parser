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
        parsing_table = {}
        table = open(parse_table_file)
        try:
            temp = []
            for row in table:
                temp = row.split('\n')[0].split(",")
                temp.remove('')
                break
            for row in table:
                curr = row.split('\n')[0]
                state = ""
                front = 0
                for char in curr:
                    if char != ",":
                        state += char
                        front += 1
                    else:
                        break
                state = int(state)
                curr = curr[front:]
                col = -1
                goto = ""
                for c in curr:
                    if c == "," and not goto:
                        col += 1
                    elif c == "," and goto:
                        parsing_table[(state, temp[col])] = goto
                        goto = ""
                        col += 1
                    else:
                        goto += c
                if goto:
                    parsing_table[(state, temp[col])] = goto
            return parsing_table
        finally:
            table.close()

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
        """
        S->E=E S->id S'->S E->E+id E->id
        """
        stack = []
        stack.append("E")
        stack.append(0)
        isParsing = True
        step = 1
        step_stack = []
        temp_stack = "E0"
        temp_stack_stack = []
        temp_stack_stack.append(temp_stack)
        stream = ""
        stream_stack = []
        table_lookup = ""
        table_lookup_stack = []
        while isParsing:
            temp_stack = ""
            for char in self.token_stream:
                stream += char[0]
            stream_stack.append(stream)
            step_stack.append(step)
            qm = int(stack[-1])
            i = self.token_stream[0][1]
            tempi = self.token_stream[0][0]
            x = self.parser_table.get((qm, i))
            table_lookup = "[{},{}]={}".format(tempi,qm,x)
            table_lookup_stack.append(table_lookup)
            if not x or x == "ACCT":
                isParsing = False
            elif x[0] == "S":
                stack.append(self.__get_next_token()[1])
                stack.append(x[1:])
            elif x[0] == "R":
                if x[1] == "1":
                    stack = [stack.pop(0) for x in range(len(stack) - 6)]
                    qm = int(stack[-1])
                    stack.append("S")
                    stack.append(self.parser_table.get((qm, stack[-1])))
                elif x[1] == "2":
                    stack = [stack.pop(0) for x in range(len(stack) - 2)]
                    qm = int(stack[-1])
                    stack.append("S")
                    stack.append(self.parser_table.get((qm, stack[-1])))
                elif x[1] == "3":
                    stack = [stack.pop(0) for x in range(len(stack) - 6)]
                    qm = int(stack[-1])
                    stack.append("E")
                    stack.append(self.parser_table.get((qm, stack[-1])))
                elif x[1] == "4":
                    stack = [stack.pop(0) for x in range(len(stack) - 2)]
                    qm = int(stack[-1])
                    stack.append("E")
                    stack.append(self.parser_table.get((qm, stack[-1])))
            for tempx in stack:
                temp_stack += str(tempx)
            temp_stack_stack.append(temp_stack)
            step += 1
            stream = ""
            table_lookup = ""
        if x == "ACCT":
            print("STEP\tSTACK\t\tSTREAM\t\tTABLE LOOKUP")
            for i in range(len(step_stack)):
                print("{}\t{}\t\t{}\t\t{}".format(step_stack[i],temp_stack_stack[i],stream_stack[i],table_lookup_stack[i]))
            print("Parsing Accepted")
        else:
            print("Failed")
