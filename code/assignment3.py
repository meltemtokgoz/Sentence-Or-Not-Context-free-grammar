import random


# find necessary comment line number
def find_line_num(path):
    start_vocab = 0
    start_rule = 0
    with open(path) as f:
        for line in f:
            start_vocab += 1
            if '# Vocabulary. There is no rule for rewriting the terminals.' in line:
                break
    with open(path) as f:
        for line in f:
            start_rule += 1
            if '#    Pronoun  = Pronoun ' in line:
                break
    return start_vocab, start_rule


# word_dict = { 'word' : 'word_type'} example : {'ate': 'Verb', 'floor' : 'Noun'}
def word_and_type_dict(path,start_vocab):
    word_dict = {}
    word_list =[]
    with open(path) as f:
        line_num = 0
        for line in f:
            line_num += 1
            if line_num > start_vocab:
                if line != "\n":
                    token = line.strip().split()
                    word_dict[token[1]] = token[0]
                    word_list.append(token[1])
    return word_dict, word_list


# rule_dict = {'NP VP': 'S', 'Verb NP': 'VP' ...}
def rules(path, start_vocab, start_rule):
    rule_dict ={}
    with open(path) as f:
        line_num = 0
        for line in f:
            line_num += 1
            if line_num > start_rule:
                if line_num < start_vocab:
                    if line != "\n":
                        token = line.strip().split()
                        first_part = token[0]
                        second_part = ""
                        x = 0
                        for i in token[1:]:
                            x += 1
                            if x < len(token)-1:
                                second_part = second_part + i + " "
                            else:
                                second_part = second_part + i
                        rule_dict[second_part] = first_part
    return rule_dict


# generate random sentence function
def random_sentence(sent_count, sent_length, word_list):
    out_file = open("output.txt", "w")
    for x in range(sent_count):
        sentence = ""
        for i in range(sent_length):
            new_word = random.choice(word_list)
            sentence = sentence + new_word + " "
        out_file.write(sentence+"\n")
    out_file.close()


# cyk parser algorithm
def cyk_parser(c_r, c_c, matrix, sentence, rule_dict, word_dict, sent_len):
    token = sentence.strip().split()
    if (c_r + c_c) <= (sent_len-1):
        if c_r == 0:
            matrix[c_r][c_c].append(word_dict[token[c_c]])
            if word_dict[token[c_c]] in rule_dict.keys():
                matrix[c_r][c_c].append(rule_dict[word_dict[token[c_c]]])
        else:
            temp_c = c_c
            temp_r = c_r
            for i in range(c_r):
                if temp_c + temp_r <= len(sentence)-1:
                    if len(matrix[i][c_c]) != 0:
                        for temp_word_1 in matrix[i][c_c]:
                            first_item = temp_word_1
                            if len(matrix[temp_r-1][temp_c+1]) != 0:
                                for temp_word_2 in matrix[temp_r-1][temp_c+1]:
                                    second_item = temp_word_2
                                    temp_pair = first_item+" "+second_item
                                    if temp_pair in rule_dict.keys():
                                        matrix[c_r][c_c].append(rule_dict[temp_pair])
                    temp_c += 1
                    temp_r -= 1
            if c_r == len(matrix)-1:
                true_or_false = 0
                for temp_word_3 in matrix[c_r][c_c]:
                    if temp_word_3 == 'S':
                        true_or_false += 1
                        break
                print(sentence.strip())
                if true_or_false > 0:
                    print("Result : It's a grammatically correct sentence.")
                else:
                    print("Result : It's not a grammatically correct sentence.")

    return matrix


def main():
    # read the input file
    path = "cfg.gr"
    start_vocab, start_rule = find_line_num(path)

    # created dictionary to word and rule
    word_dict, word_list = word_and_type_dict(path, start_vocab)
    rule_dict = rules(path, start_vocab, start_rule)

    # parameter sentence length and count
    sent_length = 5
    sent_count = 2

    # generated sentence
    random_sentence(sent_count, sent_length, word_list)

    # read the output file and call cyk parser function to all sentences
    with open("output.txt") as f:
        for line in f:
            if line != "\n":
                matrix = [[[] for x in range(sent_length)] for y in range(sent_length)]
                len_s = len(line.strip().split())
                print("-----------------------------------------------")
                for current_row in range(len_s):
                    for current_column in range(len_s):
                        matrix = cyk_parser(current_row, current_column, matrix, line, rule_dict, word_dict, len_s)

                # prints cyk table  if you want to see
                '''
                k = sent_length-1
                while k >= 0:
                    if k == 0:
                        print(matrix[k])
                    else:
                        print(matrix[k][0:(sent_length-k)])
                    k -= 1
                '''


if __name__ == '__main__':
    main()