from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size=0.7)

X_train = X_train[:, :2]
X_test = X_test[:, :2]

log_reg = LogisticRegression(random_state=0).fit(X_train, y_train)
log_reg.coef_
log_reg.intercept_