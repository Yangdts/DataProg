#!/usr/bin/env python
# coding: utf-8

# # Global Cost of Living

# ## 1. Aim, Objectives and Background

# ## 1.1 Introduction

# The cost of living is an important factor that affects the quality of life and financial well-being of individuals and families. It is influenced by a variety of factors, including the prices of goods and services, housing costs and the overall level of economic development in a particular location.
# 
# I decided to focus this research study on the various factors that influence the cost of living in different countries and cities, mainly focusing on the relationship between the average monthly salary and the different expenditures one person might have. Through this study, we can also determine the country with lowest cost of living, based on a select few factors.
# 
# The focus will be on average monthly salary as that is the source of income for all individuals and families which pays for the costs of living factors.

# ## 1.2 Aims and objectives

# To examine the correlation between the average monthly salary and average cost of living in various countries, and to assess the degree to which salary levels vary based on differences in the cost of living. 
# To provide insight into the relationship between salary and cost of living, the economic well-being of residents in different countries.
# 
# The aim of this research will be to understand the relationships between the average monthly salary and the average cost of living in different countries. The data should be cleaned to allow utilisation of techniques later. Identify trends within the data with further analysis.

# This study is relevant as the economic well-being affects every individual and might provide some insight on the relationship between salary and various cost factors. 
# 
# From a logical point of view, the average monthly salary must be sufficient for an individual to afford the costs of living in the city of residence. The analysis later in the report should support this hypothesis. 
# The research will mainly focus on the average monthly salary as a comparison to other factors in the dataset such as cost for basic necessities and food. This is because some of the data is more of an luxury compared to necessities. For example, a fitness club membership or alcohol.

# ## 2. Data

# ### 2.1 Data Requirement

# Three potential datasets were chosen. All 3 are csv data are found on (https://www.kaggle.com). The different datasets are relevant to the study objective as they provide various countries, average monthly salary in the csv data file. The contents in the datafiles differs slightly.
# 
# The datasets are from Numbeo(https://www.numbeo.com), a crowd-sourced global database, which means the data from the dataset is provided by the contributors to the global database. As written on the numbeo website, there are more than 700,000 contributors from 11,000+ cities.
# The other data is gathered from NationMaster(https://www.nationmaster.com), the data is gathered through a survey by Numbeo.com from May 2011, to February 2014. 

# #### 2.1.1 Dataset Choice

# Dataset 'Avg monthly salary' contains the country and average monthly salary but has no cost of living factors to directly compare with to find any correlation between the data.
# The other 2 dataset 'Cost_of_living_v2' and 'Cost_of_Living_Index_2022' were gathered by scraping from Numbeo's website.
# The contents differ as 'Cost_of_living_v2' provides more raw data and 'Cost_of_Living_Index_2022' uses the cost of living index that Numbeo uses, it compares the cost of living index which is relative to New York City(NYC) according to Numbeo. If the index is higher at 120%, it means that the average price is 20% higher in that country than in NYC.
# 
# 
# To choose between the 3 potential dataset, some pros and cons of each dataset will be examined.
# 
# Dataset 'Avg monthly salary'
# 
# Pros
# * Tidy and simple data
# 
# Cons
# * Does not contain a lot of data to conduct quality analysis
# 
# Dataset 'Cost_of_living_v2'
# 
# Pros
# * Lots of data for analysis
# 
# Cons
# * Not all data will be necessary for analysis
# 
# Dataset 'Cost_of_Living_Index_2022'
# 
# Pros
# * Data is good for comparision
# 
# Cons
# * Dataset might be too small

# The data that I selected for this project is 'Cost_of_living_v2', the dataset contains information about the cost of living in many countries around the world. With more raw data and more factors to choose from, we will have more freedom and be able to filter and choose which data is more relevant.

# In[1]:


#libraries used
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# ### 2.2 Data acquisition

# The data consist of various headers such as the name of the city, name of the country, meal for inexpensive restaurant, average monthly net salary (After Tax), to name a few. The csv file column header uses x1, x2 .... to represent the various types of data collected. The column headers are as shown in the table below:

# In[2]:


#To show the column header of data
table = pd.read_csv('Table.csv', index_col=0)
table


# ### 2.3 Data cleansing

