#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')

#there is still a lot to change on this sode right here 
#part 1: get the data
df = pd.read_csv('C:/Users/Don Krieg/Documents/simple_trading/trading/BAC.csv')
df.columns = df.columns.str.strip()
df


# In[3]:


#part 2: calculate the inputs that go into the model like the 200 sma and 50 sma
df['% change'] = df['Close'].pct_change()
df['200 sma'] = df['Close'].rolling(window=200).mean().round(5)
df['50 sma'] = df['Close'].rolling(window=50).mean().round(5)
df


# In[4]:


#part 3: models' criteria
df['Criteria 1'] = df['Close'] >= df['200 sma']
df['Criteria 2'] = (df['50 sma'] >= df['200 sma']) | df['Criteria 1']  == True
df


# In[5]:


#part 4: calculate models
df['Buy and Hold'] = 100*(1+df['% change']).cumprod()
df['200 sma'] = 100*(1+df['Criteria 1'].shift(1)*df['% change']).cumprod()
df['200 sma + crossover model'] = 100*(1+df['Criteria 2'].shift(1)*df['% change']).cumprod()
df


# In[11]:


#part 5: Calculate the models return

#200 sma model's return
start_model1 = df['200 sma'].iloc[200]
end_model1 = df['200 sma'].iloc[-1]
years = (df['200 sma'].count()+1-200)/253
model1_average_return = (end_model1/start_model1)**(1/years)-1
print('200 sma model yields an average of', model1_average_return*100, '% per year')

#200 sma + crossover model's returns
start_model2 = df['200 sma + crossover model'].iloc[200]
end_model2 = df['200 sma + crossover model'].iloc[-1]
model2_average_return = (end_model2/start_model2)**(1/years)-1
print('200 sma + crossover model yields an average of', model2_average_return*100, '% per year')

#buy and hold's returns
start_spx = df['Close'].iloc[200]
end_spx = df['Close'].iloc[-1]
spx_average_return = (end_spx/start_spx)**(1/years)-1
print('Buy and Hold yields an average of', spx_average_return*100, '% per year')


# In[16]:


#part 6: plot the models
df[['Buy and Hold', '200 sma', '200 sma + crossover model']].plot(grid=True, kind='line', title='Different Models', logy=True)


# In[ ]:




