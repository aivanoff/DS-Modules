
# coding: utf-8

# # Slave Migration Lab
# 
# In 1793(?) Eli Whitney patented an invention with enormous consequences:
# <img src="eli-whitney-cotton-gin.jpg" width=250>
# source: "http://mtviewmirror.com/eli-whitney-inventor-of-the-cotton-gin/"
# 
# Textile production drove the early Industrial Revolution, but by the early 19th Century, the need for cotton was growing much faster than the supply.  The reason was that "short staple" cotton -- the easiest kind of cotton to grow was not commercially viable because separating the seeds from the fluffy part was too tedious even for slave labor.
# 
# Whitney's cotton gin changed that and as a result, by 1860 the American South below the 37th paralell came to supply over 80% of Britain's remarkable demand for Cotton.

# In[542]:

from datascience import *


# In[543]:

# Run this cell, but please don't change it.

# These lines import the Numpy and Datascience modules.
import numpy as np
from datascience import *
#from datascience.predicates import are
# These lines do some fancy plotting magic
import matplotlib
get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')


# In[544]:

slaves1850=Table.read_table("ICPSR-LabDataSlavesByAgeSex1850-long.csv")
slaves1860=Table.read_table("ICPSR-LabDataSlavesByAgeSex1860-long.csv")


# In[545]:

slaves1860.show()


# In[546]:

slaves1850.relabel('variable','agesex')
slaves1850.relabel('value','N')
slaves1860.relabel('variable','agesex')
slaves1860.relabel('value','N')


# What's up with 'nan' ?  
# 
# Why do you think New York's "X860SLAVE.FEMALES.00.01.UNDER.1." are reported as 'nan'  while those of New Jersey
# are reported as 0 ?
# 
# Yes google knows the answer, but thinking before googling is good for your soul.

# In[547]:

## Let's lose the virtuous -- but non interesting states that have no saves
slaves1850=slaves1850.where(slaves1850['N'] >=0)
slaves1860=slaves1860.where(slaves1860['N'] >=0)


# In[548]:

#slaves1850.where(slaves1850['N'] >=0).show(10)
# Let's investigate which states had slaves in 1850 and 1860 by working with tables that 
# contain the number of records whith valid entries (0 or greater numbers of slaves ie. NOT nan)
s50test=slaves1850.select(['STATE.NAME','N']).where(slaves1850['N'] >=0).group('STATE.NAME', collect= len)
s60test=slaves1860.select(['STATE.NAME','N']).where(slaves1860['N'] >=0).group('STATE.NAME', collect= len)
## Should s60test ans s50test have the same number of rows?
## what are the implications of different number of rows.
s60test.num_rows == s50test.num_rows
s50test.sort('STATE.NAME').show()
s60test.sort('STATE.NAME').show()


# In[549]:

## Find the states which have become  free (or slave?) between 1850 and 1860
## add a year column 
s50test.append_column('year',1850)
s60test.append_column('year',1860)
## make a copy of s50test
s50save=s50test.copy()
## because s50test will be changed by the .append method -- even though we asign the result 
s5060stacked=s50test.append(s60test).group('STATE.NAME',collect = sum)
## reset s50test so it can be used again
s50test=s50save.copy()
## show the rows that are in Both the 1850 and 1860 tables
print("States with slaves in both 1850 and 1860")
s5060stacked.where(s5060stacked['year sum'] == 3710).show()
print("that's" ,s5060stacked.where(s5060stacked['year sum'] == 3710).num_rows, "states")

## and the rows that are in only one of the years
print("And here are the states that only have slaves in either 1850 or 1860")
s5060stacked.where(s5060stacked['year sum'] < 3710).show()


# Google Compromise of 1850; Kansas-Nebraska Act; and Dred Scott Decision

# Now let's clean up the original data tables (slaves1850 and slaves1860) so that we can estimate slave mortality rates... and eventually the numbers of slaves by age and sex who migrated into and out of each state.
# 
# For this we will need to use some string functions:
# <ul>
# <li> x.split('.') -- which converts a sring, x, into a list by splitting at each instance of '.'
# <li> x.find('boo') -- which reports the index of the 'b' within the string x.
# <li> 'y' in L  -- which reports whether or not the  'y' is an element of list L
# </ul>

# In[550]:

## But first, it turns out that the agesex variable is not easily comparable across 1850 and 1860. This sort of thing is 
## quite common in science -- but it really sucks.
slaves1850.where(slaves1850['STATE.NAME'] == "VIRGINIA").select('agesex').show()
slaves1860.where(slaves1860['STATE.NAME'] == "VIRGINIA").select('agesex').show()


# In[551]:

## How many of these differences did you find:

## (1) TOT vs TOTAL
## (2) UNKW vs UKWN  -- nice!
## we'll neaten up a few more things

