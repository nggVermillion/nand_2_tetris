import os.path

# 0–15 Sixteen virtual registers, usage described below
# 16–255 Static variables (of all the VM functions in the VM program)
# 256–2047 Stack
# 2048–16483 Heap (used to store objects and arrays)
# 16384–24575 Memory mapped I/O

# files
input_file = None
output_file = None


def get_input_file_path():
    return input("Enter the path of your input file:")


def get_output_file_path():
    return input("Enter the path of your output file:")


def open_input_file():
    path = get_input_file_path()
    if os.path.isfile(path):
        global input_file
        input_file = open(path, "r")
    else:
        print("The provided file doesn't exists or the path name is wrong")
        open_input_file()


def open_output_file():
    path = get_output_file_path()
    if os.path.isfile(path):
        global output_file
        output_file = open(path, "a")
    else:
        print("The provided file doesn't exists or the path name is wrong")
        open_output_file()


def close_files():
    final_characters = ["(FINAL_END)\n", "@FINAL_END\n", "0;JMP\n"]
    for commands in final_characters:
        output_file.write(commands)
    output_file.close()
    input_file.close()


arithmetic_commands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


# convert commands

# convert push and pop commands

def write_assembly_to_output_file(assembly_commands):
    for command in assembly_commands:
        print(command)
        global output_file
        output_file.write(command)


def convert_push_command(line):
    assembly_push_commands = [
        "@" + line[2] + "\n",  # index of push command: for example 3 of 'push argument 3'
        "D=A\n",
    ]
    segment = line[1]
    if segment == "argument":
        assembly_push_commands.append("@ARG\n")
    elif segment == "local":
        assembly_push_commands.append("@LCL\n")
    elif segment == "static":
        assembly_push_commands.append("@16\n")
    elif segment == "this":
        assembly_push_commands.append("@THIS\n")
    elif segment == "that":
        assembly_push_commands.append("@THAT\n")
    elif segment == "pointer":
        assembly_push_commands.append("@3\n")
    elif segment == "temp":
        assembly_push_commands.append("@5\n")
    elif segment == "constant":
        assembly_push_commands.append("@SP\n")
        assembly_push_commands.append("A=M\n")
        assembly_push_commands.append("M=D\n")
        assembly_push_commands.append("@SP\n")
        assembly_push_commands.append("M=M+1\n")
        write_assembly_to_output_file(assembly_push_commands)
        return
    else:
        print("Segment is wrong (doesnt exists)\n")
        return

    # increase A-reg by index and select RAM[A+index]
    if segment == "that" or segment == "this" or segment == "argument":
        assembly_push_commands.append("A=M+D\n")
    else:
        assembly_push_commands.append("A=D+A\n")
        if segment != "temp" and segment != "pointer" and segment != "static":
            assembly_push_commands.append("A=M\n") #warum bruch ich das? -> für push temp index bruchts es au nöd.
    assembly_push_commands.append("D=M\n")
    # push onto stack and increase stack[top] by one
    assembly_push_commands.append("@SP\n")
    assembly_push_commands.append("A=M\n")
    assembly_push_commands.append("M=D\n")
    assembly_push_commands.append("@SP\n")
    assembly_push_commands.append("M=M+1\n")
    write_assembly_to_output_file(assembly_push_commands)


pop_command_count = -1
def convert_pop_command(line):
    global pop_command_count
    pop_command_count += 1
    count = str(pop_command_count)
    assembly_pop_commands = [
        "@\n",  # pop top element from stack and decrease stack by one
        "D=M\n",
        "@" + line[2] + "\n",
        "D=D+A\n",
        "@EL\n",
        "M=D\n",
        "@SP\n",
        "A=M-1\n",
        "D=M\n",
        "@EL\n",
        "A=M\n",
        "M=D\n",
        "@SP\n",
        "M=M-1\n"
    ]

    segment = line[1]
    if segment == "argument":
        assembly_pop_commands[0] = "@ARG\n"
    elif segment == "local":
        assembly_pop_commands[0] = "@LCL\n"
    elif segment == "static":
        assembly_pop_commands[0] = "@16\n"
        assembly_pop_commands[1] = "D=A\n"
    elif segment == "this":
        assembly_pop_commands[0] = "@THIS\n"
    elif segment == "that":
        assembly_pop_commands[0] = "@THAT\n"
    elif segment == "pointer":
        assembly_pop_commands[0] = "@3\n"
        assembly_pop_commands[1] = "D=A\n"
    elif segment == "temp":
        assembly_pop_commands[0] = "@5\n"
        assembly_pop_commands[1] = "D=A\n"
    else:
        print("Segment is wrong (doesnt exists)\n")
        return

    write_assembly_to_output_file(assembly_pop_commands)


