import os

# symbol table in form of {name: [type, kind, #]}
class_symbol_table = {}
subroutine_symbol_table = {}


def find_name_index(token):
    global class_symbol_table
    global subroutine_symbol_table
    if token not in class_symbol_table and token not in subroutine_symbol_table:
        print(f"No valid key in class symbol table for {token}")
        return
    else:
        if token in class_symbol_table:
            return f"push this {class_symbol_table[token][2] - 1}"
        else:
            return f"push local {subroutine_symbol_table[token][2] - 1}"


def reset_all_globals():
    global class_symbol_table
    global subroutine_symbol_table
    class_symbol_table = {}
    subroutine_symbol_table = {}


def count_subroutine_table_vars():
    cnt = 0
    for key, value in subroutine_symbol_table.items():
        if value[1] == "var":
            cnt += 1
    return cnt


def get_amount_kind(class_symbol_table, kind):
    count = 1
    for key, value in class_symbol_table.items():
        if value[1] == kind:
            count += 1
    return count


def in_symbol_table(symbol_table, name):
    for key in symbol_table:
        if key == name:
            return True
    return False


def add_identifier_to_subroutine_symbol_table(kind, type, name):
    amount_kind = get_amount_kind(subroutine_symbol_table, kind)
    if not in_symbol_table(class_symbol_table, name):
        subroutine_symbol_table[name] = [type, kind, amount_kind]


def add_identifier_to_class_symbol_table(kind, type, name):
    amount_kind = get_amount_kind(class_symbol_table, kind)
    if not in_symbol_table(class_symbol_table, name):
        class_symbol_table[name] = [type, kind, amount_kind]


def write_math_function(symbol, output_file):
    if symbol == "abs":
        ...
    elif symbol == "*":
        ...
    elif symbol == "/":
        ...
    else:
        ...


def increase_index(index):
    index[0] += 1


def next_token(list_tokenized, index):
    return list_tokenized[index[0]][1]


def next_lexical_element(list_tokenized, index):
    return list_tokenized[index[0]][0]


def count_field_var():
    count = 0
    for k, v in class_symbol_table.items():
        if v[1] == "field":
            count += 1
    return count


def determine_class_or_subroutine(list_tokenized, index):
    index_plus_one = [index[0] + 1]
    if next_token(list_tokenized, index_plus_one) == "(":
        return "subroutine"
    else:
        return "class"


def determine_category(list_tokenized, index, name):
    if name in class_symbol_table.keys():
        return class_symbol_table[name][1]
    elif name in subroutine_symbol_table.keys():
        return subroutine_symbol_table[name][1]
    else:
        return determine_class_or_subroutine(list_tokenized, index)


def determine_if_var(name):
    if len(class_symbol_table) > 0 and name in class_symbol_table:
        return "True"
    elif len(subroutine_symbol_table) > 0 and name in subroutine_symbol_table.keys():
        return "True"
    else:
        return "False"


def get_index(name, category):
    if category == "static" or category == "field":
        return str(class_symbol_table[name][2])
    elif category == "var" or category == "argument":
        return str(subroutine_symbol_table[name][2])
    else:
        return "-1"


def code_write(expression, output_file):
    output_file.write(expression + "\n")


def write_identifier_category(list_tokenized, index, output_file, level, state):
    name = list_tokenized[index[0]][1]
    category = determine_category(list_tokenized, index, name)
    var_of_four_kind = determine_if_var(name)
    category_index = get_index(name, category)
    expression = ""
    if category == "class" and state == "new":
        expression = "label (" + name + ")"
    elif category == "subroutine":
        expression = "label (" + subroutine_symbol_table["this"][0] + "." + name + ")"
    else:
        expression = "push " + category + " " + category_index
    code_write(expression, level, output_file)
    increase_index(index)


def write_current_xml_statement(list_tokenized, index, output_file, level):
    output_file.write(level * " " + "<" + list_tokenized[index[0]][0] + ">" + list_tokenized[index[0]][1] + "</" +
                      list_tokenized[index[0]][0] + ">\n")
    increase_index(index)


def write_amount_next_tokens(list_tokenized, index, output_file, current_level, amount):
    for x in range(0, amount):
        write_current_xml_statement(list_tokenized, index, output_file, current_level)