# To provide a more accurate analysis, the data should be filtered. The last column in the csv file covers the data quality, the data will either be 0 or 1, the data will be 0 if Numbeo considers more contributors to the data are needed to increase data quality. 
# The csv data will be filtered according to their data quality.

# In[3]:


#Sort data by quality as determined by numbeo
df = pd.read_csv('Cost_of_living_v2.csv')
dataGoodMain = df.loc[df['data_quality']==1]
dataBadMain = df.loc[df['data_quality']==0]


# In[4]:


dataGoodAll = dataGoodMain
dataGoodAll.shape
#Number of entries with data quality of 1


# In[5]:


dataBadAll = dataBadMain
dataBadAll.shape
#Number of entries with data quality of 0


# In[6]:


#Remove last column of data as it is no longer required
#dataGoodMain will be working data set and dataGoodAll will remain with all values
dataGoodMain.drop("data_quality", inplace = True, axis = 1)
dataBadMain.drop("data_quality", inplace = True, axis = 1)


# The column data_quality is no longer necessary as the data has been sorted. Now the data consists of the city, country and only numeric values which represents different cost of living factors and the average monthly salary.

# dataGoodMain consists of the data with data quality of 1 which contains 923 entries as compared to the original 4494 entries. The previously large dataset has now been filtered to about 20% of its original size with more accurate data for further analysis. The main focus of analysis later will be on the 'good' quality data.

# #### 2.2.1 Checking for numeric data

# To check if all the data in the dataset has no non-numerical data, the code below will check and print out the columns that include non-numerical data.
# The is_numeric function converts the value into float and returns True and inputs it into the applymap() function. The function checks all columns in the dataset and returns the header of the columns with a False return. This will ensure that the data we use for plotting and analysis does not contain illegal data.

# In[7]:


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
non_numeric_columns = dataGoodMain.columns[~dataGoodMain.applymap(is_numeric).all(0)]

print(non_numeric_columns)


# #### 2.2.2 Check for null data

# To ensure that null data does not affect the analysis in any way, the null entries are removed. 

# To check for null values, the code below checks for null values in both dataGoodMain and dataBadMain. dataGoodMain represents data that has large enough contributors that Numbeo considers the data quality to be sufficient, even dataGoodMain has null values which meant that there is no data gathered even with a larger data quality. 

# ##### 2.2.2.1 Most null values

# We can determine the columns with the most number of null values with this code.

# In[8]:


dataBadMain.isnull().sum().sort_values(ascending=False)[0:5]


# The top 5 columns with null entries are Tennis Court Rent(1 Hour on Weekend) (USD) (x40), Price per Square Meter to Buy Apartment Outside of Centre (USD) (x53), Price per Square Meter to Buy Apartment in City Centre (USD) (x52), Monthly Pass (Regular Price) (USD) (x29) and International Primary School, Yearly for 1 Child (USD) (x43).

# Some logical reason could be that in specific countries some values are not applicable such as for x40, Tennis Court Rent(1 Hour on Weekend)(USD) or x43, International Primary School, Yearly for 1 Child(USD). Not all cities have a tennis court for rent or International primary school.
# Some possible reason for the large number of null values could be that in some cities and countries some categories might not be applicable or difficult to access.
# For example, some cities might not have a Tennis court or International Primary School, Not all cities have public transportation for the monthly pass as well.
# Similarly, there might not be any real estate for sale which cause x53 and x52 to be high in number.

# In[9]:


null_columns = dataGoodMain.columns[dataGoodMain.isnull().any()]
print(null_columns)


# In[10]:


null_columns = dataBadMain.columns[dataBadMain.isnull().any()]
print(null_columns)


# #### 2.2.3 Removing null values

# Null values are not helpful to the comparision between cost of living as there is no numeric value. To remove the values from the working data sets, the dropna function in pandas can be used to remove rows with null value.

# In[11]:


dataGoodMain.dropna(inplace=True)
dataGoodMain.shape


# In[12]:


dataBadMain.dropna(inplace=True)
dataBadMain.shape


# Previously, dataGoodMain.shape has (923,58) and after removing the null rows, dataGoodMain.shape returned (744,57). The number of column decreased by 1 as the data_quality column has be dropped.
# 179 rows have null entries and are removed.
# dataBadMain.shape returned (4033, 58) previously and after removing the null rows, (534,57) remain in dataBadMain.

