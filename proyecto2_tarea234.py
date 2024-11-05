# -*- coding: utf-8 -*-
"""Proyecto2_Tarea234.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f2DfzXWevswrW8EotNoJkZqM0v6MuK6X

# Analítica computacional para la toma de decisiones
## Proyecto 1
## Tarea 2 - Limpieza y alistamiento de datos

### Importar librerías
"""

import pandas as pd
import numpy as np

"""### Importar dataset"""

df = pd.read_csv('bank-full.csv', delimiter=";")
df.head()

"""### reemplazar los valores de Unknown por N/A"""

df = df.dropna()  # Elimina filas con valores vacíos (NaN)

# Verificar que no haya vacíos en las columnas del dataset, se imprime False si es así y True de lo contrario
for i in df.columns:
    print(i + " " + str(df[i].isin([None]).any()))

"""### Transformar el valor -1 en la columna 'pdays' a 'No contactado'"""

df['pdays'] = df['pdays'].replace(-1, 0)
print(df)

"""### Verificar si hay duplicados"""

# Número de datos duplicados
duplicates = len(df[df.duplicated()])
print(f'Number of Duplicate Entries: {duplicates}')
df.shape

"""### Codificar las columnas binarias (Categoricas)"""

binary_columns = ['default', 'housing', 'loan', 'y']
df[binary_columns] = df[binary_columns].applymap(lambda x: 1 if x == 'yes' else 0)
print(df)

import pandas as pd

# Crear la columna binaria inicializada en 0
df["marital (bin)"] = 0

# Asignar 1 a las filas donde 'poutcome' es 'success'
df.loc[df["marital"] == "married", "marital (bin)"] = 1

df.head()

contact_column = ['contact']
df[contact_column] = df[contact_column].applymap(lambda x: 1 if x == 'telephone' else 0)

df = df[df['month'].notna()]

# Diccionario de mapeo de meses a números
month_map = {
    'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
}

# Reemplazar los nombres de los meses con sus valores numéricos
df['month'] = df['month'].map(month_map)

# Crear un diccionario de mapeo único para cada trabajo
job_map = {job: idx for idx, job in enumerate(df["job"].unique(), start=1)}

# Mostrar el mapeo de cada trabajo con su número asignado
print("Asignación de números para cada trabajo:")
for job, num in job_map.items():
    print(f"{job}: {num}")

# Asignar el número único a cada trabajo en una nueva columna
df["job_id"] = df["job"].map(job_map)

import pandas as pd

# Crear la columna binaria inicializada en 0
df["education (bin)"] = 0

# Asignar 1 a las filas donde 'poutcome' es 'success'
df.loc[df["education"] == "tertiary", "education (bin)"] = 1

df.head()

import pandas as pd



df.head()

df = df.drop("poutcome", axis=1)
df.head()
df.shape

df = df.drop("job", axis=1)
df.head()
df.shape

df = df.drop("marital", axis=1)
df.head()
df.shape

df = df.drop("education", axis=1)
df.head()
df.shape

df

"""# Tarea 3 - Exploracion de datos

### Estadisticas descriptivas
"""

import seaborn as sns
import matplotlib.pyplot as plt

df.describe()

descriptive_stats_all = df.describe(include='all')
print(descriptive_stats_all)

"""## Correlacion"""

import seaborn as sb
plt.figure(figsize=(10, 8))
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Heatmap of Correlations')
plt.show()

sns.pairplot(df.select_dtypes(include=['float64', 'int64']))
plt.show()

"""## Histograma para cada variable"""

for column in df.select_dtypes(include=['float64', 'int64']).columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df[column], kde=True)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

"""## Boxplots"""

for column in df.select_dtypes(include=['float64', 'int64']).columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, y=column)
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
    plt.show()

"""## Diagramas de dispersion"""

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='age', y='balance')
plt.title('Scatter Plot of Age vs Balance')
plt.xlabel('Age')
plt.ylabel('Balance')
plt.show()

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='duration', y='campaign')
plt.title('Scatter Plot of Duration vs Campaign')
plt.xlabel('Duration')
plt.ylabel('Campaign')
plt.show()

