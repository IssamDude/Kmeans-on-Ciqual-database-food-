# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 20:40:09 2021

@author: issam
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 14:19:59 2021

@author: issam
"""
import random
import math
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly
pd.options.mode.chained_assignment = None  # default='warn'

#import re
#import numpy as np


# Exporting the excel file to a pandas dataframe
dataframe1 = pd.read_excel('Table Ciqual 2020_ENG_2020 07 07.xlsx')
dataframe1.head()

# Our focus will be around milk and milk products
dataframe3 = dataframe1.loc[dataframe1['alim_grp_nom_eng'] == "milk and milk products"]
#print(dataframe3.head())

# The 5 components we'll study are : Energy, water, protains, carbohydrates and  fats
# The dataframe originally contains about 70 columns, we will only keep usefull ones
df = dataframe3[['alim_ssgrp_nom_eng','alim_ssssgrp_nom_eng','alim_code','alim_nom_eng','Energy, Regulation EU No 1169/2011 (kcal/100g)','Water (g/100g)','Protein (g/100g)','Carbohydrate (g/100g)','Fat (g/100g)']]

# We reset the index to 0, 1, 2...

#print(df.head())
df.rename(columns = {'Energy, Regulation EU No 1169/2011 (kcal/100g)':'Energy (kcal/100g)'}, inplace = True)


# Now we need to drop the rows containing non numeric values in componenets :
    #For that, we used regular expressions : 
        
x1=df[df['Fat (g/100g)'].str.match('^[0-9]*[,]{0,1}[0-9]*$')== True]
x2=x1[x1['Protein (g/100g)'].str.match('^[0-9]*[,]{0,1}[0-9]*$')== True]
x3=x2[x2['Carbohydrate (g/100g)'].str.match('^[0-9]*[,]{0,1}[0-9]*$')== True]
x4=x3[x3['Water (g/100g)'].str.match('^[0-9]*[,]{0,1}[0-9]*$')== True]
x5=x4[x4['Energy (kcal/100g)'].str.match('^[0-9]*[,]{0,1}[0-9]*$')== True]

x5=x5.reset_index(drop=True)

# To work on the values of the components, we have to convert them first to floats since they are object type ( strings )
# The conversion doesn't work unless we change the decimal comma to a decimal dot ( 2,2 should be 2.2 in order not to generate an error in astype())

x5['Water (g/100g)'] = x5['Water (g/100g)'].str.replace(',','.')
x5['Water (g/100g)'] = x5['Water (g/100g)'].astype(float, errors = 'raise')

x5['Protein (g/100g)'] = x5['Protein (g/100g)'].str.replace(',','.')
x5['Protein (g/100g)'] = x5['Protein (g/100g)'].astype(float, errors = 'raise')

x5['Carbohydrate (g/100g)'] = x5['Carbohydrate (g/100g)'].str.replace(',','.')
x5['Carbohydrate (g/100g)'] = x5['Carbohydrate (g/100g)'].astype(float, errors = 'raise')

x5['Fat (g/100g)'] = x5['Fat (g/100g)'].str.replace(',','.')
x5['Fat (g/100g)'] = x5['Fat (g/100g)'].astype(float, errors = 'raise')

x5['Energy (kcal/100g)'] = x5['Energy (kcal/100g)'].str.replace(',','.')
x5['Energy (kcal/100g)'] = x5['Energy (kcal/100g)'].astype(float, errors = 'raise')

# We now have "cleaned" our dataframe, converted it to the types we want :
# Let's first rename it to a more practical name : data
    
data = x5
print(data.info())
print(data.shape)
print(data.head())



# As we'll perform the k means algorithm on this data, we'll need to iterate through it.

columns = list(data) # List containing the names of columns.

print(columns)

for i in columns : 
    print(data[i][2]) # Example : The third row of our data

print(data[columns[2]])

print("2 e code d'aliment : ", data['alim_code'][2])

#Create functions to access Columns, rows & value with coordinates 

def acces_column1(d,column_number) : 
    columns = list(d)
    return d[columns[column_number]]

#Test : 

print("Colonne 4 :  ", acces_column1(data, 3))

def acces_column2(d,column_name):
    return d[column_name]

#Test :

print("Colonne Water  :  ", acces_column2(data, "Water (g/100g)" ))

def acces_row(d, row_number) : 
    list1=[]
    columns = list(d)
    for i in columns :
        list1.append(d[i][row_number])
    return list1

#Test ! 

print("4 e ligne : ", acces_row(data, 3))



def acces_element(d,n,m) : # d : dataframe , n : ligne, m : colonne
    columns = list(d)
    assert (n>=0) and (n<=d.shape[0]) , "Please make sure you enter a valid row number"
    assert (m>=0) and (m<=d.shape[1]) , "Please make sure you enter a valid column number"
    assert (type(n)==int ) and (type(m)==int), "Row and column must be integers"
    return d[columns[m]][n]


#Test :

print("Element dans la 2e ligne, 3e colonne ", acces_element(data,1,2))


def getIndexes(dfObj, value):
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

#Test :

print("Index de l'aliment au code 19024 : ", getIndexes(data, 19024)[0][0])

def get_foodname(alim_code) :  # Getting the aliment's name using his alim_code.
    return acces_element(data,getIndexes(data, alim_code)[0][0],3)

#Test :

print("Nom de l'aliment au code  19051 : ", get_foodname(19051))

# TODO : Write a distance function, and a function that calculate the "centroid" of n points.


subdata = data[['alim_code','Energy (kcal/100g)','Water (g/100g)','Protein (g/100g)','Carbohydrate (g/100g)','Fat (g/100g)']]
#La dataframe qu'on va utiliser pour notre algorithme K means.
#subdata.to_excel("short.xlsx")

markersize = subdata['Energy (kcal/100g)']/10
markercolor = subdata['Water (g/100g)']/10

#Make Plotly figure
fig1 = go.Scatter3d(x=subdata['Protein (g/100g)'],
                    y=subdata['Carbohydrate (g/100g)'],
                    z=subdata['Fat (g/100g)'],
                    marker=dict(size=markersize,
                                color=markercolor,
                                opacity=0.9,
                                reversescale=True,
                                colorscale='Greens'),
                    line=dict (width=0.02),
                    mode='markers')

#Make Plot.ly Layout
mylayout = go.Layout(scene=dict(xaxis=dict( title="Protein"),
                                yaxis=dict( title="Carbohydrate"),
                                zaxis=dict(title="Fat")),)

#Plot and save html
plotly.offline.plot({"data": [fig1],
                     "layout": mylayout},
                     auto_open=True,
                     filename=("5D Plot.html"))


def get_foodcomponents(alim_code) : #Nous retourne la liste des composants de l'aliment ayant pour code alim_code
    return acces_row(subdata, getIndexes(subdata, alim_code)[0][0])[1:]
def get_food(alim_code) : 
    return acces_row(subdata, getIndexes(subdata, alim_code)[0][0])


def distancei(c1, c2) : # Fonction qui calcule la distance euclidienne entre deux points aliments a1 a2 de dimension 5 de la dataframe subdata.
    d2=0 # distance au carré
    for i in range(len(get_foodcomponents(c1))):
        d2+=(get_foodcomponents(c1)[i]-get_foodcomponents(c2)[i])**2
    return math.sqrt(d2)     

def distanceii(p, c1) : # distance entre un point et un aliment de la dataframe.
    d2=0
    for i in range(len(get_foodcomponents(c1))):
        d2+=(p[i]-get_foodcomponents(c1)[i])**2
    return math.sqrt(d2)

def centroid(*args) : # Fonction qui calcule le centre d'un certain nombre de points.
    y=get_foodcomponents(args[0])
    for i in range(1, len(args)) : 
        for j in range (0, len(get_foodcomponents(args[i]))) : 
            y[j]+=get_foodcomponents(args[i])[j]
    for k in range(len(y)) : 
        y[k]=round((y[k]/len(args)),3)
    return y

def centroid2(l) : # Fonction qui calcule le centre d'un certain nombre de points.
    y=get_foodcomponents(l[0])
    for i in range(1, len(l)) : 
        for j in range (0, len(get_foodcomponents(l[i]))) : 
            y[j]+=get_foodcomponents(l[i])[j]
    for k in range(len(y)) : 
        y[k]=round((y[k]/len(l)),3)
    return y



  
    
 

file_name = 'new.xlsx'
x5.to_excel(file_name)

file_name4="subdata.xlsx"
subdata.to_excel(file_name4)

 
def kmeans(d, n, k) : # d : dataframe, n : nombre d'itérations,  k : K
    clusters=[]
    
    
    
    for i in range(k): # On crée k clusters initialement vides
        clusters.append([])
    
    x=random.sample(acces_column2(d, "alim_code").tolist(),k) #k code d'aliments uniques choisis au hasard.
    
    for i in range(k): # On remplit la liste des clusters par k code d'aliments choisis au hasard.
        clusters[i].append(x[i])
    
    
    #FIRST ITERATION : 
    
    
    for i in range(len(d)):
            d1=distancei(clusters[0][0], acces_element(subdata, i, 0))
            d2=distancei(clusters[1][0], acces_element(subdata, i, 0))
            d3=distancei(clusters[2][0], acces_element(subdata, i, 0))
            mindist=min(d1, d2, d3)
            if mindist == d1 :
                clusters[0].append(acces_element(subdata, i, 0))
            elif mindist == d2 :
                clusters[1].append(acces_element(subdata, i, 0))
            else:
                clusters[2].append(acces_element(subdata, i, 0))
    cc1=centroid2(clusters[0])
    cc2=centroid2(clusters[1])
    cc3=centroid2(clusters[2])
    print("Centres 1  : ", cc1, cc2, cc3)

    
    
    #On vide les clusters 
    clusters[0].clear()
    clusters[1].clear()
    clusters[2].clear()
    
      #n-2 itérations suivantes : 
    for a in range(1, n-1) :  
        
        for i in range(len(d)):
            d1=distanceii(cc1, acces_element(subdata, i, 0))
            d2=distanceii(cc2, acces_element(subdata, i, 0))
            d3=distanceii(cc3, acces_element(subdata, i, 0))
            mindist=min(d1, d2, d3)
     
            if mindist == d1 :
                 clusters[0].append(acces_element(subdata, i, 0))
            elif mindist == d2 :
                 clusters[1].append(acces_element(subdata, i, 0))
            else:
                 clusters[2].append(acces_element(subdata, i, 0))
        cc1=centroid2(clusters[0])
        cc2=centroid2(clusters[1])
        cc3=centroid2(clusters[2])
        print("Centres", a+1, "   : ", cc1, cc2, cc3)
        clusters[0].clear()
        clusters[1].clear()
        clusters[2].clear()
    #Derniere itération     
    for i in range(len(d)):
            d1=distanceii(cc1, acces_element(subdata, i, 0))
            d2=distanceii(cc2, acces_element(subdata, i, 0))
            d3=distanceii(cc3, acces_element(subdata, i, 0))
            mindist=min(d1, d2, d3)
     
            if mindist == d1 :
                 clusters[0].append(acces_element(subdata, i, 0))
            elif mindist == d2 :
                 clusters[1].append(acces_element(subdata, i, 0))
            else:
                 clusters[2].append(acces_element(subdata, i, 0))   
       
    print("Centres finaux ", cc1, cc2, cc3)
    
  
        
   
    
    return clusters



C = kmeans(subdata, 7, 3)
print("Cluster 1:",C[0])
print("Cluster 2:",C[1])
print("Cluster 3:",C[2])
