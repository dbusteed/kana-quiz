# run from root directory
#   ex: python scripts/model_testing.py

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import csv

ENCODER = {'A': 1,'I': 2,'U': 3,'E': 4,'O': 5,'KA': 6,'KI': 7,'KU': 8,'KE': 9,'KO': 10,'SA': 11,'SHI': 12,'SU': 13,'SE': 14,'SO': 15,'TA': 16,'CHI': 17,'TSU': 18,'TE': 19,'TO': 20,'NA': 21,'NI': 22,'NU': 23,'NE': 24,'NO': 25,'HA': 26,'HI': 27,'FU': 28,'HE': 29,'HO': 30,'MA': 31,'MI': 32,'MU': 33,'ME': 34,'MO': 35,'YA': 36,'YU': 37,'YO': 38,'RA': 39,'RI': 40,'RU': 41,'RE': 42,'RO': 43,'WA': 44,'WO': 45,'N': 46}

X = []
y = []

with open('data.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        y.append(ENCODER[row[0]])
        X.append( list(map(int, row[1:])) )
        
X_train, X_test, y_train, y_test = train_test_split(X, y)

## hyper parameter tuning

# grid = {'C': [.001, .01, .1, 1], 'kernel': ['linear']}
# cv = GridSearchCV(SVC(), grid, cv=5)

# cv.fit(X_train, y_train)
# cv.best_estimator_.score(X_test, y_test)
# cv.best_estimator

mdl = SVC(kernel='linear', C=.001)
mdl.fit(X_train, y_train)

score = mdl.score(X_test, y_test)

print(f"score: {score}")

# score: 0.8878504672897196
