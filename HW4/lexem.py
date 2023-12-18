#!/usr/bin/python3

class lexem():
    def __init__(self, token: str):
        self.TOKEN_LIST: list[str] = [*token]

        # create list of variables common to most functions
        self.NUMERIC: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        #self.NON_ZERO_NUMERIC: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.LOWERCASE_ALPHABETIC: list[str] = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        self.UPPERCASE_ALPHABETIC: list[str] = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.PLUS_OR_MINUS: list[int] = ["+", "-"]
        self.KEYWORDS: list[str] = ["WRITE", ".", "[", "]", "(", ")", ";"]
        #self.OPERATORS: list[str] = [":=", "~", "<", ">","=", "#", "+", "-", "&", "OR", "*", "/", "AND"]
        self.NON_STRING_LITERALS = [" ", '"']

    def _is_integer(self, INPUT_CHAR_LIST: list) -> bool:
        # auxillary variables
        start_index = 0

        if len(INPUT_CHAR_LIST) <= 0:
            return False

        # check if first element is + or -
        if INPUT_CHAR_LIST[0] in self.PLUS_OR_MINUS:
            start_index = 1  # loop over all numbers afterwards

        # check that sequence is non-empty after + or -
        if len(INPUT_CHAR_LIST) <= start_index:
            return False

        # check if any element in the list after the start isn't numeric
        for element in range(start_index, len(INPUT_CHAR_LIST)):
            if INPUT_CHAR_LIST[element] not in self.NUMERIC:
                return False
        # all elements in list after start are numeric
        return True

    # this is messy, but it works so don't touch it
    def _is_decimal(self, INPUT_CHAR_LIST: list) -> bool:
        # convert token list to list of substrings seperated by period
        INPUT_CHAR_STR: str = "".join(INPUT_CHAR_LIST)
        TOKEN_LIST_PARTS = INPUT_CHAR_STR.split(".")

        # make sure that there is only one period
        # and that it's not at the end (which would create two substrings)
        if (
            INPUT_CHAR_STR.count(".") != 1
            or len(TOKEN_LIST_PARTS) != 2
            or TOKEN_LIST_PARTS[1] == ""
        ):
            return False

        # check that first part is an integer
        if not self._is_integer(list(TOKEN_LIST_PARTS[0])):
            return False

        # check that second part is digits

        # convert 2nd part to list
        AFTER_PERIOD_LIST = list(TOKEN_LIST_PARTS[1])

        # check if any element in the list after the start isn't numeric
        for element in range(0, len(AFTER_PERIOD_LIST)):
            if AFTER_PERIOD_LIST[element] not in self.NUMERIC:
                return False

        # all elements in list after start are numeric, so return true
        return True
    
    def _is_keyword(self, INPUT_CHAR_LIST: list) -> bool:
        INPUT_CHAR_STRING = "".join(INPUT_CHAR_LIST)
        if INPUT_CHAR_STRING in self.KEYWORDS:
            return True
        else:
            return False

    def _is_string_literal(self, INPUT_CHAR_LIST: list) -> bool:
        # check that the string has quotes on both ends (must be at least 2 chars long to have to double quotes)
        if (
            len(INPUT_CHAR_LIST) <= 1
            or not INPUT_CHAR_LIST[0] == '"'
            or not INPUT_CHAR_LIST[-1] == '"'
        ):
            return False

        # check that the elements between the quotes don't have " or a space
        for element in range(1, len(INPUT_CHAR_LIST) - 1):
            if INPUT_CHAR_LIST[element] in self.NON_STRING_LITERALS:
                return False

        # all checks cleared, return true
        return True
        
    def _is_identifier(self, INPUT_CHAR_LIST: list) -> bool:
        # check that input is not keyword, hexadecimal or character literal
        if (
            self._is_keyword(INPUT_CHAR_LIST)
        ):
            return False

        # check if first character is a letter
        if (
            INPUT_CHAR_LIST[0] not in self.LOWERCASE_ALPHABETIC
            and INPUT_CHAR_LIST[0] not in self.UPPERCASE_ALPHABETIC
        ):
            return False

        # check if rest of characters are letters, numbers or underscore
        for element in range(1, len(INPUT_CHAR_LIST)):
            if (
                INPUT_CHAR_LIST[element] != "_"
                and INPUT_CHAR_LIST[element] not in self.LOWERCASE_ALPHABETIC
                and INPUT_CHAR_LIST[element] not in self.UPPERCASE_ALPHABETIC
                and INPUT_CHAR_LIST[element] not in self.NUMERIC
            ):
                return False

        # all checks passed, return true
        return True

    #one line checker functions
    @staticmethod
    def check_is_integer(TOKEN: str):
        lex = lexem(TOKEN)
        return lex._is_integer(lex.TOKEN_LIST)
    
    @staticmethod
    def check_is_decimal(TOKEN: str):
        lex = lexem(TOKEN)
        return lex._is_decimal(lex.TOKEN_LIST)
    @staticmethod
    def check_is_string_literal(TOKEN: str):
        lex = lexem(TOKEN)
        return lex._is_string_literal(lex.TOKEN_LIST)
    
    #the methods don't use the same structure, but I just want it done quickly
    @staticmethod
    def check_is_relation(TOKEN: str):
        RELATION_OPERATORS = ["<", ">", "=", "#"]
        if TOKEN in RELATION_OPERATORS: return True
        else: return False
    
    @staticmethod
    def check_is_add_operator(TOKEN: str):
        ADD_OPERATORS = ["+", "-", "OR", "&"]
        if TOKEN in ADD_OPERATORS: return True
        else: return False
    
    @staticmethod
    def check_is_mul_operator(TOKEN: str):
        MUL_OPERATORS = ["*", "/", "AND"]
        if TOKEN in MUL_OPERATORS: return True
        else: return False
    
    @staticmethod
    def check_is_identifier(TOKEN: str):
        lex = lexem(TOKEN)
        return lex._is_identifier(lex.TOKEN_LIST)