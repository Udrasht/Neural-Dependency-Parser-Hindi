import re

new_dependencies, dependencies = [], []
count = 0
filename = 'extracted_head.txt'
output_filename = 'extracted_head.txt'

with open(filename, 'r', encoding='utf-8') as f, open(output_filename, 'w', encoding='utf-8') as output_file:
    for line in f:

        if line.rstrip():

            line = re.sub("\s+", " ", line)
            line1 = line.split(" ")

            if line1[0] == "<Sentence":
                output_file.write("<Sentence id='" + str(count+1) + "'>\n")
                count += 1
                
            elif line1[0].strip() == "</Sentence>":
                n1 = len(dependencies)
                for t in range(0, n1 ):
                    temp = []

                    if dependencies[t][7] == "ROOT":
                        temp.append("ROOT")
                        temp.append(";")
                        for k in range(len(dependencies[t])):
                            temp.append(dependencies[t][k])
                        indx = len(temp)
                        temp.insert(indx,";")
                        temp.insert(indx+1,"L")
                        temp.insert(indx+2,";")
                        temp.insert(indx+3,"ROOT")

                    #if dependencies[t][7] != "ROOT":
                    else:
                        for j in range(0, n1):

                            if dependencies[t][7] == dependencies[j][5]:
                                if t > j:

                                    for k in range(len(dependencies[j])):
                                        temp.insert(len(temp), dependencies[j][k])

                                    temp.append(";")

                                    for k in range(len(dependencies[t])):
                                        temp.insert(len(temp), dependencies[t][k])

                                    temp.append(";")
                                    temp.append("L")

                                elif j > t:
                
                                    for k in range(0, len(dependencies[t])):
                                        temp.insert(len(temp), dependencies[t][k])

                                    temp.append(";")

                                    for k in range(len(dependencies[j])):
                                        temp.insert(len(temp), dependencies[j][k])

                                    temp.append(";")
                                    temp.append("R")

                                temp.append(";")
                                temp.append(dependencies[t][6])
                                break

                    new_dependencies.append(temp)

                n2 = len(new_dependencies)
                for t in range(n2):
                    for j in new_dependencies[t]:
                        output_file.write(j + " ")
                    output_file.write("\n")

                output_file.write(line1[0].strip() + "\n")
                new_dependencies.clear()
                dependencies.clear()
                

            elif line1[0] == "H":
                dependencies.insert(len(dependencies) , line1)

            else:
                # print(line)
                output_file.write(line)
                output_file.write("\n")

# This part is outside the loop, so it will execute after processing all lines in the input file.
# output_file.write("Final output line\n")