def compile_class(list_tokenized, index, output_file, level):
    increase_index(index)
    class_name = next_token(list_tokenized, index)
    increase_index(index)
    increase_index(index)
    while index[0] < len(list_tokenized) - 1:
        current_token = next_token(list_tokenized, index)
        if current_token == "static" or current_token == "field":
            compile_class_var_dec(list_tokenized, index, output_file, 2)
        elif current_token == "constructor" or current_token == "method" or current_token == "function":
            subroutine_symbol_table["this"] = [class_name, "argument", 1]
            compile_subroutine(list_tokenized, index, output_file, 2, )
            print(subroutine_symbol_table)
            subroutine_symbol_table.clear()
        else:
            print("There is an error somewhere... Should be class var or function etc.")
            return
    increase_index(index)
    print(class_symbol_table)


def compile_class_var_dec(list_tokenized, index, output_file, level):
    current_kind = next_token(list_tokenized, index)
    increase_index(index)
    current_type = next_token(list_tokenized, index)
    increase_index(index)
    while next_token(list_tokenized, index) != ";":
        if next_lexical_element(list_tokenized, index) == "identifier":
            add_identifier_to_class_symbol_table(current_kind, current_type, next_token(list_tokenized, index))
            increase_index(index)
        else:
            increase_index(index)
    increase_index(index)


def compile_subroutine_body(list_tokenized, index, output_file, level, subroutine_name, subroutine_type):
    current_level = level
    current_level += 2
    increase_index(index)
    compile_var_dec(list_tokenized, index, output_file, current_level)
    cnt = count_subroutine_table_vars()
    expression = f"function {subroutine_symbol_table['this'][0]}.{subroutine_name} {cnt}"
    code_write(expression, output_file)
    if subroutine_type == "constructor":
        space_required = str(count_field_var())
        code_write("push constant " + space_required, output_file)
        code_write("call Memory.alloc 1", output_file)
        code_write("pop pointer 0", output_file)
    elif subroutine_type == "method":
        code_write("push argument 0", output_file)
        code_write("pop pointer 0", output_file)
    compile_statements(list_tokenized, index, output_file, current_level, subroutine_name)
    increase_index(index)


def compile_subroutine(list_tokenized, index, output_file, level):
    current_level = level + 2
    subroutine_type = next_token(list_tokenized, index)
    increase_index(index)
    increase_index(index)
    subroutine_name = next_token(list_tokenized, index)
    increase_index(index)
    increase_index(index)
    compile_parameter_list(list_tokenized, index, output_file, current_level)
    increase_index(index)
    compile_subroutine_body(list_tokenized, index, output_file, current_level, subroutine_name, subroutine_type)


def compile_parameter_list(list_tokenized, index, output_file, level):
    current_level = level + 2
    if next_token(list_tokenized, index) == ")":  # if parameter list is empty
        return
    while next_token(list_tokenized, index) != ")":
        if next_token(list_tokenized, index) == ",":
            increase_index(index)
        else:
            type = next_token(list_tokenized, index)
            increase_index(index)
            name = next_token(list_tokenized, index)
            add_identifier_to_subroutine_symbol_table("argument", type, name)
            increase_index(index)


def compile_var_dec(list_tokenized, index, output_file, level):
    if list_tokenized[index[0]][1] != "var":  # if no variables
        return
    current_kind = next_token(list_tokenized, index)
    increase_index(index)
    current_type = next_token(list_tokenized, index)
    increase_index(index)
    while next_token(list_tokenized, index) != ";":
        if next_lexical_element(list_tokenized, index) == "identifier":
            add_identifier_to_subroutine_symbol_table(current_kind, current_type, next_token(list_tokenized, index))
            increase_index(index)
        else:
            increase_index(index)
    increase_index(index)
    if next_token(list_tokenized, index) == "var":
        compile_var_dec(list_tokenized, index, output_file, level)
cond_index = {
    "WHILE_INDEX": 0,
    "IF_INDEX": 0,
}

def determine_statement_type(list_tokenized, index, output_file, level, subroutine_name):
    global cond_index
    statement = list_tokenized[index[0]][1]
    sub_name = subroutine_symbol_table["this"][0] + "." + subroutine_name
    if statement == "let":
        compile_let(list_tokenized, index, output_file)
    elif statement == "if":
        label_name_start = sub_name + ".if.start." + str(cond_index["IF_INDEX"])
        label_name_end = sub_name + ".if.end." + str(cond_index["IF_INDEX"])
        cond_index["IF_INDEX"] += 1
        compile_if(list_tokenized, index, output_file, level, subroutine_name, label_name_start, label_name_end)
    elif statement == "while":
        print(cond_index["WHILE_INDEX"])
        label_name_start = sub_name + ".while.start." + str(cond_index["WHILE_INDEX"])
        label_name_end = sub_name + ".while.end." + str(cond_index["WHILE_INDEX"])
        cond_index["WHILE_INDEX"] += 1
        print(cond_index["WHILE_INDEX"])
        compile_while(list_tokenized, index, output_file, level, subroutine_name, label_name_start, label_name_end)
    elif statement == "do":
        compile_do(list_tokenized, index, output_file, level)
    else:
        compile_return(list_tokenized, index, output_file, level)