"""## Diagramas de violin"""

plt.figure(figsize=(12, 8))
sns.violinplot(data=df, x='job_id', y='balance')
plt.xticks(rotation=90)
plt.title('Violin Plot of Balance by Job')
plt.xlabel('Job')
plt.ylabel('Balance')
plt.show()

"""# Punto 4"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import statsmodels.api as sm

features = ['age', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'marital (bin)', 'job_id', 'education (bin)', 'poutcome (bin)']
X=df[features]

Y=df['y']

types = df.dtypes.value_counts()
print(types)

# Reemplazar infinitos por NaN y eliminar cualquier valor faltante
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Verificar que no haya valores faltantes o infinitos en el DataFrame completo
print("Valores faltantes después de la limpieza:")
print(df.isnull().sum().sum())  # Debería ser 0 si no hay valores NaN
print("Valores infinitos después de la limpieza:")
print(np.isinf(df.values).sum())  # Debería ser 0 si no hay infinitos

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=1)

# Eliminar filas con valores NaN
X_train = X_train.dropna()
y_train = y_train.loc[X_train.index]  # Asegúrate de que y_train tenga los mismos índices

from statsmodels.stats.stattools import durbin_watson

# Agregar constante explíticamente
X_train = sm.add_constant(X_train)

# Regresión usando mínimos cuadrados ordinarios (ordinary least squares - OLS)
model = sm.OLS(y_train, X_train).fit()

# Resumen de resultados
print(model.summary())

# Estadístico Durbin-Watson
dw_statistic = durbin_watson(model.resid)
print("\nEstadístico de Durbin-Watson:" + str(dw_statistic))

"""Se quitan las variables no significativas"""

features1 = ['balance', 'housing', 'loan', 'contact', 'duration', 'campaign', 'pdays', 'previous', 'marital (bin)', 'job_id', 'education (bin)', 'poutcome (bin)']
X1=df[features1]
Y1 =df['y']

X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, Y1, test_size=0.2, random_state=42)

X_train1.shape, X_test1.shape, y_train1.shape, y_test1.shape

# Agregar constante explíticamente
X_train1 = sm.add_constant(X_train1)

# Regresión usando mínimos cuadrados ordinarios (ordinary least squares - OLS)
model = sm.OLS(y_train1, X_train1).fit()

# Resumen de resultados
print(model.summary())

# Estadístico Durbin-Watson
dw_statistic = durbin_watson(model.resid)
print("\nEstadístico de Durbin-Watson:" + str(dw_statistic))

"""### Modelo de redes neuronales con variables significativas"""

# Crear el modelo base
model_base = Sequential([
    Dense(64, activation='relu', input_shape=(X_train1.shape[1],)),
    Dense(64, activation='relu'),
    Dense(1)  # Salida para regresión
])

# Compilar el modelo
model_base.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenar el modelo
history_base = model_base.fit(X_train1, y_train1, epochs=100, validation_split=0.2, verbose=0)

model_base.summary()

# Graficar historial
plt.figure(figsize=(12, 6))
plt.plot(history_base.history['loss'], label='Pérdida de entrenamiento')
plt.plot(history_base.history['val_loss'], label='Pérdida de validación')
plt.title('Historial de pérdida del modelo base')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.show()

