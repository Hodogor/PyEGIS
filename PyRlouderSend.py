import pyodbc
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.14.198.200;DATABASE=AKUZDB;UID=sa;PWD=Q!w2E#r4')
    # Create a cursor from the connection
cursor = cnxn.cursor()
ex = """
/****** Проверка на наличие документов ******/

--объявляем переменные
declare @DirectionID varchar(250)
	   ,@Patient varchar(250)
	   ,@DocType varchar(250)
	   ,@DocSeries varchar(16)
	   ,@DocNumber varchar(16)
	   ,@NewDocNumber varchar(16)
	   ,@SNILS char(14)
	   ,@double int

--объявляем курсор
DECLARE my_cur CURSOR 
FOR 
SELECT [PatientBenefitsDirectionID]
	,[Patient]
	,[SNILS]
	,[DocType]
	,[DocSeries]
	,[DocNumber] FROM  [AKUZDB].[dbo].[T_PATIENT_BENEFITS_DIRECTION] WHERE [Loaded]=0

--открываем курсор
OPEN my_cur

--считываем данные первой строки в наши переменные
FETCH NEXT FROM my_cur INTO @DirectionID, @Patient, @SNILS,@DocType,@DocSeries,@DocNumber

--если данные в курсоре есть, то заходим в цикл
--и крутимся там до тех пор, пока не закончатся строки в курсоре
WHILE @@FETCH_STATUS = 0
BEGIN
	--на каждую итерацию цикла запускаем нашу основную процедуру с нужными параметрами   
	SELECT @DocSeries=[DocSeries] 
      , @DocNumber=[DocNumber]
      , @SNILS=[SNILS]
      , @DocType=[DocType]
       FROM [AKUZDB].[dbo].[T_PATIENT]
	WHERE [PatientID]= @Patient
	
	
	
	-- удаляем направления без документов
	if @DocNumber is NULL OR @DocSeries is NULL
		Begin
			PRINT 'Нет документов';
			-- удаляем льготу
			Delete 
			From [T_PATIENT_BENEFITS_DIRECTION_DATA]
			where
				T_PATIENT_BENEFITS_DIRECTION_DATA.PatientBenefitsDirection = @DirectionID;
			-- удаляем направление
			Delete 
			From [T_PATIENT_BENEFITS_DIRECTION]
			where
				T_PATIENT_BENEFITS_DIRECTION.PatientBenefitsDirectionID = @DirectionID;
		End
		
	-- удаляем направления если есть дубль 
	SELECT @double = Count([T_PATIENT_BENEFITS_DIRECTION].[Patient]) FROM  [AKUZDB].[dbo].[T_PATIENT_BENEFITS_DIRECTION] WHERE [Loaded]=0 AND [Patient]=@Patient
	PRINT @double;
	if @double <> 1
		Begin
			PRINT 'дубль';
			-- удаляем льготу
			Delete 
			From [T_PATIENT_BENEFITS_DIRECTION_DATA]
			where
				T_PATIENT_BENEFITS_DIRECTION_DATA.PatientBenefitsDirection = @DirectionID;
			-- удаляем направление
			Delete 
			From [T_PATIENT_BENEFITS_DIRECTION]
			where
				T_PATIENT_BENEFITS_DIRECTION.PatientBenefitsDirectionID = @DirectionID;
		End
	
	--считываем следующую строку курсора
	FETCH NEXT FROM my_cur INTO @DirectionID,@Patient, @SNILS,@DocType,@DocSeries,@DocNumber
END
--закрываем курсор
CLOSE my_cur
DEALLOCATE my_cur
    """
   
cursor.execute(ex)