## grab the agesex column from slaves1860 as an nparray
agesex= slaves1860['agesex'] 
## use barbaric python code (with familiar .replace() method) to modify each element of agesex
agesex= [f.replace('.UNDER.1.','') for f in agesex] # useless redundant info
agesex= [f.replace('X860SLAVE.','') for f in agesex] # useless redundant
agesex= [f.replace('X860TOT.SLAVE','TOTAL') for f in agesex ] 
agesex= [f.replace('AND.OVER','110') for f in agesex ] 
agesex= [f.replace('AGE.UNKW','UNKOWN') for f in agesex ] 
## make the array agesex into a new column of slaves1860 -- but name it temp so as not to conflict with existing column
slaves1860.append_column('temp',agesex)
## inspect results and be happy
slaves1860.show(100)
## recreate slaves1860 keeping only the columns that matter AND renaming temp to agesex
slaves1860=slaves1860.select(['STATE.NAME','temp','N']).relabel('temp','agesex')
slaves1860.show(25)


# In[552]:



##  and do the same sort of thing to 1850
agesex= slaves1850['agesex'] 
agesex= [f.replace('.UNDER.01.','') for f in agesex] 
agesex= [f.replace('X850SLAVE.','') for f in agesex] 
agesex= [f.replace('X850TOTAL.SLAVE','TOTAL') for f in agesex ] 
agesex= [f.replace('AND.OVER','110') for f in agesex ] 
agesex= [f.replace('AGE.UKWN','UNKOWN') for f in agesex ] 
slaves1850.append_column('temp',agesex)
#slaves1850.show()
slaves1850=slaves1850.select(['STATE.NAME','temp','N']).relabel('temp','agesex')
slaves1850.show()


# In[553]:

## Now we need to use the information in teh agesex column to create three new columns that we can work with
# more easily



## Let's use the string functions .split(), .find() and in to detect patterns in the agesex variable and use that
## to constuct useful



def parseAgesex(x) :
    # convert x from string to list splitting on '.' x is expected to be like: 'X850SLAVE.FEMALES.99.AND.OVER'
    splitz = x.split('.')
    ## grab the ages limits if they exist otherwise nan
    try:
        loAge=int(splitz[1])
    except:
        loAge=float('nan')
    try:
        hiAge=int(splitz[2])
    except:
        hiAge=float('nan')
    # initialize sex,total, and unknown variables
    sex='missing'
    total=False
    unknown=False
    
    if x.find('FEMAL') >= 0 :
        sex = 'FEMALE'
    elif x.find('MALE') >= 0 :     
        sex = 'MALE'
    if  x.find('UNKOWN') >= 0  :
        unknown = True 
    if x.find('TOTAL') >= 0 :
        total = True
    # return a 'dict' which is a special but easy to understand data type in python
    return({'string':x,'sex':sex,'loAge':loAge,'hiAge':hiAge,'total':total,'unknown':unknown})


parsedAgesex1850=slaves1850.apply(parseAgesex,'agesex')
parsedAgesex1860=slaves1860.apply(parseAgesex,'agesex')

print("Here's what the list of dicts, parsedAgesex1860 looks like")
print(parsedAgesex1860[0:5])
slaves1850.append_column('sex',(f['sex'] for f in parsedAgesex1850))
slaves1850.append_column('loAge',(f['loAge'] for f in parsedAgesex1850))
slaves1850.append_column('hiAge',(f['hiAge'] for f in parsedAgesex1850))
slaves1850.append_column('total',(f['total'] for f in parsedAgesex1850))
slaves1850.append_column('unknown',(f['unknown'] for f in parsedAgesex1850))
slaves1850.show()
slaves1860.append_column('sex',(f['sex'] for f in parsedAgesex1860))
slaves1860.append_column('loAge',(f['loAge'] for f in parsedAgesex1860))
slaves1860.append_column('hiAge',(f['hiAge'] for f in parsedAgesex1860))
slaves1860.append_column('total',(f['total'] for f in parsedAgesex1860))
slaves1860.append_column('unknown',(f['unknown'] for f in parsedAgesex1860))
print("And here is what our enhanced version of slaves1860 looks like")
slaves1860.show()


# In[554]:

## delete the unknowns ages and Total rows
print(slaves1850.num_rows)
slaves1850=slaves1850.where(slaves1850.column('unknown') == False )
slaves1850=slaves1850.where(slaves1850.column('total') == False )
print(slaves1850.num_rows)
print(slaves1860.num_rows)

slaves1860=slaves1860.where(slaves1860.column('unknown') == False )
slaves1860=slaves1860.where(slaves1860.column('total') == False )
print(slaves1860.num_rows)


# In[555]:

print("Slaves of known age in 1850")
slaves1850_allStates=slaves1850.groups(['loAge','hiAge','sex','agesex'],sum).sort('loAge')
slaves1860_allStates=slaves1860.groups(['loAge','hiAge','sex','agesex'],sum).sort('loAge')
## note agesex is redundant in the above, but if we leave it out we lose it 'cause it does not sum well
slaves1850_allStates.show()
slaves1860_allStates.show()


