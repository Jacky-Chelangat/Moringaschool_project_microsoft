#!/usr/bin/env python
# coding: utf-8

# # Microsoft Market Research (Film industry)
# Author: Jacqueline Chelang'at
# 

# ## Overview & Business Problem
# Microsoft would like to start a new revenue stream in original video content creation. 
# Explore what types of films are currently doing the best at the box office. 
# Translate the findings into actionable insights to help Microsoft decide if this is a viable business venture.
# 

# # The Data
# 
# 3 Sets of data are utilized for this research,
# 
# **Title basics - Contains various movie titles, years, runtimes and genres.
# 
# **Movie gross - Contains various movie titles, studio, domestic gross, foreign gross and year.
# 
# **Title ratings - Contains the Average ratings and number of votes of various movies.
# 

# In[32]:


#Import the requisite libraries (Pandas, seaborn and matplotlib)
#Assign the file imdb.title.basics.csv.gz to a variable and read the CSV file in pandas to see the info contained
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
df = pd.read_csv('imdb.title.basics.csv.gz')
df


# # Data cleaning

# In[3]:


# Get an overall view of the title basics file and the number of null values present
df.info()


# In[4]:


#Check summation of null values in the title basics file
df.isna().sum()


# In[6]:


#Check for duplicates in the title basics file
duplicates = df[df.duplicated()]
print(len(duplicates))
duplicates.head()


# In[7]:


#Work out the mean of runtime_minutes to obtain the values to replace the missing values with
print(df['runtime_minutes'].mean())


# In[8]:


#Replace the null values in the runtime_minutes column with the mean of runtimes
df['runtime_minutes'] = df['runtime_minutes'].fillna(value = df['runtime_minutes'].mean())
df.isna().sum()


# In[9]:


#Calculate the mean to confirm the if value has changed significantly after filling the null values
print(df['runtime_minutes'].mean())


# In[10]:


#Fill the null values in the genres folder with the mode and confirm if there are any null values left
df['genres'] = df['genres'].fillna(value = df['genres'].mode()[0])
df.isna().sum()


# In[11]:


#Display and review the cleaned data
df


# In[12]:


#Assign the movie_gross csv document to a variable and display the contents
df1 = pd.read_csv('bom.movie_gross.csv.gz')
df1


# In[13]:


#Check the number of null values in the movie_gross data
df1.isna().sum()


# In[14]:


#Display the details of the movie_gross data and number and data type of the variables
df1.info()


# In[15]:


#Fill the null values in the domestic gross column of the movie_gross data with the the mean
df1['domestic_gross'] = df1['domestic_gross'].fillna(value = df1['domestic_gross'].mean())
df1.isna().sum()


# In[16]:


# Replace the foreign character in the foreign_gross column with blank
df1['foreign_gross'] = df1['foreign_gross'].str.replace(',','').apply(float)

#Check if the data type of the foreign gross column has changed from object to float

df1.info()


# In[17]:


# Fill the null values in the foreign gross column with the median of the data

df1['foreign_gross'] = df1['foreign_gross'].fillna(value = df1['foreign_gross'].median())

df1.info()


# In[18]:


#drop the remaining 5 rows showing null values on the studio column
df1 = df1.dropna()
df1.isna().sum()


# In[19]:


#display the details of the movie gross data to ensure the clean up of data is complete
df1.info()


# In[20]:


#Assign a variable to the 3rd data set, the title ratings and display the data
df2 = pd.read_csv('imdb.title.ratings.csv.gz')
df2


# In[21]:


#Display the details of the data to check the data types of the columns and the number of null values present
df2.info()


# # Data Analytics

# In[22]:


#Intall pandasql to enable you  to work with sql within the pandas dataframe
get_ipython().system('pip install pandasql')


# In[23]:


#import pandas sql as sqldf
from pandasql import sqldf


# In[24]:


#Pass a global variables to avoid doing this everytime we need to use an object
pysqldf = lambda q: sqldf(q, globals())


# In[46]:


#Set the theme for the visuals as dark grid using seaborn libraries
sns.set_theme(style = 'darkgrid')


# In[47]:


#Plot the number of movies that have been created over the years to observe the trend in the industry
q = """
SELECT start_year, Count(*) AS n_movies
FROM df
GROUP BY start_year
HAVING n_movies > 100
;"""