# convert arithemitic commands
end_count = -1
def convert_add(assembly_arithmetic_commands):
    # global end_count
    # end_count += 1
    # count = str(end_count)
    assembly_add_commands = [
        "@SP\n"
        "A=M-1\n",
        "D=M\n",  # stack[SP-1] (stack[top])
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",  # stack[SP-2]
        "D=D+M\n",  # stack[SP-1] + stack[SP-2] + set RAM[SP] so that SP represents the top of the stack again
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=D\n",
        "D =A+1\n",
        "@SP\n",
        "M=D\n"
        #"(END)\n"
    ]

    for command in assembly_add_commands:
        assembly_arithmetic_commands.append(command)


def convert_sub(assembly_arithmetic_commands):
    assembly_sub_commands = [
        "@SP\n"
        "A=M-1\n",
        "D=M\n",  # stack[SP-1] (stack[top])
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",  # stack[SP-2]
        "D=M-D\n",  # stack[SP-1] + stack[SP-2] + set RAM[SP] so that SP represents the top of the stack again
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=D\n",
        "D =A+1\n",
        "@SP\n",
        "M=D\n"
        #"(END)\n"
    ]

    for command in assembly_sub_commands:
        assembly_arithmetic_commands.append(command)


def convert_neg(assembly_arithmetic_commands):
    assembly_neg_commands = [
        # "@SP\n",
        # "D=M\n",
        # "@256\n",
        # "D=D-A\n",
        # "@END\n",
        # "D;JLE\n",
        "@SP\n",
        "A=M-1\n",
        "D=0\n",
        "D=D-M\n",
        "@SP\n",
        "A=M-1\n",
        "M=D\n"
        #"(END)\n"
    ]

    for command in assembly_neg_commands:
        assembly_arithmetic_commands.append(command)

equal_count = -1
def convert_eq(assembly_arithmetic_commands):
    global equal_count
    equal_count += 1
    count = str(equal_count)
    global end_count
    end_count += 1
    count_end = str(end_count)
    assembly_eq_commands = [
        "@SP\n",
        "A=M-1\n",
        "D=M\n",
        "A=A-1\n",
        "D=D-M\n",
        "@EQUAL" + count + "\n",
        "D;JEQ\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=0\n",
        "@END" + count_end + "\n",
        "0;JMP\n",
        "(EQUAL" + count + ")\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "D=0\n",
        "D=D-1\n",
        "M=D\n"
        "(END" + count_end + ")\n",
        "@SP\n",
        "M=M-1\n"
        #"(END_FINAL)\n"
    ]

    for command in assembly_eq_commands:
        assembly_arithmetic_commands.append(command)


greater_count = -1
def convert_gt(assembly_arithmetic_commands):
    global greater_count
    greater_count += 1
    count = str(greater_count)
    global end_count
    end_count += 1
    count_end = str(end_count)
    assembly_gt_commands = [
        "@SP\n",
        "A=M-1\n",
        "D=M\n",
        "A=A-1\n",
        "D=D-M\n",
        "@GREATER" + count + "\n",
        "D;JLT\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=0\n",
        "@END" + count_end + "\n",
        "0;JMP\n",
        "(GREATER" + count + ")\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "D=0\n",
        "D=D-1\n",
        "M=D\n"
        "(END" + count_end + ")\n",
        "@SP\n",
        "M=M-1\n"
        #"(END_FINAL)\n"
    ]

    for command in assembly_gt_commands:
        assembly_arithmetic_commands.append(command)


lower_count = -1
def convert_lt(assembly_arithmetic_commands):
    global lower_count
    lower_count += 1
    count = str(lower_count)
    global end_count
    end_count += 1
    count_end = str(end_count)
    assembly_lt_commands = [
        "@SP\n",
        "A=M-1\n",
        "D=M\n",
        "A=A-1\n",
        "D=D-M\n",
        "@LOWER" + count + "\n",
        "D;JGT\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=0\n",
        "@END" + count_end + "\n",
        "0;JMP\n",
        "(LOWER" + count + ")\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "D=0\n",
        "D=D-1\n",
        "M=D\n"
        "(END" + count_end + ")\n",
        "@SP\n",
        "M=M-1\n"
        #"(END_FINAL)\n"
    ]

    for command in assembly_lt_commands:
        assembly_arithmetic_commands.append(command)