# ## 3. Analysis

# ### 3.1 Pre-analysis information

# #### 3.1.1 Data quality

# After initial cleansing of data, we have 2 sets of data which represents the different data_quality values. Bad data quality does not necessarily mean that all the data gathered is wrong. 
# We can determine the countries with the most reliable data by counting the number of cities in the country, with respect to data quality. With this information, we can learn which country's data will be the most reliable.
# However, by counting the number of cities in the dataBadMain as well, it is shown that the most reliable data country and least reliable data country is the same. 

# In[13]:


dataGoodMain["country"].value_counts()[0:10].plot(kind='barh')
#dataGoodMain plot


# In[14]:


dataBadMain["country"].value_counts()[0:10].plot(kind='barh')
#dataBadMain plot


# This can be explained that the United States has the most number of entries which would make sense that the data represents both sides.

# In[15]:


dataquality1 = dataGoodMain['country'].value_counts()[0:5]
dataquality2 = dataBadMain['country'].value_counts()[0:5]
#Print both Highest 5 countries to show that US are on both
print(dataquality1)
print(dataquality2)


# #### 3.1.2 Average salary (x54)

# Average salary will be the main comparision between the factors, some background knowledge regarding average salary will be useful. 
# The describe function provides statistics that summarizes the central tendancy, dispersion and shape of the dataset's distribution. 

# The mean, or average, gives a sense of the central tendancy of the data and can be used to compare with other datasets or groups.
# The standard deviation measures the dispersion of data round the mean. If the value is large, there is a significant variability or diversity within the dataset. This could be due to outliers.
# The minimum and maximum value gives a sense of the range of the data within the dataset.

# In[16]:


x54_Mean = dataGoodMain['x54'].mean()#x54 mean = 1917.940941
dataGoodMain['x54'].describe()


# The city and country with the min and max value are as shown below.

# In[17]:


min_value = dataGoodMain['x54'].min()
dataGoodMain.loc[dataGoodMain['x54']==min_value , ['city','country','x54']]


# In[18]:


max_value = dataGoodMain['x54'].max()
dataGoodMain.loc[dataGoodMain['x54']==max_value , ['city','country','x54']]


# ### 3.2 Data Analysis & Visualisation

# Following the hypothesis above, the data should show that there is a proportional relationship between the average salary and the various costs of living factors. We will be plotting graphs for Meal, Inexpensive Restaurant (USD) (x1), Meal for 2 People, Mid-range Restaurant, Three-course (USD) (x2), Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment (USD) (x36) and Apartment (1 bedroom) in City Centre (USD) (x48) against the Average Monthly Net Salary (After Tax) (USD) (x54) 
# 
# As the number of entries are very large still, plotting them in a scatter plot is the most effective and readable. For the next few visualisations it will focus on the general trend of the data.

# #### 3.2.1 Meal, Inexpensive restaurant (x1) VS Average Salary (x54)

# By calculating the mean of the entries of (x1), we know the central tendancy of a meal at an inexpensive restaurant. A mean cost of 10.715(3.sf) compared to the mean salary of 1917.941(3.sf). The mean cost of a meal is significantly lower than the average monthly salary which suggest that meals are relatively affordable and may not be a significant financial burden on individuals and households.  

# In[19]:


x1_Mean = dataGoodMain['x1'].mean() 
x1_Mean #x1 mean = 10.71512096774196


# To better understand the data and trend, we use a scatter graph to see the general trend of the data. 

# In[20]:


#Code to plot graph
dataGoodMain.plot(kind='scatter', x = 'x1',y = 'x54')
plt.xlabel('Meal, Inexpensive restaurant')
plt.ylabel('Average Salary')
plt.show()


# The data trends proportionally, which means that as the average monthly salary increase, the price of a meal at an inexpensive restaurant increases as well.

# #### 3.2.2 Meal for 2, Mid-range Restaurant (x2) VS Average Salary (x54)

# (x2) has a mean cost of 48.899(3.sf) compared to the mean salary of 1917.941(3.sf). The mean cost of a meal is still lower than the average monthly salary which suggest that meals are relatively affordable and may not be a financial burden on individuals and households. 
# 
# We can also compare the mean difference between (x1) and (x2), as (x2) is a meal for 2, we can divide the mean by 2 for a fair comparision with (x1). With the difference between (x1) and (x2) we know that a meal at a mid-range restaurant is on average more than twice as expensive than at an inexpensive restaurant.

