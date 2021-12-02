import pandas as pd
pd.options.display.max_rows = 10


#Creando un dataframe a partir de un diccionario
#es importante notar que los valores son listas, si tuviera un solo valor sería una serie

frame_test = pd.DataFrame({1999: [1,2,3],
                           1998: [4,5,6],
                           1997: [7,8,9]})

print(frame_test)


#Dataframe a partir de listas

frame_test2 = pd.DataFrame([[1,2,3],
                           [4,5,6],
                           [7,8,9]])

print(frame_test2)

#incluir labels en las columnas

frame_test3 = pd.DataFrame([[1,2,3],
                           [4,5,6],
                           [7,8,9]], columns=["uno", "dos", "tres"])

print(frame_test3)