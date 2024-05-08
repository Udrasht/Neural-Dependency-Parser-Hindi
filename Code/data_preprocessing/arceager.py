import re
import json

not_parasble_sentences_ki, not_parasble_sentences = [],[]
tags, line_state, buffer = [], [], []
stack, dependencies = [], []
sentence_id = line_number = 0

	
def check_orignal_dependencies():
	f = True
	stack_top = stack[len(stack) - 1]
	buffer_top = buffer[len(buffer) - 1]
	for i in range(len(tags)):
		if(tags[i][0] == stack_top and tags[i][1] == buffer_top):
			f = False
			return tags[i][2],tags[i][3]
	if f:
		return 0,0;	

def check_left_arc():
	f = True
	n1 = len(stack)-1
	n2 = len(dependencies)
	for i in range(n2):
		if(dependencies[i][2] == stack[n1]):
			f = False
			return 0
	if f:
		return 1	

def check_right_arc():
	f = True
	n1 = len(buffer)-1
	n2 = len(dependencies)
	for i in range(n2):
		if(dependencies[i][2] == buffer[n1]):
			f = False
			return 0
	if f:
		return 1
	
def check_reduce():
	n1 = len(stack)-1
	n2 = len(dependencies)
	f = True
	for i in range(n2):
		if(dependencies[i][2] == stack[n1]):
			f = False
			return 1
	if f:
		return 0

def left_arc(relation):
	indx =0 
	n1 = len(stack)
	n2 = len(buffer)
	stack_top = stack[n1 - 1]
	buffer_top = buffer[n2 - 1]
	indx = 0
	temp = []
	temp.insert(indx, buffer_top)
	temp.insert(indx+1, relation)
	temp.insert(indx+2, stack_top)
	dependencies.insert(len(dependencies),temp)
	stack.pop(n1-1)

def right_arc(relation):
	indx = 0
	temp = []
	n1=len(stack)
	n2 = len(buffer)
	stack_top = stack[n1 - 1]
	buffer_top = buffer[n2 - 1]
	indx = 0
	temp.insert(indx , stack_top)
	temp.insert(indx+1,relation)
	temp.insert(indx+2,buffer_top)
	dependencies.insert(len(dependencies) , temp)
	buffer.pop(len(buffer)-1)
	stack.insert(n1 , buffer_top)


def dependency_link():
	n2 = len(buffer)
	buffer_top = buffer[n2 - 1]
	f=True
	n1=len(stack)
	for i in range(n1-2 , -1 , -1):
		for j in range(len(tags)):
			if(tags[j][0] == stack[i] and tags[j][1] == buffer_top):
				f=False
				return 1
	if f:
		return 0			


def reduce():
	stack.pop()

def shift():
	indx = 0
	n2 = len(buffer)
	buffer_top = buffer[n2 - 1]
	buffer.pop(n2-1)
	stack.insert(len(stack) ,buffer_top)


def is_parsable():

	while( not( len(stack) == 1 and len(buffer) == 1) ):

		if(len(buffer) > 1):
			if(len(stack) > 0):
				orignal_dependency,relation = check_orignal_dependencies()
				if(orignal_dependency == 0):
					if(len(stack) > 1):
						if(dependency_link() != 1):
							shift()		
						else:
							if(check_reduce() != 1):
								return 0
							else:
								reduce()
					else:
						shift()


				elif(orignal_dependency == "L"):
					can_right_arc = check_right_arc()
					if(can_right_arc != True):
						return 0
					else:
						right_arc(relation)
						

				elif(orignal_dependency == "R"):
					can_left_arc = check_left_arc()
					if(can_left_arc != True):
						return 0
					else:
						left_arc(relation)
						

		elif(len(stack) > 1 and len(buffer) == 1):
			can_reduce = check_reduce()
			if(can_reduce!=True):
				return 0
			else:
				reduce()

	if(stack[0] != "ROOT"  ):
		return 0
	else:
		if( buffer[0] == "BLK"):
			return 1

def get_line_state():
	line_state = []
	indx = 0
	line1 = line.split(";")
	line_state.insert(indx,"ROOT")
	line_state.insert(indx+1,line1[1].split(" ")[6])
	line_state.insert(indx+2,"L")
	line_state.insert(indx+3,"ROOT")
	return line_state														

input_file = "extract_dependency.txt" 
f = open(input_file, "r",encoding='utf-8')

count = 0
for line in f:
	
	pattern_end=re.compile('</S+')
	pattern_start=re.compile('<S+')
	pattern_root=re.compile('ROOT+')
	pattern_head=re.compile('H+')

	line = re.sub("\s+"," ",line)
	line_number += 1
	if(pattern_start.match(line)):
		line_number = 0
		sentence_id = line.split("'")[1]
		# print(sentence_id)


	elif(pattern_head.match(line)):
		line_state = []
		indx = 0
		line1 = line.split(";")
		line_state.insert(indx,line1[0].split(' ')[5])
		
		lst = line1[1].split(' ')
		if len( lst ) < 7 :
			line_number-=1
			continue

		line_state.insert(indx+1,line1[1].split(' ')[6])
		line_state.insert(indx+2,line1[2].split(' ')[1])
		line_state.insert(indx+3,line1[3].split(' ')[1])
		tags.insert(len(tags),line_state)

	elif(pattern_root.match(line)):
		line_state = get_line_state()
		tags.insert( len(tags), line_state)	

	elif(line_number == 8):
		indx = 0 
		buffer=[]
		line2 = line.strip().split(' ')
		for i in range(len(line2)):
		
			buffer.insert( len(buffer), line2[i])
		buffer.reverse()


	elif(pattern_end.match(line)):

		stack.insert(len(stack) , 'ROOT')
		flag = is_parsable()

		if(flag != 1):
			indx = len(not_parasble_sentences)
			not_parasble_sentences.insert(indx, sentence_id)
			count+=1
		else:
			a = 1
	
		flagki = 0	
		dependencies, tags, buffer, stack = [], [], [], []	

print(len(not_parasble_sentences))

# Save the list to a JSON file
with open('not_parasble_sentences_lst.json', 'w') as f:
    json.dump(not_parasble_sentences, f)

# with open('not_parasble_sentences_lst.json', 'r') as f:
#     NULL_index = json.load(f)

NULL_index = not_parasble_sentences
output_file = "after_clean.txt"

count = 0
flag = False

with open(input_file, "r", encoding='utf-8') as f_in, open(output_file, "w", encoding='utf-8') as f_out:
    for line in f_in:
        if line.rstrip():
            line = re.sub("\s+", " ", line)
            line1 = line.split(" ")

            if line1[0] == "<Sentence" and (line1[1].split('\'')[1] not in NULL_index):
                count += 1
                f_out.write(f"<Sentence id='{count}'>\n")
                flag = True

            elif line1[0].strip() == "</Sentence>" and flag:
                f_out.write("</Sentence>\n")
                flag = False

            elif flag:
                f_out.write(line)
                f_out.write("\n")