# In[21]:


x2_Mean = dataGoodMain['x2'].mean() #x2 mean = 48.898682795698896
x2_ForOne = x2_Mean/2 #x2 mean/2 = 24.449341397849448
diff_Mean = x2_ForOne - x1_Mean
diff_Mean # diff = 13.734220430107488


# Plotting of scatter graph to ensure that the trend continues.

# In[22]:


#Code to plot graph
dataGoodMain.plot(kind='scatter', x = 'x2',y = 'x54')
plt.xlabel('Meal for 2, Mid-range Restaurant')
plt.ylabel('Average Salary')
plt.show()


# The data value increases proportionally. With a higher average salary, the higher cost of meal for 2 at a Mid-range restaurant.

# #### 3.2.3 Apartment (1 bedroom) in City Centre (x48) VS Average Salary (x54)

# (x48) has a mean cost of 804.993(3.sf) compared to the average salary mean of 1917.941(3.sf). The average 1 bedroom apartment when compared to the average monthly salary is almost 42% of the entire monthly salary. This means that the average individual spends almost 42% on rent and the remaining 58% will be leftover for other expenses.

# In[23]:


x48_Mean = dataGoodMain['x48'].mean() 
x48_Mean #x48 mean = 804.9927150537643

percentage = (x48_Mean/x54_Mean)*100 #Find what percentage is x48 of x54
print(percentage) #41.97171549467612


# Plotting of scatter graph to ensure trend continues

# In[24]:


#Code to plot graph
dataGoodMain.plot(kind='scatter', x = 'x48',y = 'x54')
plt.xlabel('Apartment (1 bedroom) in City Centre')
plt.ylabel('Average Salary')
plt.show()


# The data value increases proportionally. The higher the salary, the higher the cost of an apartment.

# #### 3.2.4 Basic (Electricty,etc) (x36) VS Average Salary (x54)

# (x36) has a mean cost of 142.753(3.sf) compared to the mean monthly salary of 1917.941(3.sf). When compared in terms of percentage, basic is about 7.5% of the average monthly salary. 

# In[25]:


x36_Mean = dataGoodMain['x36'].mean() 
x36_Mean #x36 mean = 142.7525403225807

percentage1 = (x36_Mean/x54_Mean)*100 #Find what percentage is x36 of x54
print(percentage1) #7.443010224212363


# In[26]:


#Code to plot graph
dataGoodMain.plot(kind='scatter', x = 'x36',y = 'x54')
plt.xlabel('Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment (USD)')
plt.ylabel('Average Salary')
plt.show()


# The data value increase proportionally. The higher the salary, the higher the cost of basics.

# ### 3.3 Cost of living

# #### 3.3.1 Determine comparision

# After understanding that the cost of living of various factors are proportional to the average monthly salary, we can perform further analysis of the data to provide find out the cities/countries with the lowest and highest cost of living. 
# 
# To determine a baseline for the cost of living in regards to the monthly salary, we use the average monthly salary and minus the basics, 1 room apartment, and meal at an inexpensive restaurant. Based on the columns (x54)-(x48)-(x1)*60. By multiplying the meal cost by 60 we can simulate the cost of 2 meals a day in a month.
# 
# This formula for calculation does not represent the actual cost of living as each individual can choose the method to spend their money. For example, less money would be spent if the day to day meals are homecooked, instead of eating out at an inexpensive restaurant. 

# In[27]:


#calculate the cost of living
def calculate_cost(row):
    return row['x54'] - row['x48'] - row['x36'] - row['x1']*60

dataCost = dataGoodMain
#add a new column called disposable_income
dataCost['disposable_income'] = dataCost.apply(calculate_cost,axis=1)
dataCost['disposable_income'].describe()


# Based on the describe function, we find out that the average 'disposable income' is 327.288(3.sf), with a large standard deviation which means the values are more dispersed. There are cities that if they spend their monthly salary on the average cost of living, they will be in the negatives and some that will have a significant amount of 'disposable income' leftover. 
# 

# #### 3.3.2 Visualisation

# We can visual the spread of the data using a bar graph as we only have one data to compare. The graph shows the number of cities with positive 'disposable income' in green and negative in red.

