import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
fname = 'featurevector.csv'
# data = np.genfromtxt(fname, delimiter=",", dtype=None)
# data = np.genfromtxt(fname, delimiter=",", dtype=None, skip_header=1)


df = pd.read_csv('featurevector.csv')
array = df.values
X = array[:, :24]
y = array[:, 24]


# clf = DecisionTreeClassifier()
# clf = clf.fit(X, y)
# print(clf.predict([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
# 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0]))
k_range = list(range(1, 26))
score = []
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=4)
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    score.append(accuracy_score(y_pred, y_test))

plt.plot(k_range, score)
plt.xlabel('Value of K for KNN')
plt.ylabel('Testing Accuracy')
plt.show()
