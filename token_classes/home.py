import re

#source code file path
SOURCE_CODE_FILE_PATH = "source_code.txt"

#pre-defined lists of keywords, operators and punctuations
keywords_list = ["for", 'if', 'else', 'while', 'this', 'not', 'and', 'or', 'delete', 'new', 'return',
                 'break', 'continue', 'goto', 'switch', 'case', 'int', 'float', 'double', 'bool', 'string',
                 'vector', 'char', 'cout', 'cin', 'null', 'using', 'namespace', 'std', 'include', 'iostream',
                 'main', 'endl']

punctuations_list = ['}', '{', '(', ')', '[', ']', ';', ':', ',', '.', '"', "'", '#']
operators_list = ['+', '-', '*', '/', '=', '^', '>', '<', '&', '|', '!', '%']

#regular expressions for identifiers and constants
identifier_regex = "^[a-zA-z_][a-zA-z0-9_]*$"
constant_regex = "[0-9]+"

#initialize empty lists for token classes
line_comments_found = []
block_comments_found = []
operators_found = []
punctuations_found = []
constants_found = []
identifiers_found = []
keywords_found = []
strings_found = []


#function to returns list of unique values (removes dublicate)
def unique_list(list):
    unique = []
    for item in list:
        if item not in unique:
            unique.append(item)
    return unique


#write token-lexeme pairs to token_lexeme_pairs.txt
def token_lexeme_pair(list, name, FILE_PATH):
    token_lexeme_pair = []
    file = open(FILE_PATH, 'a+')
    for item in list:
        pair = '<' + name + ', ' + item + '>'
        token_lexeme_pair.append(pair)
        file.write(pair + '\n')
    return token_lexeme_pair


# read source code from a file
file = open(SOURCE_CODE_FILE_PATH, "r")
contents = file.read()

# recognize operators, punctuations, line comments, block comments
index = 0
block_comment_started = False
line_comment_started = False
string_started = False
string_count = 0
block_comment = ""
string = ""

lines = contents.split('\n')
line_counter = 0

for line in lines:
    line_comment = ""
    for counter in range(0, len(line)):
        line += ' '
        end = False

        #identify operators and punctuations other than in comments and strings
        if line_comment_started == False and block_comment_started == False and string_started == False:

            # identify single characters operators
            if (line[counter] in operators_list and line[counter + 1] not in operators_list and line[counter - 1] not in operators_list):
                operators_found.append(line[counter])
                lines[line_counter] = lines[line_counter].replace(line[counter], ' ')

            # identify double characters operators
            if line[counter] in operators_list and line[counter + 1] in operators_list:

                #identify operators other than comment initializers
                if (line[counter] + line[counter + 1]) not in ['//', '/*', '*/']:
                    operators_found.append(line[counter] + line[counter + 1])
                    lines[line_counter] = lines[line_counter].replace(line[counter] + line[counter + 1], '  ')

            # Identify punctuations
            if line[counter] in punctuations_list:
                punctuations_found.append(line[counter])
                lines[line_counter] = lines[line_counter].replace(line[counter], ' ')

        # identify line comments start point
        if (line[counter] + line[counter + 1]) == '//':
           line_comment_started = True

        # identify block comments start point
        if (line[counter] + line[counter + 1]) == '/*':
            block_comment_started = True

        # identify block comments end point and append block comment to the list
        if (line[counter] + line[counter + 1]) == '*/':
            lines[line_counter] = lines[line_counter].replace(line[counter] + line[counter + 1], '  ')
            block_comment_started = False
            # block_comment = block_comment.replace('/*', '')
            block_comment += '*/'
            block_comments_found.append(block_comment)
            block_comment = ""

        #identify block comments
        if block_comment_started:
            block_comment += line[counter]
            lines[line_counter] = lines[line_counter].replace(line[counter], ' ')

        #identify line comments
        if line_comment_started:
            line_comment += line[counter]
            lines[line_counter] = lines[line_counter].replace(line[counter], ' ')

        #identify start of a string
        if line[counter] == '"' and string_started == False:
            string_started = True
            string_count = 1

        #identify end of a string
        if line[counter] == '"' and string_started == True and string_count != 1:
            string_started = False
            string = string.replace('"', '')
            lines[line_counter] = lines[line_counter].replace(string, ' ')
            strings_found.append(string)
            string = ""

        #identify strings
        if string_started:
            string += line[counter]
            # lines[line_counter] = lines[line_counter].replace(line[counter], ' ')

        index += 1
        string_count = 0

    #add end line characters in block comments
    if block_comment_started:
        block_comment += '\n'

    #append line comment to list and terminate comment
    if line_comment_started:
        # line_comment = line_comment.replace('//', '')
        line_comments_found.append(line_comment)
        line_comment_started = False

    #storing location of a character in source code as index (optional)
    index += 1
    line_counter += 1


#identify keywords, identifiers, constants using regex class
for line in lines:
    words = line.split()
    for word in words:

        #identify keywords
        if word in keywords_list:
            keywords_found.append(word)

        #identify identifiers
        temp = re.findall(identifier_regex, word)
        if len(temp) != 0:
            if temp[0] not in keywords_list:
                identifiers_found.append(temp[0])

        #identify constants
        constants_found += re.findall(constant_regex, word)

#repace line terminator with end line character (/n)
# contents = re.sub("\n", '/n', contents)
# print(contents)

#remove line comments from the code
for comment in line_comments_found:
    contents = re.sub(comment, "", contents)

#remove block comments from the code
for comment in block_comments_found:
    contents = re.sub(re.escape(comment), "", contents)

#write code without comments to file code_without_comments.txt
write_code_to_file = open("code_without_comments.txt", 'w')
write_code_to_file.write(contents)

#remove white spaces from the code
contents = re.sub("\s", '', contents)

#removing dublicate items in lists
keywords_found = unique_list(keywords_found)
identifiers_found = unique_list(identifiers_found)
constants_found = unique_list(constants_found)
operators_found = unique_list(operators_found)
punctuations_found = unique_list(punctuations_found)
line_comments_found = unique_list(line_comments_found)
block_comments_found = unique_list(block_comments_found)
strings_found = unique_list(strings_found)

#making a list of token-lexeme pairs in a source code
token_lexeme_pair_list = token_lexeme_pair(keywords_found, 'keyword', "token_lexeme_pairs.txt")
token_lexeme_pair_list += token_lexeme_pair(operators_found, 'operator', "token_lexeme_pairs.txt")
token_lexeme_pair_list += token_lexeme_pair(punctuations_found, 'punctuation', "token_lexeme_pairs.txt")
token_lexeme_pair_list += token_lexeme_pair(identifiers_found, 'identifier', "token_lexeme_pairs.txt")
token_lexeme_pair_list += token_lexeme_pair(constants_found, 'constant',"token_lexeme_pairs.txt")

print("Keywords Recognized : ", keywords_found)
print("Identifiers Recognized : ", identifiers_found)
print("Constants Recognized : ", constants_found)
print("Operators Recognized : ", operators_found)
print("Punctuations Recognized : ", punctuations_found)
print("Line Comments Recognized : ", line_comments_found)
print("Block Comments Recognized : ", block_comments_found)
print("Strings Recognized : ", strings_found)
print("token-lexeme Pairs : ", token_lexeme_pair_list)
print("\nCode without white spaces and Comments : \n", contents)
print("\nNote:\n1. Code without comments have been written to code_without_comment.txt !!!")
print("2. token-lexeme pairs have been written to token_lexeme_pairs.txt !!!")