# In[28]:


#Code to plot graph
#Negative values are red and positive are green
colors = ['r' if value<0 else 'g' for value in dataCost['disposable_income']]
dataCost.plot(kind='bar', x = 'city',y = 'disposable_income',color = colors,legend=False)
plt.xticks([]) #hide the x axis ticks as there are too many
plt.xlabel('Cities')
plt.ylabel('"Disposable Income"')
plt.show()


# For additional information, we can determine the city and country with the highest and lowest cost of living in regards to monthly salary.
# 
# To find out which country has the highest cost of living in regards to the monthly salary, we can use the nsmallest() function and create a table. 

# In[29]:


top_countries = dataCost.nsmallest(5,'disposable_income')
top_countries[['city','country','disposable_income']]


# Similarly, we can also find out which country has the lowest cost of living in regards to the monthly salary with the same method.

# In[30]:


top_countries = dataCost.nlargest(5,'disposable_income')
top_countries[['city','country','disposable_income']]


# We find out that Sharjah has an average 'disposable income' of -5488.66
# and on the other end of the spectrum, Zug has an average of 3649.17.

# ##### 3.3.2.1 Ethical statement

# The data showing the country and city with the lowest calculated 'disposable income' is not the actual disposable income amount and a calculated value which is an average of few selected fixed values. The information of lowest 'disposable income' is not meant for any discriminatory actions or cause harm, as the study is on averages and there is a large disparity between the data.

# ## 4. Conclusion & Critical Evaluation

# ### 4.1 Conclusion

# As written in the hypothesis, the cost of living in an area is proportional to the average monthly salary. This is because the the average monthly salary has to be able to afford the basic needs such as food, shelter and basic necessities. 

# ### 4.2 Critical evaluation

# The data and analysis used in this report is very broad as the data is large and not very specific. The analysis covers purely the average costs and might not be applicable to the extreme outliers in analysis.
# 
# The values used to compare the cost of living to monthly salary is the average value and it is important to note that there can be exceptions to this case. Not all data will follow the trend and have proportional cost of living to monthly salary. It is possible that there are cases with low monthly salary and high cost of living and vice-versa.

# ## 5. Ethical Statement

# ### 5.1 Use/reuse of data and derived data

# All of the data from this study is from Numbeo and free to use.
# 
# According to Numbeo's terms of use, licensing of content states that:
# 
# "Use, reuse, and distribution of Numbeo's content in newspapers, journals, books, radio broadcasting, TV broadcasting, and academic usages (such as thesis and journal articles) are allowed under this or other licenses, under the term that if you reuse our data, you must give appropriate credit. Appropriate credit is a link back to Numbeo.com or a reference format in journal articles and books."
# 
# The data is all free of use and public so no anonymisation is required. The analysis and conclusions reached are my own.

# ### 5.2 Potential bias
# The number of entries for US is significantly more than the rest of the countries. The average in the data analysis will be skewed towards the average of US data. When working with the data, the average of all entries have been used and not specifically entries for US.

# In[31]:


df['country'].value_counts()[0:5]


# ### 5.3 Potential impacts
# I believe that the data utilised have no/minimal potential to harm. The data used is mostly numerical and used purely for the data analysis.
# 

# # 6 References & Resources used

# Cost of living (no date) Cost of Living. Available at: https://www.numbeo.com/cost-of-living/ (Accessed: January 1, 2023).
# 
# Piedade, M. (2022) Global cost of living, Kaggle. Available at: https://www.kaggle.com/datasets/mvieira101/global-cost-of-living (Accessed: January 1, 2023).
# 
# Zinovei, A. (2019) Average monthly salary after taxes by country, Kaggle. Available at: https://www.kaggle.com/datasets/zinovadr/average-monthly-salary-after-taxes-by-country?select=After%2Btax%2Bplus%2Byear%2Bgross.csv (Accessed: January 1, 2023). 
# 
# Hore, A. (2022) Cost of living index 2022, Kaggle. Available at: https://www.kaggle.com/datasets/ankanhore545/cost-of-living-index-2022 (Accessed: January 1, 2023). 
# 
# DataFrame# (no date) DataFrame - pandas 1.5.2 documentation. Available at: https://pandas.pydata.org/docs/reference/frame.html (Accessed: January 1, 2023). 
