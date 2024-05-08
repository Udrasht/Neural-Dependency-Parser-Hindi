import re

count = 0

head_list = {
    "JJP1": ["QF", "QC", "QO"],
    "JJP": ["JJ"],
    "NEGP": ["NEG"],
    "VG*": ["VM"],
    "RBP1": ["NN", "WQ"],
    "RBP": ["RB"],
    "BLK1": ["UNK", "RP", "INJ"],
    "BLK": ["SYM"],
    "CCP1": ["SYM"],
    "CCP": ["CC"],
    "NP1": ["QC", "QF", "QO"],
    "NP": ["NN", "PRP", "NNP"],
    "NP2": ["NST"],
    "NP3": ["WQ"]
}


heads_o_pos = heads = sentence_pos = heads_lemma = heads_name = heads_pos = sentence_lemma = sentence = ""

head_relation = head_pos = head_name = head_relative_name = head_lemma = head_o_pos = head = ""

chunk_lemma, dependencies, chunk_pos, chunk_words = [], [], [], []

def find_head_jjp():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['JJP']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['JJP1']:
            if chunk_pos[i] == j:
                return i

def find_head_vg():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['VG*']:
            if chunk_pos[i] == j:
                return i

def find_head_negp():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['NEGP']:
            if chunk_pos[i] == j:
                return i

def find_head_rbp():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['RBP']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['RBP1']:
            if chunk_pos[i] == j:
                return i

def find_head_blk():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['BLK']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['BLK1']:
            if chunk_pos[i] == j:
                return i

def find_head_ccp():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['CCP']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['CCP1']:
            if chunk_pos[i] == j:
                return i

def find_head_np():
    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['NP']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['NP1']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['NP2']:
            if chunk_pos[i] == j:
                return i

    for i in range(len(chunk_pos) - 1, -1, -1):
        for j in head_list['NP3']:
            if chunk_pos[i] == j:
                return i
            
def write_output_file(sentence, sentence_lemma, sentence_pos, heads, heads_lemma, heads_pos, heads_name):
    output_file.write(sentence + "\n")
    output_file.write(sentence_lemma + "\n")
    output_file.write(sentence_pos + "\n")
    output_file.write(heads + "\n")
    output_file.write(heads_lemma + "\n")
    output_file.write(heads_o_pos + "\n")
    output_file.write(heads_pos + "\n")
    output_file.write(heads_name + "\n")

def find_head(head_o_pos):
    index = -1
    if head_o_pos == "JJP":
        index = find_head_jjp()
    elif head_o_pos == "NEGP":
        index = find_head_negp()
    elif head_o_pos == "RBP":
        index = find_head_rbp()
    elif head_o_pos == "VGF" or head_o_pos == "VGNN" or head_o_pos == "VGNF":
        index = find_head_vg()
    elif head_o_pos == "BLK":
        index = find_head_blk()
    elif head_o_pos == "CCP":
        index = find_head_ccp()
    elif head_o_pos == "NP":
        index = find_head_np()
    return index


filename = "extract_data.txt" 
output_filename = 'extracted_head.txt'

with open(filename, 'r', encoding='utf-8') as f, open(output_filename, 'w', encoding='utf-8') as output_file:
    for line in f:
        if line.rstrip():
            line1 = re.sub('\s+', " ", line).split(" ")

            if line1[0] == "<Sentence":
                output_file.write("<Sentence id='" + str(count+1) + "'>\n")
                count += 1

            elif line1[0].strip() == "</Sentence>":
                
                head = chunk_words[find_head(head_o_pos)]
                heads += head + " "
                
                head_pos = chunk_pos[find_head(head_o_pos)]
                heads_pos += head_pos + " "

                head_lemma = chunk_lemma[find_head(head_o_pos)]
                heads_lemma += head_lemma + " "
            
                heads_o_pos += head_o_pos + " "
                
                
                fill = "H " + head + " " + head_lemma + " " + head_o_pos + " " + head_pos + " " + head_name + " " + head_relation + " " + head_relative_name
                indx = len(dependencies)
                dependencies.insert(indx, fill)

                heads_name += head_name + " "
                write_output_file(sentence, sentence_lemma, sentence_pos, heads, heads_lemma, heads_pos, heads_name)

                for i in dependencies:
                    output_file.write(i + "\n")

                heads_lemma, heads_o_pos, heads, sentence_lemma, heads_name, heads_pos, sentence_pos, sentence = '', '', '', '', '', '', '', ''
                
                dependencies.clear()
                chunk_words.clear()
                chunk_pos.clear()
                chunk_lemma.clear()

                output_file.write(line1[0].strip() + "\n")

            elif line1[0] == "T":

                chunk_words.insert(len(chunk_words), line1[1])
                chunk_pos.insert(len(chunk_pos), line1[2])
                chunk_lemma.insert(len(chunk_lemma), line1[3])

                sentence_lemma += line1[3] + " "
                sentence_pos += line1[2] + " "
                sentence += line1[1] + " "

            elif line1[0] == 'H':
                if len(chunk_words):

                    head = chunk_words[find_head(head_o_pos)]
                    heads += head + " "
                    
                    head_pos = chunk_pos[find_head(head_o_pos)]
                    heads_pos += head_pos + " "
                    
                    head_lemma = chunk_lemma[find_head(head_o_pos)]
                    heads_lemma += head_lemma + " "
                    
                    heads_name += head_name + " "
                    heads_o_pos += head_o_pos + " "

                    fill = "H " + head + " " + head_lemma + " " + head_o_pos + " " + head_pos + " " + head_name + " " + head_relation + " " + head_relative_name
                    indx = len(dependencies)
                    dependencies.insert(indx, fill)

                chunk_words.clear()
                chunk_pos.clear()
                chunk_lemma.clear()

                head_relative_name = line1[4]
                head_relation = line1[3]
                head_name = line1[2]
                head_o_pos = line1[1]

            

    # This part is outside the loop, so it will execute after processing all lines in the input file.
    # output_file.write("Final output line\n")