def convert_and(assembly_arithmetic_commands):
    assembly_and_commands = [
        "@SP\n",
        "A=M-1\n",
        "D=M\n",
        "A=A-1\n",
        "D=D&M\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=D\n"
        "@SP\n",
        "M=M-1\n"
        #"(END)\n"
    ]

    for command in assembly_and_commands:
        assembly_arithmetic_commands.append(command)


def convert_or(assembly_arithmetic_commands):
    assembly_or_commands = [
        "@SP\n",
        "A=M-1\n",
        "D=M\n",
        "A=A-1\n",
        "D=D|M\n",
        "@SP\n",
        "A=M-1\n",
        "A=A-1\n",
        "M=D\n"
        "@SP\n",
        "M=M-1\n"
        #"(END)\n"
    ]

    for command in assembly_or_commands:
        assembly_arithmetic_commands.append(command)


def convert_not(assembly_arithmetic_commands):
    assembly_not_commands = [
        # "@SP\n",
        # "D=M\n",
        # "@256\n",
        # "D=D-A\n",
        # "@END\n",
        # "D;JLE\n",
        "@SP\n",
        "A=M-1\n",
        "M=!M\n"
        #"(END)\n",
    ]

    for command in assembly_not_commands:
        assembly_arithmetic_commands.append(command)


def append_check_if_index_in_bound(assembly_arithmetic_commands, command):
    return
    # assembly_arithmetic_commands.append("@SP\n")
    # assembly_arithmetic_commands.append("A=M-1\n")
    # assembly_arithmetic_commands.append("A=A-1\n")
    # assembly_arithmetic_commands.append("D=A\n")
    # assembly_arithmetic_commands.append("@256\n")
    # assembly_arithmetic_commands.append("D=D-A\n")
    # if command == "gt" or command == "lt":
    #     assembly_arithmetic_commands.append("@END_FINAL\n")
    # else:
    #     assembly_arithmetic_commands.append("@END\n")
    # assembly_arithmetic_commands.append("D;JLT\n")


def convert_arithmetic_command(line):
    command = line[0]
    assembly_arithmetic_commands = []
    append_check_if_index_in_bound(assembly_arithmetic_commands, command)
    if command == "add":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_add(assembly_arithmetic_commands)
    elif command == "sub":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_sub(assembly_arithmetic_commands)
    elif command == "eq":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_eq(assembly_arithmetic_commands)
    elif command == "neg":
        convert_neg(assembly_arithmetic_commands)
    elif command == "gt":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_gt(assembly_arithmetic_commands)
    elif command == "lt":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_lt(assembly_arithmetic_commands)
    elif command == "and":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_and(assembly_arithmetic_commands)
    elif command == "or":
        append_check_if_index_in_bound(assembly_arithmetic_commands, command)
        convert_or(assembly_arithmetic_commands)
    elif command == "not":
        convert_not(assembly_arithmetic_commands)
    else:
        print("arithemtic command is wrong or missing\n")
        return
    write_assembly_to_output_file(assembly_arithmetic_commands)

def convert_label_command(line):
    return


def convert_goto_command(line):
    return


def convert_if_command(line):
    return


def convert_function_command(line):
    return


def convert_return_command(line):
    return


def convert_call_command(line):
    return


def determine_command(line):
    global output_file
    output_file.write("// ")
    for element in line:
        output_file.write(element)
    output_file.write("\n")
    if line[0] == 'push':
        convert_push_command(line)
    elif line[0] == 'pop':
        convert_pop_command(line)
    elif line[0] in arithmetic_commands:
        convert_arithmetic_command(line)
    else:
        print("It is some other command")
        return


def clean(line):
    line_cleaned = []
    index = 0
    while index < (len(line)) and line[index] != '//':
        line_cleaned.append(line[index])
        index += 1
    return line_cleaned


def parse_input_file():
    global input_file
    for line in input_file:
        line_split = line.split()
        if line_split == [] or line_split[0] == "//":
            continue
        else:
            cleaned_line = clean(line_split)
            print(cleaned_line)
            # determine command
            determine_command(cleaned_line)


def main():
    open_input_file()
    open_output_file()  # e.g. StackTest.txt
    parse_input_file()  # e.g. StackTest.asm
    close_files()


if __name__ == '__main__':
    main()
    print("Hello World!")
