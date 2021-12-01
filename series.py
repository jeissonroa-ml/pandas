import pandas as pd

#Serie con una lista, lo cual crea un índice

series_test = pd.Series([100, 200, 300])

#print(series_test)

#Serie con un diccionario, en el cual los indices son los mismo labels

series2 = pd.Series({"Nombre": "Jeisson",
                     "Nombre2": "Alfonso",
                     "Apellido": "Roa"})

print(series2)


#Series con tipo de dato

series_test3 = pd.Series([100,200,300],dtype=float)

#insertando los indices

series_test4 = pd.Series([11,13,17,19],
                index = ['a','b','c','d'])