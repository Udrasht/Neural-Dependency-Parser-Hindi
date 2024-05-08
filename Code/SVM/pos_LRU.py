import json
import re
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

def feature_transform( train_file, tags, tags_len ):
    row_idx = []
    column_idx = []
    tags_len = len(tags)
    data = []
    y = []
    feature_length = tags_len # Per head
    ctr = 0
    f = open(train_file, encoding='utf-8')

    for line in f:
        ctr += 1
        if(line.rstrip()):
            line = re.sub("\s+"," ",line)
            line1 = line.split(";")

            row_idx += [ctr-1]*2
            data += [1] * 2

            a3 = line1[2].split(" ")
            a2 = line1[1].split(" ")
            a1 = line1[0].split(" ")
            y.append(a3[1])

            if(a1[0] == "ROOT"):
                column_idx.append(tags.index("ROOT"))

            elif(a1[0] == "H"):
                column_idx.append(tags.index(a1[4]))
            
            column_idx.append(feature_length + tags.index(a2[5]))

    f.close()
    X = csr_matrix((data, (row_idx, column_idx)), shape=(ctr,2*(tags_len)))
    return X, y


listfile = "..\\training_preprocessing\\data_lists.json"
f = open(listfile, encoding='utf-8')
data = json.load(f)
f.close()

tags = data["tags"]

train_file = '..\\training_preprocessing\\parsed_output.txt'
test_file = "..\\testing_preprocessing\\parsed_output.txt"

tags_len = len(tags)

model = LinearSVC()
X_train, y_train = feature_transform( train_file, tags, tags_len )
model.fit(X_train, y_train)
pred_train = model.predict(X_train)
print(classification_report(y_train, pred_train))

X_test, y_test = feature_transform( test_file, tags, tags_len )
pred_test = model.predict(X_test)
print(classification_report(y_test, pred_test))

