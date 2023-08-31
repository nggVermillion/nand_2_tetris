import os


def increase_index(index):
    index[0] += 1


def next_token(list_tokenized, index):
    return list_tokenized[index[0]][1]


def next_lexical_element(list_tokenized, index):
    return list_tokenized[index[0]][0]


def write_current_xml_statement(list_tokenized, index, output_file, level):
    output_file.write(level * " " + "<" + list_tokenized[index[0]][0] + ">" + list_tokenized[index[0]][1] + "</" +
                      list_tokenized[index[0]][0] + ">\n")
    increase_index(index)


def write_amount_next_tokens(list_tokenized, index, output_file, current_level, amount):
    for x in range(0, amount):
        write_current_xml_statement(list_tokenized, index, output_file, current_level)


def compile_class(list_tokenized, index, output_file, level):
    output_file.write("<class>\n")
    output_file.write("  <keyword> class <\keyword>\n")
    index[0] += 1
    output_file.write("  <identifier> " + list_tokenized[index[0]][1] + " <\identifier>\n")
    index[0] += 1
    output_file.write("  <symbol> { <\symbol>\n")
    index[0] += 1
    while index[0] < len(list_tokenized)-1:
        if list_tokenized[index[0]][1] == "static" or list_tokenized[index[0]][1] == "field":
            compile_class_var_dec(list_tokenized, index, output_file, 2)
        elif list_tokenized[index[0]][1] == "constructor" or list_tokenized[index[0]][1] == "method" or \
                list_tokenized[index[0]][1] == "function":
            compile_subroutine(list_tokenized, index, output_file, 2)
        else:
            print("There is an error somewhere... Should be class var or function etc.")
            return
    print(index)
    write_amount_next_tokens(list_tokenized, index, output_file, 2, 1)
    output_file.write("</class>\n")


