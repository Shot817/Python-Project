#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Data Analytics for 50km races


# In[1]:


# Import Modules

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


# Get Data From CSV File

df = pd.read_csv(r"C:\Users\Artem\Desktop\Pandas\TWO_CENTURIES_OF_UM_RACES.csv")
df.head(100)


# In[3]:


# Get Number of Columns/Rows for Table 

df.shape


# In[4]:


# look at Data Types in Table

df.dtypes


# In[5]:


##  Data Cleaning Process


# In[6]:


# Get Data Only for 50km Races

df2 = df[df['Event distance/length'].isin(['50km'])]
df2.head(10)


# In[7]:


# Split 'Event name' Column to Get Only Countries

df2['Event name'] = df2['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)
df2.head(10)


# In[8]:


# Get Exact Athlete Age

df2['Athlete Age'] = df2['Year of event'] - df2['Athlete year of birth']
df2.head(10)


# In[9]:


# Remove 'h' from 'Athlete performance' column values

df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)
df2.head(10)


# In[10]:


# Remove Needless Columns

df3 = df2.drop(['Event number of finishers','Athlete club','Athlete year of birth','Athlete age category'], axis = 1)
df3.head(10)


# In[11]:


# Search for Null Values

df3.isnull().sum()


# In[12]:


# Dispay Null Value

df3[df3['Athlete Age'].isna() == 1]


# In[13]:


# Remove Data With Null Values

df3 = df3.dropna()


# In[14]:


# Search For Duplicates

df3[df3.duplicated() == True]


# In[15]:


# Remove Duplicates

df3 = df3.drop_duplicates()


# In[16]:


# Reset Indexes

df3.reset_index(drop = True)


# In[17]:


# Fixing Data Types 

df3.dtypes


# In[18]:


# Changing Data type for 'Athlete Age' to integer

df3['Athlete Age'] = df3['Athlete Age'].astype(int)


# In[19]:


# Find Bad Data Values in 'Athlete average speed' column

df3[df3['Athlete average speed'].str.contains(':') == True]


# In[20]:


# Remove Values with Bad Data Format

df3 = df3.drop(df3[df3['Athlete average speed'].str.contains(':') == True].index)


# In[21]:


# Changing Data type for 'Athlete average speed' to float

df3['Athlete average speed'] = df3['Athlete average speed'].astype(float)


# In[22]:


df3.head()


# In[23]:


# Rename Columns For Easiest Access

df3 = df3.rename(columns = {'Year of event': 'year',
                            'Event dates': 'race_date',
                            'Event name': 'event_country',
                            'Event distance/length': 'lengh',
                            'Athlete performance': 'runner_time',
                            'Athlete country': 'runner_country',
                            'Athlete gender': 'gender',
                            'Athlete average speed': 'average_speed',
                            'Athlete ID': 'runnerId',
                            'Athlete Age': 'age' })


# In[24]:


df3.head()


# In[25]:


# Reorder Columns

df4 = df3[['year','race_date','event_country','lengh','runner_country','runner_time','average_speed','gender','age','runnerId']]


# In[26]:


df4.head()


# In[27]:


# Remove Extra Value 'x' in gender column

df4 = df4.drop(df4[df4['gender'].str.contains('X') == True].index)


# In[28]:


## Creating Additional Columns For Analysis


# In[29]:


# Create Separate Column for Months

df4['race_month'] = df4['race_date'].str.split('.').str.get(1).astype(int)


# In[30]:


# Create Separate Column For Season

df4['race_season'] = df4['race_month'].apply(lambda x: 'Winter' if x > 11 else 'Fall' if x > 8 else 'Summer' if x > 5 else 'Spring' if x > 2 else 'Winter' )


# In[31]:


# Take Only Correct Speed Values From 'average_speed'

df4 = df4[df4['average_speed'] < 20]


# In[32]:


# Take Only Runners > 18 years old

df4 = df4[df4['age'] > 17]


# In[57]:


# Take Runners under 99

df4 = df4[df4['age'] < 100]


# In[58]:


df4.head()


# In[59]:


## Analyze Data


# In[60]:


# Find Runners Average Age by Genders + Amount of Runners by Gender

df4.groupby(['gender'])['age'].agg(['mean','count']).round(2)


# In[61]:


# Amount Of Runners Difference By Genders

sns.displot(data = df4, x ='gender', hue = 'gender')


# In[204]:


# Runners Ages

sns.set(rc={'figure.figsize':(19,10)})

sns.countplot(df4, x="age", hue = 'gender')


# In[62]:


# Find Average Speed by Gender

df4.groupby(['gender'])['average_speed'].mean().round(2)


# In[205]:


# Runners Speed By Gender

sns.displot(data=df4, x="average_speed", hue="gender", kind="kde")


# In[64]:


# Find Average Speed by Age 

df4.groupby(['age'])['average_speed'].mean().round(2)


# In[71]:


# Top 3 Fastest Runners by Age 

df4.groupby(['age'])['average_speed'].agg(['mean']).sort_values('mean', ascending = False).head(3).round(2)


# In[72]:


# Top 3 Slowest Runners by Age 

df4.groupby(['age'])['average_speed'].agg(['mean']).sort_values('mean', ascending = True).head(3).round(2)


# In[301]:


# Amount of Runners by Years

df4.groupby(['year'])['runnerId'].count()


# In[177]:


# Amount of Runners By Years Plot

sns.set(rc={'figure.figsize':(13,7)})

sns.countplot(df4, x="year")


# In[165]:


# Amount Of Runners by Country 

df4.groupby(['runner_country'])['runner_country'].count().sort_values(ascending = False)


# In[336]:


# Average Speed by Seasons

df4.groupby(['race_season'])['average_speed'].agg(['mean','count']).sort_values('mean', ascending = False)


# In[ ]:


### Conclusions

# Average Age of Runners - 42.19 years
# Most Of Runners in Races was Mens
# Mens Average Speed was a Little Faster than Womens - 8.12 km/hour VS 7.36 km/hour
# Fastest Age Of Runners was - 21 Years - 8.38 km/hour
# Slowest Age of Runners was - 94 Years - 4.46 km/hour
# Year with Most Runners was - 2019 
# Country From Where Most Runners - USA(604814)
# Best Season for Races was Spring - With Best Average Speed Performance - 8.34 km/hour