def compile_statements(list_tokenized, index, output_file, level, subroutine_name):
    current_level = level + 2
    # output_file.write(level * " " + "<statements>\n")
    while list_tokenized[index[0]][1] != "}":
        determine_statement_type(list_tokenized, index, output_file, current_level, subroutine_name)
    # output_file.write(level * " " + "</statements>\n")


def compile_do(list_tokenized, index, output_file, level):
    current_level = level + 2
    increase_index(index)  # do
    token = next_token(list_tokenized, index)
    global subroutine_symbol_table
    global class_symbol_table
    token_type = ""
    increase_index(index)
    if next_token(list_tokenized, index) == "(":
        code_write("push pointer 0", output_file)
        increase_index(index)
        amt = compile_expression_list(list_tokenized, index, output_file, current_level) + 1
        expression = f"call {subroutine_symbol_table['this'][0]}.{token} {amt}"
        code_write(expression, output_file)
        increase_index(index)  # )
    elif next_token(list_tokenized, index) == ".":
        name = token
        for x in range(0, 2):
            token += next_token(list_tokenized, index)
            increase_index(index)
        token_type = token
        increase_index(index)  # (
        amt = compile_expression_list(list_tokenized, index, output_file, current_level)
        if token[0].islower():
            token_type = subroutine_symbol_table[name][0] if name in subroutine_symbol_table else \
                class_symbol_table[name][0]
            token_type += token[token.find("."):]
            expression = find_name_index(name)
            code_write(expression, output_file)
            amt += 1
        expression = f"call {token_type} {amt}"
        code_write(expression, output_file)
        increase_index(index)  # )
    code_write("pop temp 0", output_file)
    increase_index(index)  # ;


def write_segments(push_or_pop, token, output_file):
    if token in class_symbol_table:
        if class_symbol_table[token][1] == "field":
            code_write(push_or_pop + " this " + str(class_symbol_table[token][2] - 1), output_file)
        else:
            code_write(push_or_pop + " static " + str(class_symbol_table[token][2] - 1), output_file)
    else:
        if subroutine_symbol_table[token][1] == "argument":
            code_write(push_or_pop + " argument " + str(subroutine_symbol_table[token][2] - 2), output_file)
        elif subroutine_symbol_table[token][1] == "var":
            code_write(push_or_pop + " local " + str(subroutine_symbol_table[token][2] - 1), output_file)
        else:
            print("Im in compile_let and im retareded")


def compile_let(list_tokenized, index, output_file):
    increase_index(index)  # let
    token = next_token(list_tokenized, index)
    increase_index(index)
    if next_token(list_tokenized, index) == "[":
        increase_index(index)  # [
        compile_expression(list_tokenized, index, output_file)
        write_segments("push", token, output_file)
        code_write("add", output_file)
        increase_index(index)  # ]
        increase_index(index)  # =
        compile_expression(list_tokenized, index, output_file)
        code_write("pop temp 0", output_file)
        code_write("pop pointer 1", output_file)
        code_write("push temp 0", output_file)
        code_write("pop that 0", output_file)
        increase_index(index)  # ;
    else:
        increase_index(index)  # =
        compile_expression(list_tokenized, index, output_file)
        increase_index(index)  # ;
        write_segments("pop", token, output_file)


def compile_while(list_tokenized, index, output_file, level, subroutine_name, label_start, label_end):
    current_level = level + 2
    code_write("label " + label_start, output_file)
    increase_index(index)  # while
    increase_index(index)  # (
    compile_expression(list_tokenized, index, output_file)
    code_write("not", output_file)
    code_write("if-goto " + label_end, output_file)
    increase_index(index)  # )
    increase_index(index)  # {
    compile_statements(list_tokenized, index, output_file, current_level, subroutine_name)
    code_write("goto " + label_start, output_file)
    increase_index(index)  # }
    code_write("label " + label_end, output_file)