def compile_class_var_dec(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<classVarDec>\n")
    while next_token(list_tokenized, index) != ";":
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    output_file.write(level * " " + "</classVarDec>\n")


def compile_subroutine_body(list_tokenized, index, output_file, level):
    current_level = level
    output_file.write(level * " " + "<subroutineBody>\n")
    current_level += 2
    output_file.write(current_level * " " + "<symbol> { <symbol>\n")
    increase_index(index)
    compile_var_dec(list_tokenized, index, output_file, current_level)
    compile_statements(list_tokenized, index, output_file, current_level)
    output_file.write(current_level * " " + "<symbol> } </symbol>\n")
    increase_index(index)
    output_file.write(level * " " + "</subroutineBody>\n")


def compile_subroutine(list_tokenized, index, output_file, level):
    output_file.write(level * " " + "<subroutineDec>\n")
    current_level = level + 2
    for i in range(0, 3):
        output_file.write("    <" + list_tokenized[index[0]][0] + "> " + list_tokenized[index[0]][1] + " </" +
                          list_tokenized[index[0]][0] + ">\n")
        index[0] += 1
    output_file.write(current_level * " " + "<symbol> ( <symbol>\n")
    index[0] += 1
    compile_parameter_list(list_tokenized, index, output_file, current_level)  # bis i = ")"
    output_file.write(current_level * " " + "<symbol> ) </symbol>\n")
    index[0] += 1
    compile_subroutine_body(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</subroutineDec>\n")

    return


def compile_parameter_list(list_tokenized, index, output_file, level):
    current_level = level + 2
    if list_tokenized[index[0] + 1][1] == ")":  # if parameter list is empty
        return
    output_file.write(level * " " + "<parameterList>\n")
    while list_tokenized[index[0]][1] != ")":
        output_file.write(
            current_level * " " + "<" + list_tokenized[index[0]][0] + "> " + list_tokenized[index[0]][1] + " </" +
            list_tokenized[index[0]][0] + ">\n")
        increase_index(index)
    output_file.write(level * " " + "</parameterList>\n")


def compile_var_dec(list_tokenized, index, output_file, level):
    if list_tokenized[index[0]][1] != "var":  # if no variables
        return
    current_level = level + 2
    i = 1
    while i == 1:
        output_file.write(level * " " + "<varDec>\n")
        while list_tokenized[index[0]][1] != ";":
            output_file.write(
                current_level * " " + "<" + list_tokenized[index[0]][0] + ">" + list_tokenized[index[0]][1] + "</" +
                list_tokenized[index[0]][0] + ">\n")
            increase_index(index)
        output_file.write(
            current_level * " " + "<" + list_tokenized[index[0]][0] + ">" + list_tokenized[index[0]][1] + "</" +
            list_tokenized[index[0]][0] + ">\n")
        output_file.write(level * " " + "</varDec>\n")
        increase_index(index)
        if next_token(list_tokenized, index) != "var":
            i = 0


def determine_statement_type(list_tokenized, index, output_file, level):
    statement = list_tokenized[index[0]][1]
    if statement == "let":
        compile_let(list_tokenized, index, output_file, level)
    elif statement == "if":
        compile_if(list_tokenized, index, output_file, level)
    elif statement == "while":
        compile_while(list_tokenized, index, output_file, level)
    elif statement == "do":
        compile_do(list_tokenized, index, output_file, level)
    else:
        compile_return(list_tokenized, index, output_file, level)


def compile_statements(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<statements>\n")
    while list_tokenized[index[0]][1] != "}":
        determine_statement_type(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</statements>\n")


def compile_do(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<doStatement>\n")
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    if next_token(list_tokenized, index) == "(":
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
        compile_expression_list(list_tokenized, index, output_file, current_level)
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    elif next_token(list_tokenized, index) == ".":
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 3)
        compile_expression_list(list_tokenized, index, output_file, current_level)
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    output_file.write(level * " " + "</doStatement>\n")


def compile_let(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<letStatement>\n")
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    if next_token(list_tokenized, index) == "[":
        write_current_xml_statement(list_tokenized, index, output_file, current_level)
        compile_expression(list_tokenized, index, output_file, current_level)
        write_current_xml_statement(list_tokenized, index, output_file, current_level)
    write_current_xml_statement(list_tokenized, index, output_file, current_level)
    compile_expression(list_tokenized, index, output_file, current_level)
    write_current_xml_statement(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</letStatement>\n")


def compile_while(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<whileStatement>\n")
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    compile_expression(list_tokenized, index, output_file, current_level)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    compile_statements(list_tokenized, index, output_file, current_level)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    output_file.write(level * " " + "</whileStatement>\n")


def compile_return(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<returnStatement>\n")
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    if next_token(list_tokenized, index) != ";":
        compile_expression(list_tokenized, index, output_file, current_level)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    output_file.write(level * " " + "</returnStatement>\n")


def compile_else(list_tokenized, index, output_file, current_level):
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    compile_statements(list_tokenized, index, output_file, current_level)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)


def compile_if(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<ifStatement>\n")
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    compile_expression(list_tokenized, index, output_file, current_level)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 2)
    compile_statements(list_tokenized, index, output_file, current_level)
    write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    if next_token(list_tokenized, index) == "else":
        compile_else(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</ifStatement>\n")


def compile_expression(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<expression>\n")
    compile_term(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</expression>\n")


operations = ["+", "-", "*", "/", "&", "|", "<", ">", "="]


def compile_term(list_tokenized, index, output_file, level):
    current_level = level + 2
    output_file.write(level * " " + "<term>\n")
    if next_lexical_element(list_tokenized, index) == "integer_constant" or next_lexical_element(list_tokenized, index) == "string_constant" or next_lexical_element(list_tokenized, index) == "keyword":
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    elif next_lexical_element(list_tokenized, index) == "identifier": # varName | varName '[' expression ']' | subroutineCall |
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
        if next_token(list_tokenized, index) == "[": # varName '[' expression ']'
            write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
            compile_expression(list_tokenized, index, output_file, current_level)
            write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
        elif next_token(list_tokenized, index) == "(":
            write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
            compile_expression_list(list_tokenized, index, output_file, current_level)
            write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
        elif next_token(list_tokenized, index) == ".":
            write_amount_next_tokens(list_tokenized, index, output_file, current_level, 3)
            compile_expression_list(list_tokenized, index, output_file, current_level)
            write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    elif next_token(list_tokenized, index) == "(": # '(' expression ')'
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
        compile_expression(list_tokenized, index, output_file, current_level)
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
    else: # | unaryOp term
        write_amount_next_tokens(list_tokenized, index, output_file, current_level, 1)
        compile_term(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</term>\n")
    if next_token(list_tokenized, index) in operations:
        write_amount_next_tokens(list_tokenized, index, output_file, level, 1)
        compile_term(list_tokenized, index, output_file, level)


def compile_expression_list(list_tokenized, index, output_file, level):
    if next_token(list_tokenized, index) == ")":
        return
    current_level = level + 2
    output_file.write(level * " " + "<expressionList>\n")
    compile_expression(list_tokenized, index, output_file, current_level)
    while next_token(list_tokenized, index) == ",":
        compile_expression(list_tokenized, index, output_file, current_level)
    output_file.write(level * " " + "</expressionList>\n")


def compile_tokens(list_tokenized):
    i = [0]
    if list_tokenized[i[0]][1] == "class":
        output_file = open(list_tokenized[i[0]][1] + ".xml", "w")
        compile_class(list_tokenized, i, output_file, 0)
    else:
        print("First element should be class\n")
        return


def write_string_to_output_file(string_constant, list_tokenized):
    list_tokenized.append(["string_constant", string_constant])


def write_symbol_to_output_file(symbol, list_tokenized):
    if symbol == "<":
        list_tokenized.append(["symbol", "&lt"])
    elif symbol == ">":
        list_tokenized.append(["symbol", "&gt"])
    elif symbol == "'":
        list_tokenized.append(["symbol", "&quote"])
    elif symbol == ">":
        list_tokenized.append(["&", "&amp"])
    else:
        list_tokenized.append(["symbol", symbol])


def determine_keyword_or_identifier(keyword_or_identifier_constant, list_tokenized):
    if keyword_or_identifier_constant == "class":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "constructor":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "function":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "method":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "field":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "static":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "var":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "int":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "char":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "boolean":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "void":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "true":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "false":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "null":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "this":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "let":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "do":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "if":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "else":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "while":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    elif keyword_or_identifier_constant == "return":
        list_tokenized.append(["keyword", keyword_or_identifier_constant])
    else:
        list_tokenized.append(["identifier", keyword_or_identifier_constant])


def write_int_to_output_file(integer_constant, list_tokenized):
    list_tokenized.append(["integer_constant", integer_constant])


def tokenize_line(line_split, list_tokenized):
    is_string = False
    is_keyword_or_identifier = False
    string_constant = ""
    keyword_or_identifier_constant = ""
    digit_constant = ""
    for char in line_split:
        for index, letter in enumerate(char):
            if letter == '"' and is_string == False:
                is_string = True
            elif is_string:
                if letter == '"':
                    is_string = False
                    if string_constant[-1] == " ":
                        string_constant = string_constant[0:-1]
                    write_string_to_output_file(string_constant, list_tokenized)
                    string_constant = ""
                else:
                    string_constant += letter
                    if index == (len(char) - 1):
                        string_constant += " "
            elif letter.isalpha() == False and letter.isdigit() == False and letter != "_":
                if letter == "/" and index < (len(char) - 1) and (char[index + 1] == "/" or char[index + 1] == "*"):
                    return
                else:
                    if is_keyword_or_identifier:
                        is_keyword_or_identifier = False
                        determine_keyword_or_identifier(keyword_or_identifier_constant, list_tokenized)
                        keyword_or_identifier_constant = ""
                    write_symbol_to_output_file(letter, list_tokenized)
            elif letter.isdigit() == True and is_keyword_or_identifier == False:
                digit_constant += letter
                if index < (len(char) - 1) and char[index + 1].isdigit() == True:
                    continue
                else:
                    write_int_to_output_file(digit_constant, list_tokenized)
                    digit_constant = ""
            else:
                is_keyword_or_identifier = True
                keyword_or_identifier_constant += letter
        if keyword_or_identifier_constant != "":
            determine_keyword_or_identifier(keyword_or_identifier_constant, list_tokenized)
            is_keyword_or_identifier = False
            keyword_or_identifier_constant = ""


def tokenize_file(file):
    tokenized = []
    for line in file:
        line_split = line.split()
        tokenize_line(line_split, tokenized)
    return tokenized


def get_input():
    path = input("Please enter the path of your file: ")
    if os.path.isfile(path):
        return open(path, "r")
    print("The given path does not exists.")
    return get_input()


def main():
    input_file = get_input()
    list_tokenized = tokenize_file(input_file)  # format [["token_type", token], [...], ...]
    for item in list_tokenized:
        print(item)
    compile_tokens(list_tokenized)


if __name__ == '__main__':
    # print("Hello World!\n")
    # test = '	    let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");'
    # split = test.split()
    # list = []
    # tokenize_line(split, list)
    # print(list)
    main()