# In[556]:



print("slaves of known age 1850 ")
sum_1850=sum(slaves1850['N'])

print(sum_1850)
print("slaves of known age 1860 ")
sum_1860=sum(slaves1860['N'])
print(sum_1860)
print("percent increase 1850 - 1860")
print((sum_1860 -sum_1850)/sum_1850)
print("average annual growth rate")
import math
print(math.log(sum_1860/sum_1850) / 10)




# In[559]:

#slaves1850_allStates.where(slaves1850_allStates['sex'] == 'FEMALE').barh(column_for_categories='loAge',select='N sum')
#slaves1850_allStates.where(slaves1850_allStates['sex'] == 'FEMALE').scatter('loAge',select='N sum')
#slaves1850_allStates.where(slaves1850_allStates['sex'] == 'FEMALE').scatter('loAge',select='N sum')
spop1850=slaves1850_allStates.select(['sex','loAge','hiAge','agesex','N sum']).relabeled('N sum','N1850')
spop1860=slaves1860_allStates.select(['sex','loAge','hiAge','agesex','N sum']).relabeled('N sum','N1860')

#spop1850.show(10)
#spop1860.show(10)
spopByYear=spop1850.join('agesex',spop1860.select(['agesex','N1860']))
#spopByYear.show()
spopByYear.scatter('loAge',select=['N1850','N1860'])
spopByYear.show()


# In[606]:

from datascience.predicates import are
temp=spopByYear.where(spopByYear.column('loAge')<= 1).groups(['sex'],sum)
temp2a=spopByYear.where(spopByYear.column('loAge') ==10)
temp2b=spopByYear.where(spopByYear.column('loAge') == 15)
Foo=Table.with_rows(temp2a.to_array).with_rows(temp2b.to_array())
#temp2=  spopByYear.where(spopByYear.column('loAge') ==15).with_rows(temp2a.to_array)
temp.show()

#temp2.show()
## correct the loAge and hiAge
temp.append_column('loAge sum',0)
temp.relabel('loAge sum','loAge')
temp.append_column('hiAge sum',4)
temp.relabel('hiAge sum','hiAge')
temp.relabel('N1850 sum','N1850')
temp.relabel('N1860 sum', 'N1860')
temp.append_column('agesex sum',['FEMALES.0.4','MALES.0.4'])
temp.relabel('agesex sum','agesex')
temp.show()
temp
spopByYearx=spopByYear.where(spopByYear.column('loAge') >1).with_rows(
    temp.select(['agesex','sex','loAge','hiAge','N1850','N1860']).to_array())


spopByYearx.append_column('midAge',spopByYearx.apply(lambda hi, lo :(lo+hi)/2, ['loAge','hiAge']))

spopByYearx.sort('loAge')


# In[575]:

## We need to combine the 0-1 and the 1-4 age ranges because we want to compare it with
## the 10-14 age group.  It's a lot of work to do this simple operation.  You might want to close your eyes.


temp85=spop1850.where(spop1850.column('loAge') <=1).groups(['sex'], sum)
temp85.append_column('loAge',0)
temp85.append_column('hiAge',4)
temp85.append_column('agesex',['FEMALES.0.4','MALES.0.4'])
temp85=temp85.select(['sex','loAge','hiAge','agesex','N1850 sum']).relabel('N1850 sum','N1850')
temp85.show()
spop1850x=spop1850.where(spop1850.column('loAge') >1).with_rows(temp85.to_array())

spop1850x.append_column('midAge',spop1850x.apply(lambda hi, lo :(lo+hi)/2, ['loAge','hiAge']))
spop1850x.sort('loAge')
                        


# In[540]:

spop1860.apply(lambda hi, lo :(lo +hi)/2 , ['loAge','hiAge'])
from datascience.predicates import are
#spop1860.where('loAge', are.below(10))
temp86=spop1860.where(spop1860.column('loAge') <=1).groups(['sex'], sum)
temp86.append_column('loAge',0)
temp86.append_column('hiAge',4)
temp86.append_column('agesex',['FEMALES.0.4','MALES.0.4'])
temp86=temp86.select(['sex','loAge','hiAge','agesex','N1860 sum']).relabel('N1860 sum','N1860')
temp86.show()
spop1860x=spop1860.where(spop1860.column('loAge') >1).with_rows(temp86.to_array())

spop1860x.append_column('midAge',spop1850x.apply(lambda hi, lo :(lo+hi)/2, ['loAge','hiAge']))
spop1860x.sort('loAge').show()


# In[ ]:




# <img src="http://images.slideplayer.com/13/3828559/slides/slide_4.jpg">
# 

# https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwij5unfl7rNAhVT2GMKHYGKAaEQjRwIBw&url=http%3A%2F%2Fslideplayer.com%2Fslide%2F3828559%2F&psig=AFQjCNHZaJXmI6Ww060hSrcu3wo6L9D9kw&ust=1466635127084012
