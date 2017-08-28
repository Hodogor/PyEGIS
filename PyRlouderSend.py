# -*- coding: utf-8 -*-
# ~ Скрипт для проверки паспортных данных в направлениях 
# ~ на рег. регистр. 
# ~ Удаление повторных направлений
# ~ Author:      NikolayDp10
# ~ DateCreate:  2017-08-28


 # Создаем подключение к БД
import pyodbc
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.14.198.200;DATABASE=AKUZDB;UID=sa;PWD=Q!w2E#r4')


 # Получаем данные о новых направлениях и сохр. в переменную rows
cursor = cnxn.cursor()
cursor.execute("""
        SELECT [PatientBenefitsDirectionID]
            ,[Patient]
            ,[SNILS]
            ,[DocType]
            ,[DocSeries]
            ,[DocNumber] FROM  [AKUZDB].[dbo].[T_PATIENT_BENEFITS_DIRECTION] WHERE [Loaded]=0
          """)
rows = cursor.fetchall()

# Обрабатываем каждое направление
for row in rows:
    # Получаем идентификатор пациента
    PatientID = row[1]
    # Узнаем паспортные данные пациента из профиля
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.14.198.200;DATABASE=AKUZDB;UID=sa;PWD=Q!w2E#r4')
    cursor = cnxn.cursor()
    sql = "SELECT [DocSeries],[DocNumber], [SNILS], [DocType] FROM [AKUZDB].[dbo].[T_PATIENT] WHERE [PatientID]='"+PatientID +"'"
    cursor.execute(sql)
    patientDoc = cursor.fetchone()
    cnxn.commit()
    #Объявляем переменные
    DocSeries, DocNumber, SNILS, DocType = patientDoc  
    # Обновляем СНИЛС
    if SNILS != row[2]:
        cursor = cnxn.cursor()
        cursor.execute("UPDATE [T_PATIENT_BENEFITS_DIRECTION] SET [SNILS] = ? WHERE [PatientBenefitsDirectionID] = ?;", SNILS , row[0])
        cnxn.commit()
        print("Обновляю данные:"+SNILS + '=' +row[2])
        
    # Обновляем свидетельство
    if DocSeries != row[4] or DocNumber != row[5]:
        print("Обновляю данные:"+DocSeries + '=' +row[4]+' '+row[5])