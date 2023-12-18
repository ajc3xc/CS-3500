#!/usr/bin/python3

try:
    import sys
    #import os
    from lexem import lexem

    #sys.setrecursionlimit(19000)

    def error_statement(expected: str, got: str):
        print("INVALID!")
        print("Error: " + expected + " expected, got "+got)
        sys.exit(1)

    class parser():
        def __init__(self, line: str):
            #convert the line to a list of strings
            #i.e. split each part up
            self.LINE_LIST:list[str] = line.split()

            if len(self.LINE_LIST) == 0: return

            #operator types
            self.RELATION = ["<", ">", "=", "#"]
            self.ADD_OPERATOR = ["+", "-", "OR", "&"]
            self.MUL_OPERATOR = ["*", "/", "AND"]

            #self.FAIL_CODE = None
            self.PARSE_TREE = {}

            self.check_if_statement_sequence()
            self.print_return_type()

        #prints the parse tree
        #used for debugging the parser
        def print_return_type(self):
            print("CORRECT")
        #    print(self.PARSE_TREE)

        
        #used for parsing a factor
        def _check_if_factor(self, SUB_PARSE_TREE_LIST: list[str]):
            if len(SUB_PARSE_TREE_LIST) < 1:
                error_statement("Factor", "End of Term")
            
            #more than one element in parse tree
            if len(SUB_PARSE_TREE_LIST) >= 2:
                # ~ Factor
                if SUB_PARSE_TREE_LIST[0] == "~":
                    SUB_PARSE_TREE_LIST.insert(1, {"Factor": SUB_PARSE_TREE_LIST[1:]})
                    del SUB_PARSE_TREE_LIST[2:]
                    self._check_if_factor(SUB_PARSE_TREE_LIST[1]["Factor"])
                # ( Expression )
                elif SUB_PARSE_TREE_LIST[0] == "(":
                    if SUB_PARSE_TREE_LIST[-1] == ")":
                        if len(SUB_PARSE_TREE_LIST) < 3:
                            error_statement("Expression", "Nothing")
                        else:
                            SUB_PARSE_TREE_LIST.insert(1, {"Expression": SUB_PARSE_TREE_LIST[1:-1]})
                            del SUB_PARSE_TREE_LIST[2:-1]
                            self._check_if_expression(SUB_PARSE_TREE_LIST[1]["Expression"])
                    else:
                        error_statement("\")\"", "\""+SUB_PARSE_TREE_LIST[-1]+"\"")
                #len >= 2, but not ~ Factor or ( Expression )
                else:
                    error_statement(" ~Factor or (Expression)", "End of Factor")
            #only one element in parse tree
            else:
                factor_type = None
                if lexem.check_is_integer(SUB_PARSE_TREE_LIST[0]):
                    factor_type = "Integer"
                elif lexem.check_is_decimal(SUB_PARSE_TREE_LIST[0]):
                    factor_type = "Decimal"
                elif lexem.check_is_string_literal(SUB_PARSE_TREE_LIST[0]):
                    factor_type = "String Literal"
                elif lexem.check_is_identifier(SUB_PARSE_TREE_LIST[0]):
                    factor_type = "Identifier"
                else:
                    error_statement("Factor", "\""+SUB_PARSE_TREE_LIST[0]+"\"")
                
                #assign as sub-dictionary
                SUB_PARSE_TREE_LIST[0] = {factor_type: SUB_PARSE_TREE_LIST[0]}

        #used for parsing a term
        def _check_if_term(self, SUB_PARSE_TREE_LIST: list[str]):
            if len(SUB_PARSE_TREE_LIST) == 1:
                SUB_PARSE_TREE_LIST[0] = {"Factor": SUB_PARSE_TREE_LIST[0:]}
                self._check_if_factor(SUB_PARSE_TREE_LIST[0]["Factor"])
                return True

            #position of the last factor before the mul operator
            current_factor_start = 0
            #range is set, so the range can't be modified in the for loop
            for i in range(1, len(SUB_PARSE_TREE_LIST)):
            #because range is immutable while executing, this must be done
                if i >= len(SUB_PARSE_TREE_LIST): break
            #i is mul operator
                if lexem.check_is_mul_operator(SUB_PARSE_TREE_LIST[i]):
                    #replace factor sublist with dictionary
                    SUB_PARSE_TREE_LIST[current_factor_start] = {"Factor": SUB_PARSE_TREE_LIST[current_factor_start:i]}
                    del SUB_PARSE_TREE_LIST[current_factor_start + 1:i]
                    self._check_if_factor(SUB_PARSE_TREE_LIST[current_factor_start]["Factor"])
                    #jump to current muloperator element
                    i = current_factor_start + 1
                    current_factor_start = i + 1
                    #nothing after muloperator
                    if current_factor_start >= len(SUB_PARSE_TREE_LIST): error_statement("Factor", "End of Term")
                    #element after muloperator is muloperator
                    elif lexem.check_is_mul_operator(SUB_PARSE_TREE_LIST[current_factor_start]): error_statement("Factor", "\""+SUB_PARSE_TREE_LIST[i]+"\"")

            #got through all the elements, now analyze the last factor grouping
            SUB_PARSE_TREE_LIST[current_factor_start] = {"Factor": SUB_PARSE_TREE_LIST[current_factor_start:]}
            #check if the length of the remaining sub parse tree list is more than one
            if current_factor_start < len(SUB_PARSE_TREE_LIST) - 1:
                del SUB_PARSE_TREE_LIST[current_factor_start + 1:]
            #the factor dict should now be the last element in the list
            self._check_if_factor(SUB_PARSE_TREE_LIST[-1]["Factor"])


        #used for parsing a simple expression
        def _check_if_simple_expression(self, SUB_PARSE_TREE_LIST: list[str]):
            if len(SUB_PARSE_TREE_LIST) == 1:
                SUB_PARSE_TREE_LIST[0] = {"Term": SUB_PARSE_TREE_LIST[0:]}
                self._check_if_term(SUB_PARSE_TREE_LIST[0]["Term"])
                return True

            #position of the last factor before the mul operator
            current_factor_start = 0
            #range is set, so the range can't be modified in the for loop
            for i in range(1, len(SUB_PARSE_TREE_LIST)):
            #because range is immutable while executing, this must be done
                if i >= len(SUB_PARSE_TREE_LIST): break
                #i is mul operator
                if lexem.check_is_add_operator(SUB_PARSE_TREE_LIST[i]):
                    #replace factor sublist with dictionary
                    SUB_PARSE_TREE_LIST[current_factor_start] = {"Term": SUB_PARSE_TREE_LIST[current_factor_start:i]}
                    del SUB_PARSE_TREE_LIST[current_factor_start + 1:i]
                    self._check_if_term(SUB_PARSE_TREE_LIST[current_factor_start]["Term"])
                    #jump to current muloperator element
                    i = current_factor_start + 1
                    current_factor_start = i + 1
                    #nothing after muloperator
                    if current_factor_start >= len(SUB_PARSE_TREE_LIST): error_statement("Factor", "End of Term")
                    #element after muloperator is muloperator
                    elif lexem.check_is_add_operator(SUB_PARSE_TREE_LIST[current_factor_start]): error_statement("Factor", "\""+SUB_PARSE_TREE_LIST[i]+"\"")

            #got through all the elements, now analyze the last factor grouping
            SUB_PARSE_TREE_LIST[current_factor_start] = {"Term": SUB_PARSE_TREE_LIST[current_factor_start:]}
            #check if the length of the remaining sub parse tree list is more than one
            if current_factor_start < len(SUB_PARSE_TREE_LIST) - 1:
                del SUB_PARSE_TREE_LIST[current_factor_start + 1:]
            #the factor dict should now be the last element in the list
            self._check_if_term(SUB_PARSE_TREE_LIST[-1]["Term"])       


        #expression level recursion
        def _check_if_expression(self, SUB_PARSE_TREE_LIST: list[str]):
            if len(SUB_PARSE_TREE_LIST) == 1:
                SUB_PARSE_TREE_LIST[0] = {"SimpleExpression": SUB_PARSE_TREE_LIST[0:]}
                self._check_if_simple_expression(SUB_PARSE_TREE_LIST[0]["SimpleExpression"])
                return True

            #there can only be one relation per expression
            for i in range(1, len(SUB_PARSE_TREE_LIST)):
                if lexem.check_is_relation(SUB_PARSE_TREE_LIST[i]):
                    #convert everything before the relation to a simple expression, then parse it
                    SUB_PARSE_TREE_LIST[0] = {"SimpleExpression": SUB_PARSE_TREE_LIST[0:i]}
                    #if i=1, then deleting [1:1] will not delete anything
                    del SUB_PARSE_TREE_LIST[1:i]
                    self._check_if_simple_expression(SUB_PARSE_TREE_LIST[0]["SimpleExpression"])
                    i = 2
                    #check if there is anything after the relation
                    if i >= len(SUB_PARSE_TREE_LIST): error_statement("SimpleExpression", "End of Expression")
                    #convert everything after the relation to a simple expression, parse it
                    SUB_PARSE_TREE_LIST[i] = {"SimpleExpression": SUB_PARSE_TREE_LIST[i:]}
                    if i+1 < len(SUB_PARSE_TREE_LIST):
                        del SUB_PARSE_TREE_LIST[i+1:]
                    self._check_if_simple_expression(SUB_PARSE_TREE_LIST[2]["SimpleExpression"])
                    return
            #relation wasn't found, so parse the entire expression as a simple expression
            SUB_PARSE_TREE_LIST[0] = {"SimpleExpression": SUB_PARSE_TREE_LIST[0:]}
            del SUB_PARSE_TREE_LIST[1:]
            self._check_if_simple_expression(SUB_PARSE_TREE_LIST[0]["SimpleExpression"])


        #### Expression, SimpleExpression, Term and Factor ####


        #### Designator and Selector ####

        #this is going to be very complicated to try and solve
        def _check_if_designator(self, SUB_PARSE_TREE_LIST: list[str]):
            #Identifier { Selector }
            if len(SUB_PARSE_TREE_LIST) < 1:
                error_statement("Identifier", "End of Assignment")
            elif not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[0]):
                print(SUB_PARSE_TREE_LIST[0])
                error_statement("Identifier", "\""+SUB_PARSE_TREE_LIST[0]+"\"")
            else:
                original_sub_parse_tree_len = len(SUB_PARSE_TREE_LIST)
                if original_sub_parse_tree_len <= 2:
                    SUB_PARSE_TREE_LIST[0] = {"Designator": [{"Identifier": SUB_PARSE_TREE_LIST[0]}]}
                    return []
                else:
                    SUB_PARSE_TREE_LIST.append({"Designator": [{"Identifier": SUB_PARSE_TREE_LIST[0]}, *SUB_PARSE_TREE_LIST[1:]]})
                    del SUB_PARSE_TREE_LIST[:original_sub_parse_tree_len]
                    SUB_PARSE_TREE_LIST[0]["Designator"][1:], RETURN_LIST = self._check_if_selector(SUB_PARSE_TREE_LIST[0]["Designator"][1:])
                    return RETURN_LIST

        #it would be smart if a list of   
        def _check_if_selector(self, SUB_PARSE_TREE_LIST: list[str]):
            if len(SUB_PARSE_TREE_LIST) < 1:
                return []
            
            REPLACEMENT_LIST = []
            i = 0
            for i in range(len(SUB_PARSE_TREE_LIST)-1):
                #the number at the top doesn't adjust dynamically
                #so I had to do this
                if i >= (len(SUB_PARSE_TREE_LIST)-1): break
                # . Identifier
                if SUB_PARSE_TREE_LIST[i] == ".":
                    if i + 1 >= len(SUB_PARSE_TREE_LIST):
                        error_statement("Identifier", "#nd of Selector")
                    elif not lexem.check_is_identifier(SUB_PARSE_TREE_LIST[i+1]):
                        error_statement("Identifier", "\""+SUB_PARSE_TREE_LIST[i+1]+"\"")
                    else:
                        SUB_PARSE_TREE_LIST.insert(i, {"Selector": [".", {"Identifier": SUB_PARSE_TREE_LIST[i+1]}]})
                        del SUB_PARSE_TREE_LIST[i+1:i+3]
                # [ Expression ]
                elif SUB_PARSE_TREE_LIST[i] == "[":
                    #print(SUB_PARSE_TREE_LIST[i:])
                    if i + 1 >= len(SUB_PARSE_TREE_LIST):
                        error_statement("\"]\"", "End of Selector")
                    for j in range(i+1, len(SUB_PARSE_TREE_LIST)):
                        #find first instance of ]
                        if SUB_PARSE_TREE_LIST[j] == "]":
                            #make sure there is an argument to check
                            #i.e. '[' ']' would be invalid, '[' 'x' ']' would be valid
                            if j - i == 1:
                                error_statement("Expression", "nothing")
                            SUB_PARSE_TREE_LIST.insert(i, {"Selector": ["[", {"Expression": SUB_PARSE_TREE_LIST[i+1: j]}, "]"]})
                            self._check_if_expression(SUB_PARSE_TREE_LIST[i]["Selector"][1]["Expression"])
                            #delete everything between [ ], including ]
                            del SUB_PARSE_TREE_LIST[i+1:j+2]
                            break
                    #couldn't find closing ]
                    else:
                        error_statement("\"]\"", "\""+SUB_PARSE_TREE_LIST[-1]+"\"")
                else:
                    #more SUB_PARSE_TREE[i:] to the replacement list, return it
                    REPLACEMENT_LIST.extend(SUB_PARSE_TREE_LIST[i:])
                    del SUB_PARSE_TREE_LIST[i:]
                    break
            
            return SUB_PARSE_TREE_LIST, REPLACEMENT_LIST

        #### Designator and Selector ####



        #### Assignment and WriteStatement ####

        def _check_if_assignment(self, SUB_PARSE_TREE_LIST: list[str]):
            SUB_PARSE_TREE_LIST_COPIED = [i for i in SUB_PARSE_TREE_LIST]
            SUB_PARSE_TREE_LIST.append({"Assignment": SUB_PARSE_TREE_LIST_COPIED})
            del SUB_PARSE_TREE_LIST[:-1]
            return_list = self._check_if_designator(SUB_PARSE_TREE_LIST[0]["Assignment"])
            SUB_PARSE_TREE_LIST[0]["Assignment"].extend(return_list)
            if len(SUB_PARSE_TREE_LIST[0]["Assignment"]) < 2:
                error_statement("\":=\"", "End of Assignment")
            elif SUB_PARSE_TREE_LIST[0]["Assignment"][1] != ":=":
                error_statement("\":=\"", "\""+SUB_PARSE_TREE_LIST[0]["Assignment"][1]+"\"")
            elif len(SUB_PARSE_TREE_LIST[0]["Assignment"]) < 3:
                error_statement("Identifier", "End of Assignment")
            SUB_PARSE_TREE_LIST[0]["Assignment"].insert(2, {"Expression": SUB_PARSE_TREE_LIST[0]["Assignment"][2:]})
            del SUB_PARSE_TREE_LIST[0]["Assignment"][3:]
            self._check_if_expression(SUB_PARSE_TREE_LIST[0]["Assignment"][2]["Expression"])
                

        def _check_if_write_statement(self, SUB_PARSE_TREE_LIST: list[str]):
            if len(SUB_PARSE_TREE_LIST) < 1:
                error_statement("WriteStatement", "End of Statement")
            # WRITE ( )
            elif SUB_PARSE_TREE_LIST[0] == "WRITE":
                if len(SUB_PARSE_TREE_LIST) < 2:
                    error_statement("\"(\"", "End of Statement")
                elif SUB_PARSE_TREE_LIST[1] != "(":
                    error_statement("\"(\"", "\""+SUB_PARSE_TREE_LIST[1]+"\"")
                elif len(SUB_PARSE_TREE_LIST) < 3:
                    error_statement("\")\"", "End of Statement")
                elif SUB_PARSE_TREE_LIST[-1] != ")":
                    error_statement("\")\"", "\""+SUB_PARSE_TREE_LIST[-1]+"\"")
                elif len(SUB_PARSE_TREE_LIST) < 4:
                    error_statement("Expression", "Nothing")
                else:
                    #replace the list with a write statement dict
                    SUB_PARSE_TREE_LIST[0] = {"WriteStatement": ["WRITE", "(", {"Expression": SUB_PARSE_TREE_LIST[2:-1]}, ")"]}
                    del SUB_PARSE_TREE_LIST[1:]
                    self._check_if_expression(SUB_PARSE_TREE_LIST[0]["WriteStatement"][2]["Expression"])
                    return True
            else:
                return False



        #### Statement and WriteStatement ####
                
        def _check_if_statement(self, SUB_PARSE_TREE: dict[list]):
            #print(SUB_PARSE_TREE)
            if self._check_if_write_statement(SUB_PARSE_TREE["Statement"]) or self._check_if_assignment(SUB_PARSE_TREE["Statement"]):
                return True


        #generates highest level of parse tree,
        #then parses to statement level
        def check_if_statement_sequence(self):
            self.PARSE_TREE["StatementSequence"] = []

            current_sublist_start_pos = 0
            for i in range(len(self.LINE_LIST)):
                # run statement parser on everything before ;
                if self.LINE_LIST[i] == ";":
                    self.PARSE_TREE["StatementSequence"].append({"Statement": self.LINE_LIST[current_sublist_start_pos:i]})
                    self.PARSE_TREE["StatementSequence"].append(';')
                    self._check_if_statement(self.PARSE_TREE["StatementSequence"][-2])
                    current_sublist_start_pos = i + 1

            #make sure that there is something after ; to run
            #or there is no ; in the statement
            if current_sublist_start_pos < len(self.LINE_LIST):
                self.PARSE_TREE["StatementSequence"].append({"Statement": self.LINE_LIST[current_sublist_start_pos:]})
                self._check_if_statement(self.PARSE_TREE["StatementSequence"][-1])


    def main():
        #the individual line is imported as a list of strings
        #it's just how the parser works
        line = sys.argv[1]

        parsed_line = parser(line)

    main()
except Exception as error:
    sys.exit(1)