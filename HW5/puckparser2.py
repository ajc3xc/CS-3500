import sys
#import os
from lexem import lexem

#sys.setrecursionlimit(19000)

def parser_empty_error(statement: str, end_type: str, use_quotes: bool = True):
    print("INVALID!")
    if use_quotes: print(f"\"{statement}\" expected, reached end of {end_type}.")
    else: print(f"{statement} expected, reached end of {end_type}.")
    sys.exit(1)

def parser_error_statement(expected: str, got: str, use_quotes_for_expected=False):
    print("INVALID!")
    if not use_quotes_for_expected: print(f"{expected} expected, got \"{got}\".")
    else: print(f"\"{expected}\" expected, got \"{got}\".")
    sys.exit(1)

def generic_error_statement(message: str):
    print("INVALID!")
    print(message)
    sys.exit(1)

def mistyped_identifier_error(identifier: str=None, type: str=None, mistyped: str=None):
    print("INVALID!")
    print(f"{type} \"{identifier}\" used as a {mistyped}.")
    sys.exit(1)

def undefined_function_error(function_call: str):
    print("INVALID!")
    print(f"Undefined function \"{function_call}\".")
    sys.exit(1)

class parser_and_symbol_table_generator():
    def __init__(self, file_lines: str):
        #convert the line to a list of strings
        #i.e. split each part up
        self.FILE_LINES_LIST:list[str] = file_lines.split()
        #print(self.FILE_LINES_LIST)
        if len(self.FILE_LINES_LIST) == 0:
            return

        #operator types
        self.RELATION = ["<", ">", "=", "#"]
        self.ADD_OPERATOR = ["+", "-", "OR", "&"]
        self.MUL_OPERATOR = ["*", "/", "AND", "DIV", "MOD"]

        #self.FAIL_CODE = None
        self.PARSE_TREE = {}
        self.SYMBOL_TABLE = {}

        self.check_if_declaration_sequence()
        self.print_return_type()

    #prints the parse tree
    #used for debugging the parser
    def print_return_type(self):
        print(self.PARSE_TREE)
        print("CORRECT")
        print(f"Symbol Table : size {len(self.SYMBOL_TABLE.keys())}")
        #key + spaces must be exactly 12 characters
        for key, value in self.SYMBOL_TABLE.items():
            print(f"{key.ljust(11, ' ')} {value}")
        #print(self.SYMBOL_TABLE)

#######################################################################
#Expression, SimpleExpression, Term, Factor

    def check_if_expression(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        #print(SUB_PARSE_TREE_LIST)
        if len(SUB_PARSE_TREE_LIST) < 1:
            parser_empty_error("Expression", "Expression", use_quotes_for_expected=False)
        
        #tracks how many layers of parentheses the expression is inside of
        #don't do anything to the expression if it is iterating through a parentheses
        parentheses_layers = 0

        for i in range(len(SUB_PARSE_TREE_LIST)):
            #cheap hack so it'll skip all the items in the list and move to the else statement
            #solves the ( x < 30 ) AND ( y = 20 ) problem
            if SUB_PARSE_TREE_LIST[i] == '(':
                parentheses_layers += 1
            elif SUB_PARSE_TREE_LIST[i] == ')' and parentheses_layers:
                parentheses_layers -= 1
            elif SUB_PARSE_TREE_LIST[i] in self.RELATION and not parentheses_layers:
                #print(i)
                #continue
                #nothing before or after relation operator
                if i == len(SUB_PARSE_TREE_LIST) - 1 or i == 0:
                    parser_empty_error("SimpleExpression", "Expression", use_quotes_for_expected=False)
                
                #check everything left of relation operator
                REPLACEMENT_DICT = {"SimpleExpression": SUB_PARSE_TREE_LIST[:i]}
                del SUB_PARSE_TREE_LIST[:i]
                SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
                self.check_if_simple_expression(SUB_PARSE_TREE_LIST[0]["SimpleExpression"])

                #check everything right of relation operator
                #simple expression packed into subdictionary, so everything right of relation starts at index 2
                REPLACEMENT_DICT = {"SimpleExpression": SUB_PARSE_TREE_LIST[2:]}
                del SUB_PARSE_TREE_LIST[2:]
                SUB_PARSE_TREE_LIST.append(REPLACEMENT_DICT)
                self.check_if_simple_expression(SUB_PARSE_TREE_LIST[2]["SimpleExpression"])
                break
        else:
            REPLACEMENT_DICT = {"SimpleExpression": SUB_PARSE_TREE_LIST[:]}
            SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
            del SUB_PARSE_TREE_LIST[1:]
            self.check_if_simple_expression(SUB_PARSE_TREE_LIST[0]["SimpleExpression"])


    def check_if_simple_expression(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("SimpleExpression", "Expression", use_quotes=False)

        #need to think about what happens when as term is just 1 line long
        elif len(SUB_PARSE_TREE_LIST) == 1:
            SUB_PARSE_TREE_LIST[0] = {"Term": SUB_PARSE_TREE_LIST[:]}
            self.check_if_term(SUB_PARSE_TREE_LIST[0]["Term"])
            return
        else:
            #this is going to be complicated because there could be multiple terms
            #effectively, increase i every iteration
            statement_start_sequence: int = 0 #find where to split up the statement sequence

            #tracks how many layers of parentheses the expression is inside of
            #don't do anything to the expression if it is iterating through a parentheses
            parentheses_layers = 0

            #prevents a loop or if statement from being broken up
            #basically creates a list-based stack
            i = 0

            while(1):
                #necessary because len function is only set once for range
                if i >= len(SUB_PARSE_TREE_LIST): break

    #           #cheap hack so it'll skip all the items in the list and move to the else statement
                #solves the ( x < 30 ) AND ( y = 20 ) problem
                if SUB_PARSE_TREE_LIST[i] == '(':
                    parentheses_layers += 1
                elif SUB_PARSE_TREE_LIST[i] == ')' and parentheses_layers:
                    parentheses_layers -= 1

                #split into multiple statements depending on where add_operator is
                elif SUB_PARSE_TREE_LIST[i] in self.ADD_OPERATOR and not parentheses_layers:
                    #check if there is anything before the add operator
                    if i == 0:
                        parser_error_statement("Term", SUB_PARSE_TREE_LIST[i], use_quotes_for_expected=False)

                    #condense statement strings into dictionary, check if sublist is a statement
                    REPLACEMENT_DICT:dict[list] = {"Term": SUB_PARSE_TREE_LIST[statement_start_sequence:i]}
                    del SUB_PARSE_TREE_LIST[statement_start_sequence:i]
                    SUB_PARSE_TREE_LIST.insert(statement_start_sequence, REPLACEMENT_DICT)
                    self.check_if_term(SUB_PARSE_TREE_LIST[statement_start_sequence]["Term"])
                    i = statement_start_sequence + 1 #because i increments by 1 at the end of each loop, i must be set where ; is now
                    statement_start_sequence = i+1 #the next statement will start after ;
                i+=1
            #check that there wasn't a ; at the end of a statement sequence
            if SUB_PARSE_TREE_LIST[-1] in self.ADD_OPERATOR:
                parser_error_statement("Term", SUB_PARSE_TREE_LIST[-1], use_quotes_for_expected=False)
            REPLACEMENT_DICT:dict[list] = {"Term": SUB_PARSE_TREE_LIST[statement_start_sequence:i]}
            del SUB_PARSE_TREE_LIST[statement_start_sequence:]
            SUB_PARSE_TREE_LIST.insert(statement_start_sequence, REPLACEMENT_DICT)
            self.check_if_term(SUB_PARSE_TREE_LIST[statement_start_sequence]["Term"])
    


    def check_if_term(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("Term", "SimpleExpression", use_quotes=False)

        #need to think about what happens when as term is just 1 line long
        elif len(SUB_PARSE_TREE_LIST) == 1:
            SUB_PARSE_TREE_LIST[0] = {"Factor": SUB_PARSE_TREE_LIST[:]}
            self.check_if_factor(SUB_PARSE_TREE_LIST[0]["Factor"])
            return
        else:
            #this is going to be complicated because there could be multiple terms
            #effectively, increase i every iteration
            statement_start_sequence: int = 0 #find where to split up the statement sequence

            #tracks how many layers of parentheses the expression is inside of
            #don't do anything to the expression if it is iterating through a parentheses
            parentheses_layers = 0

            #prevents a loop or if statement from being broken up
            #basically creates a list-based stack
            i = 0

            while(1):
                #necessary because len function is only set once for range
                if i >= len(SUB_PARSE_TREE_LIST): break

    #           #cheap hack so it'll skip all the items in the list and move to the else statement
                #solves the ( x < 30 ) AND ( y = 20 ) problem
                if SUB_PARSE_TREE_LIST[i] == '(':
                    parentheses_layers += 1
                elif SUB_PARSE_TREE_LIST[i] == ')' and parentheses_layers:
                    parentheses_layers -= 1

                #split into multiple statements depending on where add_operator is
                elif SUB_PARSE_TREE_LIST[i] in self.MUL_OPERATOR and not parentheses_layers:
                    #check if there is anything before the add operator
                    if i == 0:
                        parser_error_statement("Factor", SUB_PARSE_TREE_LIST[i], use_quotes_for_expected=False)

                    #condense statement strings into dictionary, check if sublist is a statement
                    REPLACEMENT_DICT:dict[list] = {"Factor": SUB_PARSE_TREE_LIST[statement_start_sequence:i]}
                    del SUB_PARSE_TREE_LIST[statement_start_sequence:i]
                    SUB_PARSE_TREE_LIST.insert(statement_start_sequence, REPLACEMENT_DICT)
                    self.check_if_factor(SUB_PARSE_TREE_LIST[statement_start_sequence]["Factor"])
                    i = statement_start_sequence + 1 #because i increments by 1 at the end of each loop, i must be set where ; is now
                    statement_start_sequence = i+1 #the next statement will start after ;
                i+=1
            #check that there wasn't a ; at the end of a statement sequence
            if SUB_PARSE_TREE_LIST[-1] in self.MUL_OPERATOR:
                parser_error_statement("Factor", SUB_PARSE_TREE_LIST[-1], use_quotes_for_expected=False)
            REPLACEMENT_DICT:dict[list] = {"Factor": SUB_PARSE_TREE_LIST[statement_start_sequence:i]}
            del SUB_PARSE_TREE_LIST[statement_start_sequence:]
            SUB_PARSE_TREE_LIST.insert(statement_start_sequence, REPLACEMENT_DICT)
            self.check_if_factor(SUB_PARSE_TREE_LIST[statement_start_sequence]["Factor"])


    def check_if_factor(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("Factor", "Term", use_quotes=False)

        #can only be integer, decimal, string or identifier
        elif len(SUB_PARSE_TREE_LIST) == 1:
            if lexem.check_is_integer(SUB_PARSE_TREE_LIST[0]):
                SUB_PARSE_TREE_LIST[0] = {"Integer": SUB_PARSE_TREE_LIST[0]}
            elif lexem.check_is_decimal(SUB_PARSE_TREE_LIST[0]):
                SUB_PARSE_TREE_LIST[0] = {"Decimal": SUB_PARSE_TREE_LIST[0]}
            elif lexem.check_is_string_literal(SUB_PARSE_TREE_LIST[0]):
                SUB_PARSE_TREE_LIST[0] = {"String": SUB_PARSE_TREE_LIST[0]}
            elif lexem.check_is_identifier(SUB_PARSE_TREE_LIST[0]):
                if SUB_PARSE_TREE_LIST[0] in self.SYMBOL_TABLE and self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[0]] != "variable":
                    mistyped_identifier_error(type="Function", identifier=SUB_PARSE_TREE_LIST[0], mistyped="variable")
                else:
                    SUB_PARSE_TREE_LIST[0] = {"Identifier": SUB_PARSE_TREE_LIST[0]}
            else:
                expected="Identifier"
                if SUB_PARSE_TREE_LIST[0] == "~": expected="~Factor"
                elif SUB_PARSE_TREE_LIST[0] == "(": expected="( Expression )"
                parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[0], use_quotes_for_expected=False)
        else:
            if SUB_PARSE_TREE_LIST[0] == "(":
                if SUB_PARSE_TREE_LIST[-1] != ")":
                    parser_error_statement(")", SUB_PARSE_TREE_LIST[-1])
                elif len(SUB_PARSE_TREE_LIST) == 2:
                    parser_empty_error("Expression", "Factor", use_quotes=False)
                else:
                    #replace expression sublist with expression subdict, check if expression
                    REPLACEMENT_DICT = {"Expression": SUB_PARSE_TREE_LIST[1:-1]}
                    del SUB_PARSE_TREE_LIST[1:-1]
                    SUB_PARSE_TREE_LIST.insert(1, REPLACEMENT_DICT)
                    self.check_if_expression(SUB_PARSE_TREE_LIST[1]["Expression"])
            elif SUB_PARSE_TREE_LIST[0] == "~":
                #replace expression sublist with expression subdict, check if expression
                REPLACEMENT_DICT = {"Factor": SUB_PARSE_TREE_LIST[1:]}
                del SUB_PARSE_TREE_LIST[1:]
                SUB_PARSE_TREE_LIST.insert(1, REPLACEMENT_DICT)
                self.check_if_factor(SUB_PARSE_TREE_LIST[1]["Factor"])
            #designator (must also have a selector otherwise it would only be 1 long)
            #thus, identifier . or identifier [
            elif SUB_PARSE_TREE_LIST[1] == "." or SUB_PARSE_TREE_LIST[1] == "[":
                REPLACEMENT_DICT = {"Designator": SUB_PARSE_TREE_LIST[:]}
                SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
                del SUB_PARSE_TREE_LIST[1:]
                self.check_if_designator(SUB_PARSE_TREE_LIST[0]["Designator"])
            #function call (last option)
            else:
                REPLACEMENT_DICT = {"FunctionCall": SUB_PARSE_TREE_LIST[:]}
                SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
                del SUB_PARSE_TREE_LIST[1:]
                self.check_if_function_call(SUB_PARSE_TREE_LIST[0]["FunctionCall"])




#######################################################################

#######################################################################
#designators, selectors, param sequences and function calls

    def check_if_designator(self, SUB_PARSE_TREE_LIST: list[str]):
        if len(SUB_PARSE_TREE_LIST) < 1:
            parser_empty_error("Designator", "Designator", use_quotes_for_expected=False)
        elif not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[0]):
            parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[0], use_quotes_for_expected=False)
        elif SUB_PARSE_TREE_LIST[0] in self.SYMBOL_TABLE and self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[0]] != "variable":
            mistyped_identifier_error(type="Function", identifier=SUB_PARSE_TREE_LIST[0], mistyped="variable")
        else:
            self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[0]] = "variable"
            SUB_PARSE_TREE_LIST[0] = {"Identifier": SUB_PARSE_TREE_LIST[0]}

            #designator has selector (thus length > 1)
            if len(SUB_PARSE_TREE_LIST) > 1:
                REPLACEMENT_DICT = {"Selector": SUB_PARSE_TREE_LIST[1:]}
                del SUB_PARSE_TREE_LIST[1:]
                SUB_PARSE_TREE_LIST.append(REPLACEMENT_DICT)
                self.check_if_selector(SUB_PARSE_TREE_LIST[1]["Selector"])
    
    
    #selector statements can repeated
    #since selector statements can be of variable length, it it better to repeat it here
    # can have var . var1 [ var2 ] . var3 as a valid designator
    def check_if_selector(self, SUB_PARSE_TREE_LIST: list[str]):
        #print(SUB_PARSE_TREE_LIST)
        if len(SUB_PARSE_TREE_LIST) < 2:
            parser_empty_error("Selector", "Designator", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] == ".":
            if not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[1]):
                parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[1], use_quotes_for_expected=False)
            elif SUB_PARSE_TREE_LIST[1] in self.SYMBOL_TABLE and self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[1]] != "variable":
                mistyped_identifier_error(type="Function", identifier=SUB_PARSE_TREE_LIST[0], mistyped="variable") #identifier is a function
            else:
                self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[1]] = "variable"
                SUB_PARSE_TREE_LIST[1] == {"Identifier": SUB_PARSE_TREE_LIST[1]}

                #there is something after . identifer
                if len(SUB_PARSE_TREE_LIST) >= 3:
                    REPLACEMENT_DICT = {"Selector": SUB_PARSE_TREE_LIST[2:]}
                    del SUB_PARSE_TREE_LIST[2:]
                    SUB_PARSE_TREE_LIST.append(REPLACEMENT_DICT)
                    self.check_if_selector(SUB_PARSE_TREE_LIST[2]["Selector"])
        elif SUB_PARSE_TREE_LIST[0] == "[":
            if len(SUB_PARSE_TREE_LIST) < 3:
                parser_empty_error("]", "Designator")
            #this gets done in case there is a[b[c[...]]]
            inner_left_bracket_counter = 0
            right_bracket_index = None
            for i in range(1, len(SUB_PARSE_TREE_LIST)):
                if SUB_PARSE_TREE_LIST[i] == "[":
                    inner_left_bracket_counter += 1
                elif SUB_PARSE_TREE_LIST[i] == "]":
                    if inner_left_bracket_counter <= 0:
                        right_bracket_index = i
                        break 
                    else: inner_left_bracket_counter -= 1
            else:
                parser_empty_error("]", "Designator")
            #right_bracket_index must not be none now, otherwise program would have failed
            # check expression in [ expression ]
            REPLACEMENT_DICT = {"Expression": SUB_PARSE_TREE_LIST[1:right_bracket_index]}
            del SUB_PARSE_TREE_LIST[1:right_bracket_index]
            SUB_PARSE_TREE_LIST.insert(1, REPLACEMENT_DICT)
            self.check_if_expression(SUB_PARSE_TREE_LIST[1]["Expression"])
            
            #check if there is anything after [ expression ]
            #expression should be a 1 index subdictionary now
            if len(SUB_PARSE_TREE_LIST) >= 4:
                REPLACEMENT_DICT = {"Selector": SUB_PARSE_TREE_LIST[3:]}
                del SUB_PARSE_TREE_LIST[3:]
                SUB_PARSE_TREE_LIST.insert(3, REPLACEMENT_DICT)
                self.check_if_selector(SUB_PARSE_TREE_LIST[3]["Selector"])
        else:
            #I'm going to assume [ is the last one checked
            parser_empty_error("[", "Designator")



        
    
    def check_if_param_sequence(self, SUB_PARSE_TREE_LIST: list[str]):
        if len(SUB_PARSE_TREE_LIST) < 1:
            parser_error_statement("ParamSequence", ")", use_quotes_for_expected=False)
        
        #iterate through param sequence, must be identifier , identifier , ... identifier
        current_item_must_be_comma = False

        for i in range(0, len(SUB_PARSE_TREE_LIST)):
            if current_item_must_be_comma:
                if SUB_PARSE_TREE_LIST[i] != ",":
                    parser_error_statement(",", SUB_PARSE_TREE_LIST[i])
                elif i == len(SUB_PARSE_TREE_LIST) - 1: # param sequence ended with comma
                    parser_empty_error("Identifier", "ParamSequence", use_quotes_for_expected=False)
                else:
                    current_item_must_be_comma = False #next item must be identifier
            else:
                if not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[i]):
                    parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[i], use_quotes_for_expected=False)
                elif SUB_PARSE_TREE_LIST[i] in self.SYMBOL_TABLE and self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[i]] != "variable":
                    mistyped_identifier_error(type="Function", identifier=SUB_PARSE_TREE_LIST[i], mistyped="variable")
                else:
                    self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[i]] = "variable"
                    SUB_PARSE_TREE_LIST[i] = {"Identifier": SUB_PARSE_TREE_LIST[i]}
                    current_item_must_be_comma = True #next item must be comma
                        
                    
    
    def check_if_function_call(self, SUB_PARSE_TREE_LIST: list[str]):
        if len(SUB_PARSE_TREE_LIST) < 3:
            parser_empty_error("FunctionCall", "Statement", use_quotes=False)
        elif not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[0]):
            parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[0], use_quotes_for_expected=False)
        elif SUB_PARSE_TREE_LIST[0] not in self.SYMBOL_TABLE:
            undefined_function_error(SUB_PARSE_TREE_LIST[0])
        elif self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[0]] != "function":
            mistyped_identifier_error(SUB_PARSE_TREE_LIST[0], "Variable", "function")
        elif SUB_PARSE_TREE_LIST[1] != "(":
            parser_error_statement("(", SUB_PARSE_TREE_LIST[1])
        elif SUB_PARSE_TREE_LIST[-1] != ")":
            parser_error_statement(")", SUB_PARSE_TREE_LIST[-1])
        else:
            if len(SUB_PARSE_TREE_LIST) >= 4:
                REPLACEMENT_DICT = {"ParamSequence": SUB_PARSE_TREE_LIST[2:-1]}
                del SUB_PARSE_TREE_LIST[2:-1]
                SUB_PARSE_TREE_LIST.insert(2, REPLACEMENT_DICT)
                self.check_if_param_sequence(SUB_PARSE_TREE_LIST[2]["ParamSequence"])

