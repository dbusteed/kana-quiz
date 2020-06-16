# run from root directory
#   ex: python scripts/train_model.py

from sklearn.svm import SVC
from bidict import bidict
import joblib as jl
import csv

ENCODER = bidict({'A': 1,'I': 2,'U': 3,'E': 4,'O': 5,'KA': 6,'KI': 7,'KU': 8,'KE': 9,'KO': 10,'SA': 11,'SHI': 12,'SU': 13,'SE': 14,'SO': 15,'TA': 16,'CHI': 17,'TSU': 18,'TE': 19,'TO': 20,'NA': 21,'NI': 22,'NU': 23,'NE': 24,'NO': 25,'HA': 26,'HI': 27,'FU': 28,'HE': 29,'HO': 30,'MA': 31,'MI': 32,'MU': 33,'ME': 34,'MO': 35,'YA': 36,'YU': 37,'YO': 38,'RA': 39,'RI': 40,'RU': 41,'RE': 42,'RO': 43,'WA': 44,'WO': 45,'N': 46})

DATA_PATH = 'data.csv'

# get all the data
labels, features = [], []
with open(DATA_PATH) as file:
    reader = csv.reader(file)
    for row in reader:
        labels.append(ENCODER[row[0]])
        features.append( list(map(int, row[1:])) )

# build the model!
mdl = SVC(kernel='linear', C=.001)
mdl = mdl.fit(features, labels)

# save the model
jl.dump(mdl, 'kana.model')