movie_genres_by_year_df = pysqldf(q)


fig, axes = plt.subplots(nrows =1, ncols = 1, figsize = (14,4))
movie_genres_by_year_df.set_index('start_year')['n_movies'].plot(kind='bar',ax=axes)
axes.set_title('Number of Movies per year')
axes.set_xlabel('years')
axes.set_ylabel('count');



# In[26]:


#Join the three tables (title basics, movie gross and the title ratings), and assign the new table a variable
#Display the table
q1 = """
SELECT *
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst);
"""

title_basics_join_movie_gross = pysqldf(q1)
title_basics_join_movie_gross


# In[27]:


# Display the foreign gross earnings, the average rating and the number of votes of the top 10 voted for movies
q2 = """
SELECT title, foreign_gross,averagerating, numvotes
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst)
ORDER BY numvotes DESC
LIMIT 10;
"""

top_10_movies_by_votes = pysqldf(q2)
top_10_movies_by_votes


# In[28]:


# Display the top domestic gross, the average rating and the number of votes of the top 10 earning movies
q2 = """
SELECT title, foreign_gross,averagerating, numvotes
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst)
ORDER BY foreign_gross DESC
LIMIT 10;
"""

top_10_movies_by_earnings = pysqldf(q2)
top_10_movies_by_earnings


# In[29]:


# Display the top domestic gross, the average rating and the number of votes of the top 10 rated movies
q2 = """
SELECT title, foreign_gross,averagerating, numvotes
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst)
ORDER BY averagerating DESC
LIMIT 10;
"""

top_10_movies_by_rating = pysqldf(q2)
top_10_movies_by_rating


# In[48]:


#Plot the genres by the total domestic gross earned and limit the entries to the top 5 items 
q3 = """
SELECT genres, SUM (domestic_gross) AS total_domestic_gross
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst)
GROUP BY genres
ORDER BY total_domestic_gross DESC
LIMIT 5;
"""

domestic_earnings_by_genres_df = pysqldf(q3)

#Plot the genres by the total Foreign gross earned and limit the entries to the top 5 items 

q5 = """
SELECT genres, SUM (foreign_gross) AS total_foreign_gross
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst)
GROUP BY genres
ORDER BY total_foreign_gross DESC
LIMIT 5;
"""

foreign_earnings_by_genres_df = pysqldf(q5)


fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize= (10,3))
domestic_earnings_by_genres_df.set_index('genres')['total_domestic_gross'].plot(kind = 'bar', ax = axes[0])
axes[0].set_title('Domestic earnings by genres')
axes[0].set_xlabel('Genres')
axes[0].set_ylabel('Domestic_gross');


foreign_earnings_by_genres_df.set_index('genres')['total_foreign_gross'].plot(kind = 'bar', color = 'red', ax = axes[1])
axes[1].set_title('Foreign earnings by genres')
axes[1].set_xlabel('Genres')
axes[1].set_ylabel('Foreign_gross');


# In[49]:


#plot a histogram to view the frequency distribution of runtimes_minutes
q4 = """
SELECT runtime_minutes
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst);
"""

runtimes_minutes_df = pysqldf(q4)

runtimes_minutes_df.plot.hist(column = 'runtime_minutes', bins = 30, color = 'red', edgecolor = 'black')
axes.set_title('Runtime')
axes.set_xlabel('runtime_minutes')
axes.set_ylabel('Frequency');


# In[50]:


#plot a bar graph to show the most popular film studios
q6 = """
SELECT COUNT (studio) AS n_studio, studio
FROM df
INNER JOIN df1
ON df.primary_title = df1.title
INNER JOIN df2
USING (tconst)
GROUP BY studio
ORDER BY n_studio DESC
LIMIT 10;
"""

popular_studio_df = pysqldf(q6)

fig, axes = plt.subplots(nrows = 1, ncols = 1, figsize= (6,4))

popular_studio_df.set_index('studio')['n_studio'].plot(kind = 'bar', ax = axes, color = 'purple')
axes.set_title('Popular Studio')
axes.set_xlabel('studio')
axes.set_ylabel('n_studio');


# In[ ]:




