import re
import pandas as pd


"""====== DEF DEF DEF DEF DEF DEF DEF =====================
Библиотека функций

*** printAndType(val) ***   - Функция для отладочной печати любого объекта 
1-я строка тип элемента, например, series, DataFraime итд
2-я строка - собственно объект
Можно в одной строке записать, но когда объект например, матрица, красиво не получается:
  print('type(df),df)        - первая строка сдвигается вправо на длину вывода type()
  print('type(df),'\n',df)   - строка переводится, но 1-я строчка таблицы на один пробел все же сдвигается
--------------------------------------------------------------------------------------
def printAndType(val,comment='---'):
    print(comment,type(val))
    print(val)
"""
def printAndType(val,comment='---',prShape=False):
    if prShape==True: 
        s = ', shape'+str(val.shape)
    else:
        s = ''
    print(comment,type(val),s)
    print(val)


# =============== Доработки ===============
#   - добавить тег для value. Если нет то значение не выводится (или по умолчанию выводить) 
#   - указывать перевод строки там где надо. Если нет,  то вообще вывод в одну строку
#   не хочется делать через key=true. Понятно, стандарт, но слишком длинно
#  Попробовать все же набирать строку ключей, вывод в порядке набора, вставка перевода строки и флага отключения флага
# Доальше можно копировать понравившуюся строку чуть корректируя. А полный список флагов в примере где объявляется метод
#
#

#-------------------** def printMy **--------------------------
def printMy(value,comment='****',reOptions=''):
    # sOptions - строка из которой нужно выделить опции вывода
    #   \n    print()   - пустая строка
    #   t    - type(val) - вывод типа value
    #   len  - len(val) - вывод длины
    #   sh   - shape(val) - вывод размера
    #----------------------------------------------------------
    # создаем DataFrame с опциями   
    # столбцы - Name, pattern, Res для каждой опции
    data=[['Line',r'[ ]ln',False],   # 0
          ['Type',r'[ ]t',False],    # 1
          ['Len',r'[ ]len',False],   # 2
          ['Shape',r'[ ]sh',False],  # 3
          ['Info',r'[ ]inf',False]]  # 4
#
# Модуль получился довольно объемным. Возможно ужмется, когда лучше освою разную оптимизацию.
# reOptions задаю при вызове в виде:
# '.ln.t.sh.len.inf'     - где перечислены опции через точку. В таком виде все опции отключены!
# Чтобы включить опцию нужно вставить пробел между точкой и опцией. Точки ни какой роли не играют
# они служат для визуального разделения опций. Кстати, можно через слэш или еще какой символ
# Для парсинга использую re.search(). Пока показалось проще чем re.match(). Дальше, посмотрю.
# Функции возвращают объект match или None, который можно проверить через if. Но когда передавал в ячейку 
# dfKeys.loc[ind,'Res'] , то None превращался в NaN и это кошмар, т.к. с этим типом вообще пока ничего не возможно делать.
# Поэтому после парсинга сразу проверяю результат и превращаю в True/False , которые и заношу dfKeys.loc[ind,'Res'].
# Проверку парсинга выполняю через sheckOp(aOptName). Правда имена индексов не работают и приходится писать индексы
# Все это растягивает код и не добавляет прозрачности и читаемости. Но пока так.
#------------------------------------------------------------------------------------
# Думал добовить флаг head чтобы задавать укороченный вывод. Т.к. если передаю фрейм с .head(), то 
# по флагу shape размер фрейма показывает с учетом head(), а не реальный. Но это не самое страшное несоответствие.
# Думаю в заблуждение не часто буду попадать.
#
#

    
    dfKeys = pd.DataFrame(data,columns=['Name','Pat','Res'])
    dfKeys.set_index('Name')   # Выносим столбец 'Name' в индексы
    #printMyN(dfKeys,'dfKeys:')  # проверка до парсинга

    #-------------------------------------
    def sheckOp(aOptName):
        if dfKeys.loc[aOptName,'Res']:
            return True
        else:
            return False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    for ind in dfKeys.index:    # парсинг опций в строке
        rem = re.search(dfKeys.Pat[ind],reOptions)
        if rem:
            dfKeys.loc[ind,'Res'] = True  
        else:
            dfKeys.loc[ind,'Res'] = False
  
    #print('reOptions:',reOptions)
    #printMyN(dfKeys)  # проверка парсинга
#    printMyN(dfKeys,'dfKeys:')  # проверка парсинга
    
    # обработка флагов(опций)
    sType=''
    sShape=''
    sLen=''
    if sheckOp(0):
        print()
    if sheckOp(1):
        sType=type(value)
    if sheckOp(2):
        sLen= 'len= '+str(len(value))
    if sheckOp(3):
        sShape=value.shape
    print(comment,sShape,sLen,sType)
    print(value)
    if sheckOp(4):
        print()
        value.info()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#printMy(dfSstSort,'dfSstSort','. ln.t. sh.len.inf')