def compile_return(list_tokenized, index, output_file, level):
    current_level = level + 2
    increase_index(index)  # return
    if next_token(list_tokenized, index) != ";":
        compile_expression(list_tokenized, index, output_file)
    else:
        code_write("push constant 0", output_file)
    code_write("return", output_file)
    increase_index(index)  # :


def compile_else(list_tokenized, index, output_file, current_level, subroutine_name):
    increase_index(index)
    increase_index(index)
    compile_statements(list_tokenized, index, output_file, current_level, subroutine_name)
    increase_index(index)


def compile_if(list_tokenized, index, output_file, level, subroutine_name, label_start, label_end):
    current_level = level + 2
    increase_index(index)  # if
    increase_index(index)  # (
    compile_expression(list_tokenized, index, output_file)
    code_write(f"if-goto {label_start}", output_file)
    code_write(f"goto {label_end}", output_file)
    code_write(f"label {label_start}", output_file)
    increase_index(index)
    increase_index(index)
    compile_statements(list_tokenized, index, output_file, current_level, subroutine_name)
    code_write(f"label {label_end}", output_file)
    increase_index(index)
    # code_write("neg", output_file)
    # code_write("if-goto " + label_start, output_file)
    # increase_index(index)  # )
    # increase_index(index)  # {
    # compile_statements(list_tokenized, index, output_file, current_level, subroutine_name)
    # code_write("goto " + label_end, output_file)
    # increase_index(index)
    # code_write("label " + label_start, output_file)
    if next_token(list_tokenized, index) == "else":
        compile_else(list_tokenized, index, output_file, current_level, subroutine_name)
    # code_write("label " + label_end, output_file)


def compile_expression(list_tokenized, index, output_file):
    compile_term(list_tokenized, index, output_file)


def compile_integer_constant(list_tokenized, index, output_file):
    code_write("push constant " + next_token(list_tokenized, index), output_file)
    increase_index(index)


def compile_string_constant(list_tokenized, index, output_file):
    token = next_token(list_tokenized, index)
    length = len(token)
    code_write(f"push constant {length}", output_file)
    code_write("call String.new 1", output_file)
    for letter in token:
        code_write(f"push constant {ord(letter)}", output_file)
        code_write("call String.appendChar 2", output_file)
    increase_index(index)


def compile_keyword(list_tokenized, index, output_file):
    token = next_token(list_tokenized, index)
    if token == "null":
        code_write("push constant 0", output_file)
    elif token == "false":
        code_write("push constant 0", output_file)
    elif token == "true":
        code_write("push constant 0", output_file)
        code_write("not", output_file)
    elif token == "this":
        code_write("push pointer 0", output_file)
    else:
        print("something is wrong in term -> keyword comp")
        print(f"this is the token = {token}")
    increase_index(index)


def compile_identifier(list_tokenized, index, output_file):
    global subroutine_symbol_table;
    global class_symbol_table
    # varName | varName '[' expression ']' | subroutineCall
    token = next_token(list_tokenized, index)
    increase_index(index)
    if next_token(list_tokenized, index) == "[":  # varName '[' expression ']'
        increase_index(index)  # [
        compile_expression(list_tokenized, index, output_file)
        write_segments("push", token, output_file)
        code_write("add", output_file)
        code_write("pop pointer 1", output_file)
        code_write("push that 0", output_file)
        increase_index(index)  # ]
    elif next_token(list_tokenized, index) == "(":  # subroutineName(expression)
        code_write("push pointer 0", output_file)
        expression = f"call {subroutine_symbol_table['this'][0]}.{token}"
        increase_index(index)  # (
        amt = compile_expression_list(list_tokenized, index, output_file, 0) + 1
        expression += f" {amt}"
        code_write(expression, output_file)  # das muss call f sii
        increase_index(index)  # )
    elif next_token(list_tokenized, index) == ".":  # (className|varName).subroutineName(expressionList)
        name = token
        token_type = ""
        for i in range(0, 2):
            token += next_token(list_tokenized, index)
            increase_index(index)
        token_type = token
        increase_index(index)  # (
        expression = "call " + token_type
        amt = compile_expression_list(list_tokenized, index, output_file, 0)
        if token[0].islower():
            token_type = subroutine_symbol_table[name][0] if name in subroutine_symbol_table else \
                class_symbol_table[name][0]
            token_type += token[token.find("."):]
            expression = find_name_index(name)
            code_write(expression, output_file)
            amt += 1
        expression = f"call {token_type} {amt}"
        code_write(expression, output_file)
        increase_index(index)  # )
    else:  # varName
        if token in subroutine_symbol_table:
            if subroutine_symbol_table[token][1] == "argument":
                code_write("push argument " + str(subroutine_symbol_table[token][2] - 2), output_file)
            elif subroutine_symbol_table[token][1] == "var":
                code_write("push local " + str(subroutine_symbol_table[token][2] - 1), output_file)
            else:
                print("im in compile_term and im retarded")
        elif token in class_symbol_table:
            if class_symbol_table[token][1] == "field":
                code_write("push this " + str(class_symbol_table[token][2] - 1), output_file)
            elif class_symbol_table[token][1] == "static":
                code_write("push static " + str(class_symbol_table[token][2] - 1), output_file)
            else:
                print("Im in compiel_term and im quite retarded")
        else:
            print("yeahadsjfas")
            write_amount_next_tokens(list_tokenized, index, output_file, 0, 1)


