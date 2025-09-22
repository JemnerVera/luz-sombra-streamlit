from sklearn.metrics import classification_report

def evaluar_modelo(modelo, X_test, y_test):
    y_pred = modelo.predict(X_test)
    return classification_report(y_test, y_pred)