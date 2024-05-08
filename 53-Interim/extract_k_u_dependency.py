import re
import os
import json

output_file_path = 'parsed_output.txt'
input_file_path = "after_clean.txt"
data_list_file_path = "data_lists.json"

if os.path.exists(output_file_path):
    # Delete the file
    os.remove(output_file_path)
    print(f"File '{output_file_path}' deleted successfully.")
else:
    print(f"File '{output_file_path}' does not exist.")


tags_pair, tags,= [], [] 
unknown_dependencies_name, heads_name =[], []
line_number, flag, word_data = 0, 0, {}

def extract_unknown_dependencies():
    for dependency in range(len(tags)):
        if tags[dependency][2] == "R":
            t1=tags[dependency][1]
            head_index = heads_name.index(t1)
            t0=tags[dependency][0]
            dependent_index = heads_name.index(t0)
            n_dif=head_index - dependent_index
            if (n_dif) > 3:
                cnt, pair1, pair2 = 0, [heads_name[dependent_index], heads_name[head_index - 1]], [heads_name[dependent_index], heads_name[dependent_index + 1]]
                if pair1 not in unknown_dependencies_name:
                    if pair1 not in tags_pair:
                        cnt =cnt+ 1
                        unknown_dependencies_name.insert(len(unknown_dependencies_name) , pair1)
                        
                if pair2 not in unknown_dependencies_name:
                    if pair2 not in tags_pair:
                        cnt =cnt+ 1
                        n11=len(unknown_dependencies_name)
                        unknown_dependencies_name.insert(n11, pair2)
                        

                if cnt < 2:
                    for i in range(dependent_index + 2, head_index - 1, 1):
                        pair = [heads_name[dependent_index], heads_name[i]]
                        if pair not in unknown_dependencies_name and pair not in tags_pair:
                            unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)
                            cnt = cnt+1
                        if cnt == 2:
                            break

            elif (head_index) > 1 + dependent_index:
                pair1 = [heads_name[dependent_index], heads_name[dependent_index + 1]]
                indx=0
                if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
                    indx = len(unknown_dependencies_name)
                    unknown_dependencies_name.insert(indx, pair1)
                elif (head_index) > 2 + dependent_index:	
                    pair= [heads_name[dependent_index], heads_name[dependent_index + 2]]
                    indx=0
                    if pair not in unknown_dependencies_name and pair not in tags_pair:
                        unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)

        elif tags[dependency][2] == "L":
            if tags[dependency][0] != "ROOT" and tags[dependency][1] != "BLK":
                dependent_index, head_index = heads_name.index(tags[dependency][1]), heads_name.index(tags[dependency][0])
                if (dependent_index) >(3 + head_index):
                    cnt, pair2, pair1 =0, [heads_name[dependent_index - 1], heads_name[dependent_index]], [heads_name[head_index + 1], heads_name[dependent_index]]
                    if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
                        cnt = cnt+1
                        unknown_dependencies_name.insert(len(unknown_dependencies_name), pair1)
                
                    if pair2 not in unknown_dependencies_name and pair2 not in tags_pair:
                       
                        unknown_dependencies_name.insert(len(unknown_dependencies_name), pair2)
                        cnt += 1

                    if 2 > cnt:
                        for i in range(dependent_index - 2, head_index + 1, -1):
                            pair = [heads_name[i], heads_name[dependent_index]]
                            indx=0
                            if pair not in unknown_dependencies_name and pair not in tags_pair:
                                cnt = cnt+1
                                unknown_dependencies_name.insert(len(unknown_dependencies_name) ,pair)
                            if cnt == 2:
                                break

                elif (head_index) > 1 + dependent_index:
                    indx=0
                    pair1 = [heads_name[dependent_index - 1], heads_name[dependent_index]]
                    
                    
                    if pair1 not in unknown_dependencies_name and pair1 not in tags_pair:
                        unknown_dependencies_name.insert(len(unknown_dependencies_name), pair1)
                    elif (head_index) > (2 + dependent_index):
                        pair = [heads_name[dependent_index - 2], heads_name[dependent_index]]
                        if pair not in unknown_dependencies_name and pair not in tags_pair:
                            
                            unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)

            else:
                dependent_index = heads_name.index(tags[dependency][1])
                cnt=0
                for i in range(dependent_index - 1 , -1 , -1):
                    pair = [heads_name[i], heads_name[dependent_index]]
                    if pair not in unknown_dependencies_name and pair not in tags_pair:
                        cnt=cnt+1
                        unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)
                        
                    if cnt == 2:
                        break
                cnt = 0
                for i in range(0, dependent_index - 1, 1):
                    pair, indx = [heads_name[i], heads_name[dependent_index]], 0
                    if pair not in unknown_dependencies_name and pair not in tags_pair:
                        cnt=cnt+1
                        unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)
                        
                    if cnt == 2:
                        break

                if tags[dependency][0] != "ROOT":
                    cnt=0
                    dependent_index =heads_name.index(tags[dependency][1])
                    for i in range(dependent_index - 1, -1, -1):
                        pair = ["ROOT", heads_name[i]]
                        if pair not in unknown_dependencies_name and pair not in tags_pair:
                            
                            cnt=cnt+1
                            unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)
                            
                        if cnt == 2:
                            break
                    cnt = 0
                    for i in range(0, dependent_index - 1, 1):
                        pair = ["ROOT", heads_name[i]]
                        if pair not in unknown_dependencies_name and pair not in tags_pair:
            
                            cnt=cnt+1
                            unknown_dependencies_name.insert(len(unknown_dependencies_name), pair)
                    
                        if cnt == 2:
                            break