def compile_unaryOp_term(list_tokenized, index, output_file):
    op = next_token(list_tokenized, index)
    increase_index(index)
    compile_term(list_tokenized, index, output_file)
    if op == "-":
        code_write("neg", output_file)
    else:
        code_write("not", output_file)


def compile_operation_term(list_tokenized, index, output_file):
    op = next_token(list_tokenized, index)
    increase_index(index)
    compile_term(list_tokenized, index, output_file)
    if op == "+":
        code_write("add", output_file)
    elif op == "-":
        code_write("sub", output_file)
    elif op == "*":
        code_write("call Math.multiply 2", output_file)
    elif op == "/":
        code_write("call Math.divide 2", output_file)
    elif op == "&amp":
        code_write("and", output_file)
    elif op == "|":
        code_write("or", output_file)
    elif op == "&gt":
        code_write("gt", output_file)
    elif op == "&lt":
        code_write("lt", output_file)
    elif op == "=":
        code_write("eq", output_file)


operations = ["+", "-", "*", "/", "&amp", "|", "&lt", "&gt", "="]


def compile_term(list_tokenized, index, output_file):
    level = 0
    current_level = level + 2
    lexical_element = next_lexical_element(list_tokenized, index)
    if lexical_element == "integer_constant":
        compile_integer_constant(list_tokenized, index, output_file)
    elif lexical_element == "string_constant":
        compile_string_constant(list_tokenized, index, output_file)
    elif lexical_element == "keyword":  # null = constant 0, false = constant 0, true = constant -1(push 1 and neg)
        compile_keyword(list_tokenized, index, output_file)
    elif next_lexical_element(list_tokenized, index) == "identifier":
        # varName | varName '[' expression ']' | subroutineCall |
        compile_identifier(list_tokenized, index, output_file)
    elif next_token(list_tokenized, index) == "(":  # '(' expression ')'
        increase_index(index)
        compile_expression(list_tokenized, index, output_file)
        increase_index(index)
    else:  # | unaryOp term
        compile_unaryOp_term(list_tokenized, index, output_file)
    if next_token(list_tokenized, index) in operations:
        compile_operation_term(list_tokenized, index, output_file)


def compile_expression_list(list_tokenized, index, output_file, level):
    if next_token(list_tokenized, index) == ")":
        return 0
    current_level = level + 2
    count = 1
    compile_expression(list_tokenized, index, output_file)
    while next_token(list_tokenized, index) == ",":
        count += 1
        increase_index(index)
        compile_expression(list_tokenized, index, output_file)
    return count


def compile_tokens(list_tokenized, output_file):
    i = [0]
    if list_tokenized[i[0]][1] == "class":
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
    elif symbol == "&":
        list_tokenized.append(["symbol", "&amp"])
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
    path = input("Please enter the path to the folder of your files: ")
    if os.path.isdir(path):
        return path
    print("The given path does not exists.")
    return get_input()


def main():
    folder_path = get_input()
    jack_files = [file for file in os.listdir(folder_path) if file.endswith(".jack")]
    for file in jack_files:
        reset_all_globals()
        f = open(f"{folder_path}/{file}", "r")
        output_file = open(f"{folder_path}/{file[:file.find('.')]}.vm", "w")
        list_tokenized = tokenize_file(f)
        compile_tokens(list_tokenized, output_file)


if __name__ == '__main__':
    # print("Hello World!\n")
    # test = '	    let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");'
    # split = test.split()
    # list = []
    # tokenize_line(split, list)
    # print(list)
    main()
