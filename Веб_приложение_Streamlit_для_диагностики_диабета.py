# https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

import streamlit as st 
import pandas as pd 
from sklearn.metrics import accuracy_score 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split 

df = pd.read_csv('diabetes.csv')

st.title('Определение наличия диабета')
st.write(df.head())
st.subheader('Информация о датасете')
st.write(df.describe())

st.subheader('Визуализация')
st.bar_chart(df)

x = df.drop(['Outcome'], axis=1)  # axis=1 - столбец
y = df.iloc[:, -1]  # выбираем последний столбец, диагноз

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=0, shuffle=True)

def userreport():
    # ввод pregnancies, glucose с помощью ползунков
    pregnancies = st.sidebar.slider('Перенесённых беременностей', 0, 10, 0)
    glucose = st.sidebar.slider('Уровень глюкозы', 0, 200, 120)
    bp = st.sidebar.slider('Давление', 0, 122, 70)
    skinthickness = st.sidebar.slider('Толщина кожи', 0, 100, 20)
    insulin = st.sidebar.slider('Уровень инсулина', 0, 846, 79)
    bmi = st.sidebar.slider('Индекс массы тела', 0, 67, 20)
    dpf = st.sidebar.slider('Наследственность', 0.0, 2.4, 0.27)
    age = st.sidebar.slider('Возраст', 21, 88, 33)

    # сбор введённых значений в словарь
    report = {
        'Pregnancies' : pregnancies,
        'Glucose' : glucose, 
        'BloodPressure' : bp, 
        'SkinThickness' : skinthickness, 
        'Insulin' : insulin, 
        'BMI' : bmi, 
        'DiabetesPedigreeFunction' : dpf, 
        'Age' : age
    }

    report = pd.DataFrame(report, index=[0])  # DataFrame будет иметь 1 строку с индексом 0
    return report    


userdata = userreport()

rf = RandomForestClassifier()
rf.fit(xtrain, ytrain)

st.subheader('Точность: ')
# сравниваем полученные диагнозы с реальными
st.write(str(accuracy_score(ytest, rf.predict(xtest)) * 100) + '%')

userresult = rf.predict(userdata)  # передаём параметры, определяем наличие диабета
st.subheader('Диагноз: ')
if userresult[0] == 0:
    output = 'Диабета не обнаружено'
else:
    output = 'Обнаружен диабет'


st.write(output)



