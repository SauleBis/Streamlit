import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
tips = pd.read_csv(path)
random_dates = pd.date_range(start='2023-01-01', end='2023-01-31', periods=244)
tips['time_order'] = random_dates.strftime('%Y-%m-%d %H:%M')


st.title("Исследование по чаевым")
st.header('Данные за месяц')
st.write("Все данные взяты из этого dataframe")
st.dataframe(tips)


#Сайдбар для фильтрации данных 
st.sidebar.header('Выбор параметров для фильтрации')
st.sidebar.write("При выборе параметков графики будут изменены с учетом фильтрации")
gender = st.sidebar.selectbox('Пол',['All'] + list(tips['sex'].unique()))     #Добавила условие 'All', чтобы по умолчанию показывались все данные
day_of_week = st.sidebar.selectbox('День недели', ['All'] + list(tips['day'].unique()))
smoker = st.sidebar.selectbox('Курящих/нет', ['All'] + list(tips['smoker'].unique()))
size = st.sidebar.selectbox('Кол-во человек', ['All'] + list(tips['size'].unique()))
st.sidebar.write("В DataFrame доступны данные только на период 1-31 января 2023 года")
start_period = st.sidebar.date_input('Выберите начало периода')   #не получилось задать значение по умолчанию 1 янв.2023, поэтому по умолчанию текущий день => графики пустые
end_period = st.sidebar.date_input('Выберите конец периода')
start_period = start_period.strftime('%Y-%m-%d')
end_period = end_period.strftime('%Y-%m-%d')

#применение фильтрации к исходным данным для того, чтобы графики менялись под фильтры
tips_filter = tips.copy()
if gender != 'All':
    tips_filter = tips_filter[tips_filter['sex'] == gender]
if day_of_week != 'All':
   tips_filter = tips_filter[tips_filter['day'] == day_of_week]
if smoker != 'All':
    tips_filter = tips_filter[tips_filter['smoker'] == smoker]    
if size != 'All':
    tips_filter = tips_filter[tips_filter['size'] == size]
if start_period and end_period:
    tips_filter = tips_filter[(tips_filter['time_order'] >= start_period) & (tips_filter['time_order'] <= end_period)]
else:
    st.write("Данные отсутствуют. Выберите другой период")



st.header('Визуализация данных')
st.subheader('Динамика чаевых')
st.line_chart(data=tips_filter, x='time_order', y='tip')



st.subheader('Сумма чека')
bills = sns.displot(data=tips_filter, x='total_bill', kind='hist')
st.pyplot(bills)




st.subheader('Зависимость чаевых от суммы чека')
st.scatter_chart(data=tips_filter, x='total_bill', y='tip')