cnt1 = 0
total = 0
def print_unknown_dependencies():
    global total, cnt1
    # print(type(word_data))
    # print(word_data.keys())
    # print(word_data)
    total = total+ 1
    with open(output_file_path, "a",encoding='utf-8') as f:
        for dependency in range(len(unknown_dependencies_name)):
            # print(unknown_dependencies_name[ dependency][0], unknown_dependencies_name[ dependency][1])
            if( unknown_dependencies_name[ dependency][0] in word_data and unknown_dependencies_name[ dependency][1] in word_data ):
                f.write(word_data[unknown_dependencies_name[ dependency][0] ].strip() + " ; ")
                f.write(word_data[unknown_dependencies_name[ dependency][1] ].strip() + " ; ")
                f.write("U ; NULL\n")
            else:
                cnt1=cnt1+ 1
count = 0
f = open(input_file_path, "r", encoding='utf-8')

for line in f:
    
    
    line_number =line_number+ 1
    pattern_start = re.compile('<S+')
    pattern_head = re.compile('H+')
    pattern_root = re.compile('ROOT+')
    pattern_end = re.compile('</S+')
    
    line = re.sub("\s+", " ", line)

    if pattern_start.match(line):
        line_number = 0
        sentence_id = line.split("'")[1]

    elif pattern_end.match(line):
        extract_unknown_dependencies()
        print_unknown_dependencies()
        word_data.clear()
        tags_pair, tags= [], []
        unknown_dependencies_name, heads_name=[], []
        

    elif line_number == 8:
        
        line2 = line.strip().split(" ")
        heads_name = []
        
        for i in range(len(line2)):   
            heads_name.insert(len(heads_name), line2[i])

    elif pattern_head.match(line):
        with open(output_file_path, "a",encoding='utf-8') as f:
            f.write(line)
            f.write("\n")

        line_state_pairs, line_state = [], []
        line_state=[]

        line1 = line.split(";")
        
        line_state.insert(len(line_state), line1[0].split(" ")[5])
     
        line_state_pairs.insert(len(line_state_pairs), line1[0].split(" ")[5])
       
        try:
            line_state.insert(len(line_state), line1[1].split(" ")[6])
        except Exception as e:
            print(e,cnt1, total)
            continue
            # print(e)
            # print(line1)
            # print(line1[1].split(" "))
            
        
        line_state_pairs.insert(len(line_state_pairs), line1[1].split(" ")[6])
        
        line_state.insert(len(line_state), line1[2].split(" ")[1])
        indx = len(tags)
        tags.insert(indx, line_state)
        tags_pair.insert(len(tags_pair), line_state_pairs)

        if line_state[0] not in word_data:
            word_data[line_state[0]] = line1[0]
        if line_state[1] not in word_data:
            word_data[line_state[1]] = line1[1]

    elif pattern_root.match(line):
        with open(output_file_path, "a", encoding='utf-8') as f:
            f.write(line)
            f.write("\n")

        line_state_pairs, line_state = [], []
        line_state=[]
        line1 = line.split(";")
        
        line_state.insert(len(line_state), "ROOT")
        
        line_state_pairs.insert(len(line_state_pairs), "ROOT")
        
        line_state.insert(len(line_state), line1[1].split(" ")[6])
        line_state_pairs.insert(len(line_state_pairs), line1[1].split(" ")[6])
        line_state.insert(len(line_state), "L")
        tags.insert(len(tags), line_state)
        tags_pair.insert(len(tags_pair), line_state_pairs)

        if line_state[0] not in word_data:
            word_data[line_state[0]] = line1[0]  

f.close()

print("Count:", cnt1, total)
print("Get Lists:")

tags, chunk_tags, root, words = [],[],[],[]
root, words = [],[]

li = 0
f = open(output_file_path, "r",encoding='utf-8')
for line in f:
    li += 1
    print(li)
    if(line.rstrip()):
        line = re.sub("\s+"," ",line)
        line1 = line.split(";")

        a1 = line1[0].split(" ")
        a2 = line1[1].split(" ")
        print("line1",line1)
        print("a1", a1)
        print("a2", a2)

        if(a1[0] == "H"):
            if a1[1] not in words:
          
                words.insert(len(words) , a1[1])
            if a1[2] not in root:
              
                root.insert(len(root) , a1[2])
            if a1[3] not in chunk_tags:
                
                chunk_tags.insert(len(chunk_tags),a1[3])
            if a1[4] not in tags:
                indx = len(tags)
                tags.insert(indx,a1[4])

        
        if a2[2] not in words:
           
            words.insert(len(words) , a2[2])
        if a2[3] not in root:
            
            root.insert(len(root),a2[3])
        if a2[4] not in chunk_tags:
          
            chunk_tags.insert(len(chunk_tags),a2[4])
        if a2[5] not in tags:
            i
            tags.insert(len(tags),a2[5])	


# print(len(words))					
# print(len(root))					
# print(len(tags))					
# print(len(chunk_tags))

words.append("ROOT")
root.append("ROOT")
tags.append("ROOT")
chunk_tags.append("ROOT")

data = {}
data["root"] = root
data["tags"] = tags
data["words"] = words
data["chunk_tags"] = chunk_tags


with open(data_list_file_path,"w") as f:
	json.dump(data,f)
