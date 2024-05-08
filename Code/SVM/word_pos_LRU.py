import json
import re
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report


def feature_transform(train_file, words, tags, words_len, tags_len):

    row_idx = []
    column_idx = []
    ctr = 0
    data = []
    feature_length = words_len + tags_len # Per head
    y = []
    f = open(train_file, encoding='utf-8')

    for line in f:
        ctr += 1

        if(line.rstrip()):
            
            line = re.sub("\s+"," ",line)
            line1 = line.split(";")

            a3 = line1[2].split(" ")
            a2 = line1[1].split(" ")
            a1 = line1[0].split(" ")
            y.append(a3[1])

            row_idx += [ctr-1]*4
            data += [1] *4

            if(a1[0] == "ROOT"):
                column_idx.append(words.index("ROOT"))
                column_idx.append(tags.index("ROOT") + words_len)
                
            elif(a1[0] == "H"):
                column_idx.append(words.index(a1[1]))
                column_idx.append(tags.index(a1[4]) + words_len)
                
            column_idx.append(feature_length + words.index(a2[2]))
            column_idx.append(feature_length + tags.index(a2[5]) + words_len)
    
    f.close()
    X = csr_matrix((data, (row_idx, column_idx)), shape=(ctr,2*(words_len+tags_len)))
    return X, y

listfile = "..\\training_preprocessing\\data_lists.json"
f = open(listfile, encoding='utf-8')
data = json.load(f)
f.close()

words = data["words"]
tags = data["tags"]

train_file = '..\\training_preprocessing\\parsed_output.txt'
test_file = "..\\testing_preprocessing\\parsed_output.txt"

words_len = len(words)
tags_len = len(tags)

model = LinearSVC()
X_train, y_train = feature_transform(train_file, words, tags, words_len, tags_len)
model.fit(X_train, y_train)
pred_train = model.predict(X_train)
print(classification_report(y_train, pred_train))

X_test, y_test = feature_transform(test_file, words, tags, words_len, tags_len)
pred_test = model.predict(X_test)
print(classification_report(y_test, pred_test))