#######################################################################



#######################################################################
#assignment, writestatement, ifstatement, loopstatement

    def check_if_assignment(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        #print(SUB_PARSE_TREE_LIST)
        #sys.exit(1)
        if len(SUB_PARSE_TREE_LIST) < 3:
            parser_empty_error("Assignment", "Statement", use_quotes=False)

        #search for := in the sub parse tree list
        #if it isn't there or it is at the last line, fail
        for i in range(1, len(SUB_PARSE_TREE_LIST)):
            if SUB_PARSE_TREE_LIST[i] == ":=":
                #check if := is at the end of the list
                if i+1 >= len(SUB_PARSE_TREE_LIST):
                    parser_empty_error("Expression", "Assignment", use_quotes=False)
                else:
                    #run parser for designator part before :=
                    REPLACEMENT_DICT = {"Designator": SUB_PARSE_TREE_LIST[0:i]}
                    del SUB_PARSE_TREE_LIST[0:i]
                    SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
                    self.check_if_designator(SUB_PARSE_TREE_LIST[0]["Designator"])

                    #now that designator is a dictionary, do the same for the expression
                    #part after :=
                    REPLACEMENT_DICT = {"Expression": SUB_PARSE_TREE_LIST[2:]}
                    del SUB_PARSE_TREE_LIST[2:]
                    SUB_PARSE_TREE_LIST.insert(2, REPLACEMENT_DICT)
                    self.check_if_expression(SUB_PARSE_TREE_LIST[2]["Expression"])
                    break
        else:
            parser_empty_error(":=", "Assignment")

    def check_if_write_statement(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        if len(SUB_PARSE_TREE_LIST) < 4:
            parser_empty_error("WriteStatement", "Statement", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] != "WRITE":
            parser_error_statement("WRITE", SUB_PARSE_TREE_LIST[0])
        elif SUB_PARSE_TREE_LIST[1] != "(":
            parser_error_statement("(", SUB_PARSE_TREE_LIST[1])
        elif SUB_PARSE_TREE_LIST[-1] != ")":
            parser_error_statement(")", SUB_PARSE_TREE_LIST[-1])
        #replace list[2:-1] with dictionary
        REPLACEMENT_DICT = {"Expression": SUB_PARSE_TREE_LIST[2:-1]}
        del SUB_PARSE_TREE_LIST[2:-1]
        SUB_PARSE_TREE_LIST.insert(2, REPLACEMENT_DICT) 
        self.check_if_expression(SUB_PARSE_TREE_LIST[2]["Expression"]) 

    def check_if_if_statement(self, SUB_PARSE_TREE_LIST: list[str]):
        #print(SUB_PARSE_TREE_LIST)
        if len(SUB_PARSE_TREE_LIST) < 5:
            parser_empty_error("IfStatement", "Statement", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] != "IF":
            parser_error_statement("IF", SUB_PARSE_TREE_LIST[0])
        elif SUB_PARSE_TREE_LIST[-1] != "FI":
            parser_error_statement("FI", SUB_PARSE_TREE_LIST[-1])
        elif "THEN" not in SUB_PARSE_TREE_LIST[1:-1]:
            parser_error_statement("THEN", "FI")
        elif SUB_PARSE_TREE_LIST[1] == "THEN":
            parser_error_statement("Expression", "THEN", use_quotes_for_expected=False)
        elif SUB_PARSE_TREE_LIST[-2] == "THEN":
            parser_error_statement("StatementSequence", "THEN", use_quotes_for_expected=False)
        else:
            then_index = SUB_PARSE_TREE_LIST.index("THEN")

            #replace sublist [2:then_index] with Expression dictionary
            REPLACEMENT_DICT = {"Expression": SUB_PARSE_TREE_LIST[1:then_index]}
            del SUB_PARSE_TREE_LIST[1:then_index]
            SUB_PARSE_TREE_LIST.insert(1, REPLACEMENT_DICT)
            self.check_if_expression(SUB_PARSE_TREE_LIST[1]["Expression"])
            then_index = 2

            else_index = None
            nested_if_counter = 0
            for i in range( then_index+1, len(SUB_PARSE_TREE_LIST)-1):
                if SUB_PARSE_TREE_LIST[i] == "IF":
                    nested_if_counter += 1
                elif SUB_PARSE_TREE_LIST[i] == "FI":
                    nested_if_counter -= 1
                elif SUB_PARSE_TREE_LIST[i] == "ELSE" and nested_if_counter <= 0:
                    else_index = i
                    break

            #check if an else statement is in the part between THEN and FI
            #THEN is at position 2, FI is at position -1
            if else_index is not None:
                if else_index == then_index+1: #else index == 3
                    parser_error_statement("StatementSequence", "ELSE", use_quotes_for_expected=False)
                elif else_index+1 == len(SUB_PARSE_TREE_LIST) - 1: #check that THEN isn't before FI
                    parser_error_statement("StatementSequence", "ELSE", use_quotes_for_expected=False)
                else:
                    #set sublist between THEN and ELSE to dict
                    REPLACEMENT_DICT = {"StatementSequence": SUB_PARSE_TREE_LIST[then_index+1:else_index]}
                    del SUB_PARSE_TREE_LIST[then_index+1:else_index]
                    SUB_PARSE_TREE_LIST.insert(then_index+1, REPLACEMENT_DICT)
                    else_index = then_index+2
                    self.check_if_statement_sequence(SUB_PARSE_TREE_LIST[then_index+1]["StatementSequence"])

                    #set sublist between ELSE and FI to dict
                    #print(SUB_PARSE_TREE_LIST)
                    REPLACEMENT_DICT = {"StatementSequence": SUB_PARSE_TREE_LIST[else_index+1:-1]}
                    del SUB_PARSE_TREE_LIST[else_index+1:-1]
                    SUB_PARSE_TREE_LIST.insert(else_index+1, REPLACEMENT_DICT)
                    self.check_if_statement_sequence(SUB_PARSE_TREE_LIST[else_index+1]["StatementSequence"])
                    #print(SUB_PARSE_TREE_LIST)
            else:
                #set sublist between THEN and ELSE to dict
                REPLACEMENT_DICT = {"StatementSequence": SUB_PARSE_TREE_LIST[then_index+1:-1]}
                del SUB_PARSE_TREE_LIST[then_index+1:-1]
                SUB_PARSE_TREE_LIST.insert(then_index+1, REPLACEMENT_DICT)
                self.check_if_statement_sequence(SUB_PARSE_TREE_LIST[then_index+1]["StatementSequence"])
            #print(SUB_PARSE_TREE_LIST)

    def check_if_loop_statement(self, SUB_PARSE_TREE_LIST: list[str]):
        if len(SUB_PARSE_TREE_LIST) < 5:
            parser_empty_error("LoopStatement", "Statement", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] != "LOOP":
            parser_error_statement("LOOP", SUB_PARSE_TREE_LIST[0])
        elif SUB_PARSE_TREE_LIST[-1] != "POOL":
            parser_error_statement("POOL", SUB_PARSE_TREE_LIST[0])
        elif "DO" not in SUB_PARSE_TREE_LIST[1:-1]:
            parser_error_statement("DO", "POOL")
        elif SUB_PARSE_TREE_LIST[2] == "DO":
            parser_error_statement("Expression", "DO", use_quotes_for_expected=False)
        elif SUB_PARSE_TREE_LIST[-2] == "DO":
            parser_error_statement("StatementSequence", "DO", use_quotes_for_expected=False)
        else:
            #find index of DO, instead of using a for loop
            #just experimenting
            do_index = SUB_PARSE_TREE_LIST.index("DO")

            #check if part before do is an expression
            REPLACEMENT_DICT = {"Expression": SUB_PARSE_TREE_LIST[1:do_index]}
            del SUB_PARSE_TREE_LIST[1:do_index]
            SUB_PARSE_TREE_LIST.insert(1, REPLACEMENT_DICT)
            self.check_if_expression(SUB_PARSE_TREE_LIST[1]["Expression"])

            #check if part after do is a statement sequence
            #do_index should now be 2
            do_index = 2
            REPLACEMENT_DICT = {"StatementSequence": SUB_PARSE_TREE_LIST[do_index+1:-1]}
            del SUB_PARSE_TREE_LIST[do_index+1:-1]
            SUB_PARSE_TREE_LIST.insert(do_index+1, REPLACEMENT_DICT)
            self.check_if_statement_sequence(SUB_PARSE_TREE_LIST[do_index+1]["StatementSequence"])
        #print(SUB_PARSE_TREE_LIST)
        
        
        

#######################################################################

    def check_if_statement(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        #me and the boys on our way to avoid using return calls
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("Statement", "file", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] == "WRITE":
            REPLACEMENT_DICT = {"WriteStatement": SUB_PARSE_TREE_LIST[:]}
            SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
            del SUB_PARSE_TREE_LIST[1:]
            self.check_if_write_statement(SUB_PARSE_TREE_LIST[0]["WriteStatement"])
        elif SUB_PARSE_TREE_LIST[0] == "IF":
            REPLACEMENT_DICT = {"IfStatement": SUB_PARSE_TREE_LIST[:]}
            SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
            del SUB_PARSE_TREE_LIST[1:]
            self.check_if_if_statement(SUB_PARSE_TREE_LIST[0]["IfStatement"])
        elif SUB_PARSE_TREE_LIST[0] == "LOOP":
            REPLACEMENT_DICT = {"LoopStatement": SUB_PARSE_TREE_LIST[:]}
            SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
            del SUB_PARSE_TREE_LIST[1:]
            self.check_if_loop_statement(SUB_PARSE_TREE_LIST[0]["LoopStatement"])
        elif len(SUB_PARSE_TREE_LIST) >= 2 and SUB_PARSE_TREE_LIST[1] == "(":
            #using ( is cheap, but it should probably be foolproof
            REPLACEMENT_DICT = {"FunctionCall": SUB_PARSE_TREE_LIST[:]}
            SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
            del SUB_PARSE_TREE_LIST[1:]
            self.check_if_function_call(SUB_PARSE_TREE_LIST[0]["FunctionCall"])
        else:
            REPLACEMENT_DICT = {"Assignment": SUB_PARSE_TREE_LIST[:]}
            SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
            del SUB_PARSE_TREE_LIST[1:]
            self.check_if_assignment(SUB_PARSE_TREE_LIST[0]["Assignment"])
        


    def check_if_statement_sequence(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("StatementSequence", "file", use_quotes=False)

        #need to think about what happens when as statement is just 1 line long
        #useful in case the statement sequence is just ;, which would be wrong
        if len(SUB_PARSE_TREE_LIST) == 1:
            SUB_PARSE_TREE_LIST[0] = {"Statement": SUB_PARSE_TREE_LIST[:]}
            self.check_if_statement(SUB_PARSE_TREE_LIST[0]["Statement"])
            return

        #this is going to be complicated because there could be multiple ;s
        #effectively, increase i every iteration
        statement_start_sequence: int = 0 #find where to split up the statement sequence
        #prevents a loop or if statement from being broken up
        #basically creates a list-based stack
        statement_split_blocker: str = []
        i = 0
        while(1):
            #necessary because len function is only set once for range
            if i >= len(SUB_PARSE_TREE_LIST): break
            #these prevent if and loop statements from being split up into multiple statements
            #should protect against loop if ... fi statementsequence pool (edge case)
            #also double check that the lists aren't empty (yet another edge case)
            elif SUB_PARSE_TREE_LIST[i] == 'LOOP':
                statement_split_blocker.append('LOOP') #push loop to the stack
            elif SUB_PARSE_TREE_LIST[i] == 'POOL' and statement_split_blocker and statement_split_blocker[-1] == 'LOOP':
                statement_split_blocker.pop()
            elif SUB_PARSE_TREE_LIST[i] == 'IF':
                statement_split_blocker.append('IF')
            elif SUB_PARSE_TREE_LIST[i] == 'FI' and statement_split_blocker and statement_split_blocker[-1] == 'IF':
                statement_split_blocker.pop()
            #split into multiple statements depending on where ; is
            elif SUB_PARSE_TREE_LIST[i] == ";" and not statement_split_blocker:
                if i == 0:
                    parser_error_statement("Statement", SUB_PARSE_TREE_LIST[i], use_quotes_for_expected=False)
                #condense statement strings into dictionary, check if sublist is a statement
                REPLACEMENT_DICT:dict[list] = {"Statement": SUB_PARSE_TREE_LIST[statement_start_sequence:i]}
                del SUB_PARSE_TREE_LIST[statement_start_sequence:i]
                SUB_PARSE_TREE_LIST.insert(statement_start_sequence, REPLACEMENT_DICT)
                self.check_if_statement(SUB_PARSE_TREE_LIST[statement_start_sequence]["Statement"])
                i = statement_start_sequence + 1 #because i increments by 1 at the end of each loop, i must be set where ; is now
                statement_start_sequence = i+1 #the next statement will start after ;
            i+=1
        #check that there wasn't a ; at the end of a statement sequence
        if SUB_PARSE_TREE_LIST[-1] == ";":
            parser_error_statement("Statement", "END.", use_quotes_for_expected=False)
        REPLACEMENT_DICT:dict[list] = {"Statement": SUB_PARSE_TREE_LIST[statement_start_sequence:i]}
        del SUB_PARSE_TREE_LIST[statement_start_sequence:]
        SUB_PARSE_TREE_LIST.insert(statement_start_sequence, REPLACEMENT_DICT)
        self.check_if_statement(SUB_PARSE_TREE_LIST[statement_start_sequence]["Statement"])   

        
    
#######################################################################



    def check_if_return_statement(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        #ensure that statement is in the format of RETURN ( something )
        if len(SUB_PARSE_TREE_LIST) <= 3:
            parser_empty_error("Return statement", "file", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] != "RETURN":
            parser_error_statement("Return statement", SUB_PARSE_TREE_LIST[0])
        elif SUB_PARSE_TREE_LIST[1] != "(":
            parser_error_statement("(", SUB_PARSE_TREE_LIST[1], use_quotes_for_expected=True)
        elif SUB_PARSE_TREE_LIST[-1] != ")":
            parser_error_statement(")", SUB_PARSE_TREE_LIST[1], use_quotes_for_expected=True)
        #make sure multiple values aren't being returned
        elif len(SUB_PARSE_TREE_LIST) >= 5:
            generic_error_statement("Multiple values returned when only one is possible")
        elif not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[2]):
            parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[2])
        elif SUB_PARSE_TREE_LIST[2] in self.SYMBOL_TABLE and self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[2]] == "function":
            mistyped_identifier_error(SUB_PARSE_TREE_LIST[2], "Function", "variable")




    def check_if_function_body(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("END.", "file", use_quotes=True)
        
        if SUB_PARSE_TREE_LIST[0] == ";":
            #make sure there is nothing after the ;
            if len(SUB_PARSE_TREE_LIST) > 1:
                parser_error_statement("End of Function Body", "".join(SUB_PARSE_TREE_LIST[1:]))
            return True
        #END. may not be the end of the file
        #there may be ###### or something else after it
        #elif SUB_PARSE_TREE_LIST[-1] != "END.":
        #    parser_empty_error("END.", "file")
        elif len(SUB_PARSE_TREE_LIST) == 2:
            generic_error_statement("Statement expected, got nothing")
        else:
            #check if there is an "END." in the statement
            strings_after_end_statement = 0
            for i in range(1, len(SUB_PARSE_TREE_LIST)):
                if SUB_PARSE_TREE_LIST[i] == "END.":
                    strings_after_end_statement = len(SUB_PARSE_TREE_LIST) - (i + 1)
                    break
            else:
                parser_empty_error("END.", "file")
            
            for i in range(0, len(SUB_PARSE_TREE_LIST) - strings_after_end_statement - 1):
                #return statement was found
                if SUB_PARSE_TREE_LIST[i] == "RETURN":
                    #need to check if there is anything before the return statement
                    #if there isn't then don't pass an empty sequence
                    #to the lower function
                    if i != 0:
                        REPLACEMENT_DICT = {"StatementSequence": SUB_PARSE_TREE_LIST[0:i]}
                        del SUB_PARSE_TREE_LIST[0:i]
                        SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
                        self.check_if_statement_sequence(SUB_PARSE_TREE_LIST[0]["StatementSequence"])

                        #because the sublist [0:i] was condensed into the dictionary,
                        #the position of RETURN is changed
                        REPLACEMENT_DICT = {"ReturnStatement": SUB_PARSE_TREE_LIST[1:-(strings_after_end_statement+1)]}
                        del SUB_PARSE_TREE_LIST[1:-(strings_after_end_statement+1)]
                        SUB_PARSE_TREE_LIST.insert(1, REPLACEMENT_DICT)
                        self.check_if_return_statement(SUB_PARSE_TREE_LIST[1]["ReturnStatement"])
                    break
            #no return statement
            else:
                REPLACEMENT_DICT = {"StatementSequence": SUB_PARSE_TREE_LIST[0:-(strings_after_end_statement+1)]}
                del SUB_PARSE_TREE_LIST[0:-(strings_after_end_statement+1)]
                SUB_PARSE_TREE_LIST.insert(0, REPLACEMENT_DICT)
                self.check_if_statement_sequence(SUB_PARSE_TREE_LIST[0]["StatementSequence"])



    
    def check_if_function_declaration(self, SUB_PARSE_TREE_LIST: list[str]) -> None:
        #checking everything before getting function name
        if len(SUB_PARSE_TREE_LIST) <= 0:
            parser_empty_error("Function declaration", "file", use_quotes=False)
        elif SUB_PARSE_TREE_LIST[0] != "FUNCTION":
            parser_error_statement("Function declaration", SUB_PARSE_TREE_LIST[0])
        elif len(SUB_PARSE_TREE_LIST) == 1:
            parser_empty_error("Function name", "file")
        elif not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[1]):
            parser_error_statement("Identifier", SUB_PARSE_TREE_LIST[1])
        else:
            self.SYMBOL_TABLE[SUB_PARSE_TREE_LIST[1]] = "function"

        #getting everything afterwards
        if len(SUB_PARSE_TREE_LIST) <= 2:
            parser_empty_error("(", "file")
        elif SUB_PARSE_TREE_LIST[2] != "(":
            parser_error_statement("\"(\"", SUB_PARSE_TREE_LIST[2])
        elif len(SUB_PARSE_TREE_LIST) <= 3:
            parser_empty_error(")", "file")
        
        #check if ) exists in function declaration
        end_bracket_position = None
        for i in range(3, len(SUB_PARSE_TREE_LIST)):
            if SUB_PARSE_TREE_LIST[i] == ")":
                #param sequence isn't empty
                if i==3:
                    end_bracket_position = 4
                elif i != 3:
                    REPLACEMENT_DICT: dict[list] = {"ParamSequence": SUB_PARSE_TREE_LIST[3:i]}
                    del SUB_PARSE_TREE_LIST[3:i]
                    SUB_PARSE_TREE_LIST.insert(3, REPLACEMENT_DICT)
                    self.check_if_param_sequence(SUB_PARSE_TREE_LIST[3]["ParamSequence"])
                    end_bracket_position = 5
                break
        # ) wasn't in function declaration
        else:
            parser_error_statement("Function name", SUB_PARSE_TREE_LIST[-1])

        REPLACEMENT_DICT: dict[list] = {"FunctionBody": SUB_PARSE_TREE_LIST[end_bracket_position:]}
        del SUB_PARSE_TREE_LIST[end_bracket_position:]
        SUB_PARSE_TREE_LIST.append(REPLACEMENT_DICT)
        self.check_if_function_body(SUB_PARSE_TREE_LIST[-1]["FunctionBody"])       
            

        #print(SUB_PARSE_TREE_LIST)

    def check_if_declaration_sequence(self) -> None:
        if len(self.FILE_LINES_LIST) <= 0:
            parser_empty_error("Declaration Sequence", "file", use_quotes=False)
        self.PARSE_TREE["DeclarationSequence"] = []
        function_start = None
        function_end = None
        for i in range(len(self.FILE_LINES_LIST)):
            if self.FILE_LINES_LIST[i] == "FUNCTION":
                if function_start is None:
                    function_start = i
                    #print(function_start)
                    if function_start != 0: self.PARSE_TREE["DeclarationSequence"].extend(self.FILE_LINES_LIST[0:i])
                else:
                    function_end = i
                    self.PARSE_TREE["DeclarationSequence"].append({"FunctionDeclaration": self.FILE_LINES_LIST[function_start: function_end]})
                    self.check_if_function_declaration(self.PARSE_TREE["DeclarationSequence"][-1]["FunctionDeclaration"])
                    function_start = i
        self.PARSE_TREE["DeclarationSequence"].append({"FunctionDeclaration": self.FILE_LINES_LIST[function_start:]})
        self.check_if_function_declaration(self.PARSE_TREE["DeclarationSequence"][-1]["FunctionDeclaration"])


                


def main():
    #the individual line is imported as a list of strings
    #it's just how the parser works
    file_lines = sys.argv[1]

    parsed_file = parser_and_symbol_table_generator(file_lines)

main()