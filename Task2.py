import matplotlib
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt


df = pd.read_excel(r'training.xlsx')
print("Null Data before preprocessing \n" + str(df.isnull().sum()))

# Change ClassLabel to bool
df.classLabel = df.classLabel.replace(['yes.'], 1)
df.classLabel = df.classLabel.replace(['no.'], 0)

# Drop some NAs
df = df.dropna(subset=['variable4', 'variable5', 'variable6', 'variable7'], how='any')

# Drop var19 because it is not useful and a bit confusing data
df = df.drop('variable19', axis=1)

# Convert T&F to Binary
BinaryCols = ['variable1', 'variable9', 'variable10', 'variable12', 'variable18']
for c in BinaryCols:
    df[c] = df[c].replace(['a', 't'], 1)
    df[c] = df[c].replace(['b', 'f'], 0)
    if(df[c].isna().sum()>0):
        df[c+'na'] = df[c].fillna(1)
        df[c] = df[c].fillna(0)


# Convert Multiple class to Binary Cols
MultipleCols = ['variable4', 'variable5', 'variable6', 'variable7', 'variable13']
for c in MultipleCols:
    UniqueVals = df[c].unique()
    # print(UniqueVals)
    for c2 in UniqueVals:
        NewCol = df[c]
        NewColName = c+c2
        df[NewColName] = NewCol
        df[NewColName] = df[NewColName].replace([c2], 1)
    df = df.drop(c, axis=1)

# Split Cols by Comma
CommaCols = ['variable2', 'variable3', 'variable8']
for c in CommaCols:
    df[c + '_1'] = df[c].str.extract('(\d*\,)', expand=True)
    df[c + '_2'] = df[c].str.extract('(,\d*)', expand=True)
    df[c + '_1'] = df[c + '_1'].fillna((df[c]))
    df[c + '_2'] = df[c + '_2'].fillna((df[c]))
    df = df.drop(c, axis=1)
df = df.replace(',', '', regex=True)

# Cal Avg for some NAs
AvgCols = ['variable2_1', 'variable2_2', 'variable3_1', 'variable3_2', 'variable8_1', 'variable8_2', 'variable14', 'variable15', 'variable17']
for c in AvgCols:
    df[c] = df[c].astype(float)
    avg = df[c].dropna().mean()
    df[c] = df[c].fillna(avg)
df = df.replace('(\w*)', 0, regex=True)

print("Null Data after preprocessing \n" + str(df.isnull().sum()))
plt.scatter(df.variable1, df.classLabel, marker='+', color='red')

ColNames = []
classlabel = 0
for c in df.columns:
    if(c == 'classLabel'):
        classlabel = df[c]
    else:
        ColNames.append(c)

X_train, X_test, Y_train, Y_test = train_test_split(df[ColNames], classlabel, test_size=0.1)
model = LogisticRegression()
model.fit(X_train, Y_train)
model.predict(X_test)
print(model.score(X_test, Y_test))
model.predict_proba(X_test)

with open("trainingColNames.txt", "wb") as myFile:
    pickle.dump(ColNames, myFile)

myDictionary = {}

with open('trainingColNames.txt', 'rb') as dict_items_open:
    myDictionary = pickle.load(dict_items_open)

