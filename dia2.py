# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:32:36 2020

@author: Rafael
Clube do Cientista
Curso Python

código disponível em:
https://github.com/clubedocientista/IdacoNave_intro_Python/
"""

####################  Idaco ~ Nave do Conhecimento
###############       Seminário Python
##########            Introdução a Data Mining
#### Data Estruturados      -> https://ourworldindata.org/coronavirus-source-data
#### Dados não estruturados -> https://forms.gle/ML73NsX4zc2c17WZ9

import numpy as np
import pandas as pd

### listas, dataframes e operações simples
lista1 = [1,2,3,4,5]               # lista de int
lista1
lista1 = np.arange(1,6,1)
lista1
lista2 = [[1,2,3,4,5],[5,4,3,2,1]] # lista de listas
lista2

print (lista1[1])                  # posição 1
print (lista1[-1])                 # última posição
print (lista2[1][2])               # posição 2 do item 1
print (lista1[0:2])                # intervalo de posições

# boolean
a = True
print (a)
type (a)                           # bool  = True or False

# operações
type (lista1)    == int            # é igual a 
type (lista1[1]) != float          # é diferente de 

lista1[0:-1:2]                     # primeiro ao ultimo a cada dois 
lista1[lista1>2]
lista1>2
lista1
lista1[(lista1>=2) & (lista1<4)]   # condição E
lista1[(lista1>=4) | (lista1<2)]   # condição OU

# dataframes (tabelas)
lista1 = np.random.randint(low = 3, high = 30, size = 100)
lista1 # vetor aleatório com 100 números inteiros de 3 a 30
lista2 = np.random.randint(low = 1, high = 360, size = 100)
lista2 # vetor aleatório com 100 números inteiros de 1 a 360
 
pd.Series(lista2)               # formato Series (~coluna)
df = pd.concat([pd.Series(lista1), pd.Series(lista2)], axis = 1)
# axis = 1 --> para colunas
df
df.columns = ['Var1','Var2']    # renomeia colunas do dataframe
df.head()                       # retorna as 5 primeiras linhas

# apagando df
whos
del df
whos

# outra forma de criar DataFrame, baseado em dicionário (dict)
df_dict = {'Var1': lista1, 'Var2': lista2}
df      = pd.DataFrame(df_dict)
type(df_dict)

df['Var1'].head()  # retorna as 5 primeiras linhas da coluna Var1
len(df)            # retorna a quantidade de linhas do dataframe
len(df.columns)    # retorna a quantidade de colunas do dataframe
df.shape           # retorna as dimensões do dataframe
df.loc[2,]         # retorna todos os dados da terceira linha
df.Var2            # retorna todos os dados da coluna Var2
df.loc[1,'Var2']   # retorna o valor da segunda linha da coluna Var2

df['Var3'] = df['Var1']*np.sqrt(df['Var2'])
df['Var3'].head()

df.to_csv('minha_tabela.csv', sep = ';')


### condicionais e repetição

# if
if type (df) == float: # se tipo de 'df' é float
    print ('df é uma variável do tipo float') 
elif type(df) == bool: # ou se tipo de 'df' é bool
    print ('df é uma variável do tipo bool') 
else:                  
    print ('df não é uma variável float nem bool')

# while
nomes = []
c     = 0
while c < 5: 
    nomes.append (input ('Qual seu nome:'))
    c = c + 1
print(nomes)

# for   
n = np.arange(10)
for i in n:     # para cada elemento (i) em n 
    print (i)   # imprimir o elemento (i)

# for + if
n = df['Var1']
print (n)
r = []
for j in n:
    if j < 10:
        r.append(j)
print(r)       # r = valores em n menores do que 10
print (len(r))

# exempplo compacto: for e if em uma linha
del r
r = [i for i in n if i < 10]  
print (len(r))

#ou
del r
r = n[n<10]  
print (len(r))    


# lendo dados COVID
# https://ourworldindata.org/coronavirus-source-data

# abrindo e verificando DataFrame    
import xlrd
from os import chdir
chdir ('D:\\Documentos\\Clube do Cientista\\cursos\\Python_IdacoNave')
df_covid  = pd.read_excel('owid-covid-data.xlsx', sheet_name = 'Sheet1')
df_covid.shape
df_covid.head()

# checando e filtrando lista de países
df_covid.location.drop_duplicates()
df_covid2 = df_covid[~df_covid.location.isin(['World','International'])] # ~ -> negação
df_paises = df_covid2.drop_duplicates(subset='location')
df_paises.shape
df_paises.head()

# filtrando colunas
df_paises.columns
df_paises.columns[26]
lista_paises = df_paises['location'].reset_index(drop=True)  # salvando lista de países antes de filtrar DF
df_paises    = df_paises[df_paises.columns[26:-1]]
df_paises    = df_paises.reset_index(drop=True)
df_paises.shape
df_paises.head()
lista_paises

# buscanso maiores valores dos parâmetros do COVID
obitos, obt_per_mill, casos, testes, continente = [],[],[],[],[]
for p in lista_paises:
    df_covid_f = df_covid2[df_covid2.location == p]
    obitos.append(df_covid_f.total_deaths.max())
    obt_per_mill.append(df_covid_f.total_deaths_per_million.max())
    casos.append(df_covid_f.total_cases.max())
    testes.append(df_covid_f.total_tests.max())
    continente.append(df_covid_f.continent.drop_duplicates().item())

df_paises2 = pd.concat([lista_paises, pd.Series(continente, name = 'continente'), pd.Series(obitos, name = 'total_obitos'), pd.Series(obt_per_mill, name = 'obitos_p_mill'),pd.Series(casos, name = 'total_casos'),pd.Series(testes, name = 'total_testes'), df_paises],axis=1)

# ranqueando tabela
df_paises2[df_paises2.continente == 'South America'].sort_values(by='total_casos',ascending=False)

# verificando e removendo ausência de dados
df_paises2.info()
del df_paises2['total_testes'], df_paises2['handwashing_facilities']
df_paises2.columns
df_paises2.isnull().any(axis=1) # retorna colunas com algum valor NAN como True
df_paises3 = df_paises2[df_paises2.isnull().any(axis=1) == False] # novo DF
df_paises3.info()


# estatística descritiva exploratória
df_stats  = df_paises3.describe()
df_stats[df_stats.columns[0:6]]
cor_table = df_paises3.corr(method = 'spearman')

import seaborn as sn
import matplotlib.pyplot as plt
ct = sn.heatmap(cor_table, annot=True, cmap="YlGnBu")
ct.set_xticklabels(ct.get_xticklabels(),rotation=20)
plt.show()

'''
import statsmodels.formula.api as sm
modelB = sm.ols(formula='B ~ SR', data=df2)
modelB_trained = modelB.fit()
modelB_trained.summary()

modelB = sm.ols(formula='B ~ SR + WS', data=df2)
modelB_trained = modelB.fit()
modelB_trained.summary()
'''

### Textos ~dados não-estruturados
# https://forms.gle/vut4wWavN8WesRZJA
# pip install nltk
# https://www.nltk.org/data.html
%run wordcloud_IdacoNave.py