# Crear modelo con 32 neuronas (mitad del modelo base)
model32 = Sequential([
    Dense(32, activation='relu', input_shape=(X_train1.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1)  # Salida para regresión
])

# Compilar el modelo
model32.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenar el modelo
history32 = model32.fit(X_train1, y_train1, epochs=100, validation_split=0.2, verbose=0)

# Crear modelo con 128 neuronas (doble del modelo base)
model128 = Sequential([
    Dense(128, activation='relu', input_shape=(X_train1.shape[1],)),
    Dense(128, activation='relu'),
    Dense(1)  # Salida para regresión
])

# Compilar el modelo
model128.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenar el modelo
history128 = model128.fit(X_train1, y_train1, epochs=100, validation_split=0.2, verbose=0)

res = {32: history32, 64: history_base, 128: history128}
# Graficar resultados
plt.figure(figsize=(12, 6))
for n, history in res.items():
    plt.plot(history.history['val_loss'], label=f'{n} Neuronas')
plt.title('Comparación de Modelos con Diferente Número de Neuronas')
plt.xlabel('Épocas')
plt.ylabel('Pérdida de Validación')
plt.legend()
plt.show()

"""El modelo tendrá 64 neuronas debido a que se estabiliza más rápido

### Diferentes capas
"""

# Función para crear y entrenar un modelo con una cantidad variable de capas ocultas
def crear_entrenar(layers_configuration):
    # Crear la red neuronal con la configuración de capas especificada
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(X_train1.shape[1],)))

    # Añadir capas ocultas adicionales según la configuración dada
    for neurons in layers_configuration:
        model.add(Dense(neurons, activation='relu'))

    model.add(Dense(1))  # Capa de salida para regresión

    # Compilar el modelo
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Entrenar el modelo
    history = model.fit(X_train1, y_train1, epochs=100, validation_split=0.2, verbose=1)

    # Evaluar el modelo
    loss, mae = model.evaluate(X_test1, y_test1)

    return history, loss, mae

configs = [
    [32],               # Configuración 1: 1 capa oculta
    [32, 64],           # Configuración 2: 2 capas ocultas
    [32, 64, 128]       # Configuración 3: 3 capas ocultas
]

# Diccionarios para almacenar los resultados de cada configuración
his = {}
losses = {}
maes = {}

# Entrenar y evaluar los modelos para cada configuración
for idx, config in enumerate(configs):
    print(f"\nEntrenando modelo con {len(config)} capas ocultas: {config} neuronas...")
    history, loss, mae = crear_entrenar(config)
    his[idx] = history
    losses[idx] = loss
    maes[idx] = mae

# Graficar la historia de la pérdida para cada configuración
plt.figure(figsize=(10,6))
for idx, config in enumerate(configs):
    plt.plot(his[idx].history['val_loss'], label=f'Validación - {len(config)} capas ocultas')
plt.title('Historial de Pérdida en la Validación para Diferentes Configuraciones de Capas')
plt.xlabel('Épocas')
plt.ylabel('Pérdida (MSE)')
plt.legend()
plt.grid(True)
plt.show()

"""El modelo tendrá 3 capas ocultas debido a que se estabiliza más rápido

### Comparación con el modelo base
"""

# Primer modelo
model1 = Sequential([
        Dense(32, activation='tanh', input_shape=(X_train1.shape[1],)),
        Dense(64, activation='tanh'),
        Dense(1)
    ])

# Compilación
model1.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenamiento
history1 = model1.fit(X_train1, y_train1, epochs=100, validation_split=0.2, verbose=0)

# Segundo modelo
model2 = Sequential([
        Dense(128, activation='tanh', input_shape=(X_train1.shape[1],)),
        Dense(64, activation='tanh'),
        Dense(32, activation='tanh'),
        Dense(1)
    ])

# Compilación
model2.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenamiento
history2 = model2.fit(X_train1, y_train1, epochs=100, validation_split=0.2, verbose=0)

res = {0: history_base, 1: history1, 2: history2}
# Graficar resultados
plt.figure(figsize=(12, 6))
for n, history in res.items():
    plt.plot(history.history['val_loss'], label=f'{n} Modelo')
plt.title('Comparación de Modelos propuestos con Base')
plt.xlabel('Épocas')
plt.ylabel('Pérdida de Validación')
plt.legend()
plt.show()

"""El modelo elegido es el #2. El cual tiene 3 capas ocultas de [32, 64, 128], activación 'tanh', optimizador 'adam' y métrica 'mae'."""