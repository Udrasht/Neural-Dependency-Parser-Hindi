import re

head_const_tags = ""
tags = {"NP": [], "JJP": [], "CCP": [], "VGNF": [], "VGF": [], "BLK": [], "VGNN": [], "RBP": [], "FRAGP": [], "NEGP": []}
head_tag = 0
count, cnt, w = 0, 0, 0

# filename = "training.txt"
filename = "testing.txt"

with open(filename, "r", encoding='utf-8') as f, open('extract_data.txt', 'w', encoding='utf-8') as output_file:
    for line in f:
        if line.rstrip():
            line = re.sub("\s+", " ", line)
            troot = 0
            line1 = line.split(' ')
            if line1[0] == "<Sentence":
                count += 1
                output_file.write("<Sentence id=" + "\'" + str(count) + "\'>\n")

            elif line1[0].strip() == "))":
                if head_const_tags not in tags[str(head_tag)]:
                    indx = len(tags[str(head_tag)])
                    tags[str(head_tag)].insert(indx, head_const_tags)
                troot = 0
                continue
            
            elif line1[0].strip() == "</Sentence>":
                output_file.write(line1[0].strip() + "\n")
            
            elif line1[1] == "((":
                head_const_tags = ""
                relation, relative, drel, name, head_tag = 0, 0, 0, 0, 0
                if line1[2].split("_")[0] != "NULL":
                    head_tag = line1[2]
                else:
                    head_tag = line1[2].split("_")[2]

                for i in range(4, len(line1)):
                    splitted_line = line1[i].split("=")[0]
                    if  splitted_line == "drel" or splitted_line == "dmrel":
                        drel = 1
                        relation = line1[i].split("=")[1].split("\'")[1].split(":")[0]
                        relative = line1[i].split("=")[1].split("\'")[1].split(":")[1]
                    elif splitted_line == "name":
                        name = line1[i].split('=')[1].split("\'")[1]
                    

                output_file.write("H" + " " + head_tag + " ")
                if name == 0:
                    output_file.write("NULL ")
                else:
                    output_file.write(name + " ")
                if drel == 0:
                    output_file.write("NULL ROOT\n")
                else:
                    output_file.write(relation + " " + relative + "\n")
            else:
                troot_tag = line1[2]
                troot = line1[1]
                troot_lemma = line1[4].split("=")[1].split("\'")[1].split(",")[0]
                head_const_tags = head_const_tags + " " + troot_tag
                output_file.write("T " + troot + " " + troot_tag + " " + troot_lemma + "\n")
