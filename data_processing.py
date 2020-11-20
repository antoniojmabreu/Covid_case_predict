import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import folium
from folium import plugins
import csv
from fbprophet import Prophet

selected = input("Country (Default= Worldwide):\n-> ")
cdr = int(input("Predict:\n1) Confirmed\n2) Deaths\n3) Recovered\n-> "))
if selected == '':
    dataSet = 'Data2/covid_19_clean_complete.csv'
    title = 'Worldwide COVID-19 Cases'
    selected = 'Worldwide'
else:
    dataSet = 'Countries/'+selected+'.csv'
    title = selected+' COVID-19 Cases'

intervalWidhtPercent = 0.999
forecastInterval = int(input("Forecast Period\n-> "))


df = pd.read_csv(dataSet, parse_dates= ['Date'])
df.rename(columns= {'ObservationDate': 'Date', 'Country/Region': 'Country'}, inplace= True)

'''
df_confirmed = pd.read_csv('Data2/time_series_covid19_confirmed_global.csv')
df_recovered = pd.read_csv('Data2/time_series_covid19_recovered_global.csv')
df_deaths = pd.read_csv('Data2/time_series_covid19_deaths_global.csv')

df_confirmed.rename(columns= {'Country/Region': 'Country'}, inplace= True)
df_recovered.rename(columns= {'Country/Region': 'Country'}, inplace= True)
df_deaths.rename(columns= {'Country/Region': 'Country'}, inplace= True)


print(df.head())
df2 = df.groupby(["Date", "Country"])[['Date', 'Province/State', 'Country', 'Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
print(df2.head())
df2.to_csv('Data2/df2.csv')

#Exploring countryData
query = df.query('Country== "US"').groupby(["Date", "Country"])[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
print(query)
query.to_csv('Data2/query.csv')
'''

sum = df.groupby('Date')[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
sum.to_csv('Data2/indexed_data.csv')
#print(sum)

confirmed = df.groupby('Date').sum()['Confirmed'].reset_index()
recovered = df.groupby('Date').sum()['Recovered'].reset_index()
deaths = df.groupby('Date').sum()['Deaths'].reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x= confirmed['Date'], y= confirmed['Confirmed'], mode= 'lines+markers', name= 'Confirmed', line= dict(color= '#3498DB', width= 2)))
fig.add_trace(go.Scatter(x= deaths['Date'], y= deaths['Deaths'], mode= 'lines+markers', name= 'Deaths', line= dict(color= '#CB4335', width= 2)))
fig.add_trace(go.Scatter(x= recovered['Date'], y= recovered['Recovered'], mode= 'lines+markers', name= 'Recovered', line= dict(color= '#2ECC71', width= 2)))
fig.update_layout(title= title, xaxis= dict(title = 'Day', ticklen= 2, zeroline= True), yaxis= dict(title = 'Cases', ticklen= 2, zeroline= True))
fig.show()

confirmed = df.groupby('Date').sum()['Confirmed'].reset_index()
deaths = df.groupby('Date').sum()['Deaths'].reset_index()
recovered = df.groupby('Date').sum()['Recovered'].reset_index()


if cdr == 1:
    confirmed.columns = ['ds','y']
    confirmed['ds'] = confirmed['ds'].dt.date
    confirmed['ds'] = pd.to_datetime(confirmed['ds'])

    m = Prophet(interval_width= intervalWidhtPercent)
    m.fit(confirmed)
    future = m.make_future_dataframe(periods= forecastInterval)
    forecast = m.predict(future)
    #print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    forecast.to_csv('Data2/ProphetData/forecast_confirmed.csv')
    #confirmed_forecast_plot = m.plot(forecast)
    #plt.show()
    #confirmed_forecast_plot.savefig('Data2/ProphetData/fig_confirmed.png')

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(name= 'Actual Mesurment', mode= 'lines+markers', x= list(confirmed['ds']), y= list(confirmed['y']), marker= dict(color='#3498DB')))
    fig1.add_trace(go.Scatter(name= 'Upper Guide', mode= 'lines', x= list(forecast['ds']), y= list(forecast['trend_upper']), line= dict(color='#CB4335')))
    fig1.add_trace(go.Scatter(name= 'Upper Estimation', mode= 'markers', x= list(forecast['ds']), y= list(forecast['yhat_upper']), line= dict(color='#CB4335')))
    fig1.add_trace(go.Scatter(name= 'Lower Guide', mode= 'lines', x= list(forecast['ds']), y= list(forecast['trend_lower']), line= dict(color='#2ECC71')))
    fig1.add_trace(go.Scatter(name= 'Lower Estimation', mode= 'markers', x= list(forecast['ds']), y= list(forecast['yhat_lower']), line= dict(color='#2ECC71')))
    fig1.add_trace(go.Scatter(name= 'Trend Guide', mode= 'lines', x= list(forecast['ds']), y= list((forecast['trend'] + forecast['trend_lower']) / 2), line= dict(color='#34495E')))
    fig1.add_trace(go.Scatter(name= 'Trend', mode= 'markers', x= list(forecast['ds']), y= list((forecast['yhat'] + forecast['yhat_lower']) / 2), line= dict(color='#34495E')))
    fig1.update_layout(title= selected+' COVID-19 Confirmed Cases Estimation', xaxis= dict(title= 'Day', ticklen= 2, zeroline= True), yaxis= dict(title= 'Cases', ticklen= 2, zeroline= True))
    fig1.show()

    components = m.plot_components(forecast)
    plt.show()

elif cdr == 2:
    deaths.columns = ['ds','y']
    deaths['ds'] = deaths['ds'].dt.date
    deaths['ds'] = pd.to_datetime(deaths['ds'])

    m = Prophet(interval_width= intervalWidhtPercent)
    m.fit(deaths)
    future = m.make_future_dataframe(periods= forecastInterval)
    forecast = m.predict(future)
    #print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    forecast.to_csv('Data2/ProphetData/forecast_deaths.csv')
    #confirmed_forecast_plot = m.plot(forecast)
    #plt.show()
    #confirmed_forecast_plot.savefig('Data2/ProphetData/fig_deaths.png')

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(name= 'Actual Mesurment', mode= 'lines+markers',x= list(deaths['ds']), y= list(deaths['y']), marker= dict(color= '#3498DB')))
    fig1.add_trace(go.Scatter(name= 'Upper Guide', mode= 'lines', x= list(forecast['ds']), y= list(forecast['trend_upper']), line= dict(color='#CB4335')))
    fig1.add_trace(go.Scatter(name= 'Upper Estimation', mode= 'markers', x= list(forecast['ds']), y= list(forecast['yhat_upper']), line= dict(color='#CB4335')))
    fig1.add_trace(go.Scatter(name= 'Lower Guide', mode= 'lines', x= list(forecast['ds']), y= list(forecast['trend_lower']), line= dict(color='#2ECC71')))
    fig1.add_trace(go.Scatter(name= 'Lower Estimation', mode= 'markers', x= list(forecast['ds']), y= list(forecast['yhat_lower']), line= dict(color='#2ECC71')))
    fig1.add_trace(go.Scatter(name= 'Trend Guide', mode= 'lines', x= list(forecast['ds']), y= list((forecast['trend'] + forecast['trend_lower']) / 2), line= dict(color='#34495E')))
    fig1.add_trace(go.Scatter(name= 'Trend', mode= 'markers', x= list(forecast['ds']), y= list((forecast['yhat'] + forecast['yhat_lower']) / 2), line= dict(color='#34495E')))
    fig1.update_layout(title= selected+' COVID-19 Deaths Cases Estimation', xaxis= dict(title= 'Day', ticklen= 2, zeroline= True), yaxis= dict(title= 'Cases', ticklen= 2, zeroline= True))
    fig1.show()

    components = m.plot_components(forecast)
    plt.show()


elif cdr == 3:
    recovered.columns = ['ds','y']
    recovered['ds'] = recovered['ds'].dt.date
    recovered['ds'] = pd.to_datetime(recovered['ds'])

    m = Prophet(interval_width= intervalWidhtPercent)
    m.fit(recovered)
    future = m.make_future_dataframe(periods= forecastInterval)
    forecast = m.predict(future)
    #print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    forecast.to_csv('Data2/ProphetData/forecast_recovered.csv')
    #confirmed_forecast_plot = m.plot(forecast)
    #plt.show()
    #confirmed_forecast_plot.savefig('Data2/ProphetData/fig_recovered.png')

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(name= 'Actual Mesurment', mode= 'lines+markers', x= list(recovered['ds']), y= list(recovered['y']), marker= dict(color= '#3498DB')))
    fig1.add_trace(go.Scatter(name= 'Upper Guide', mode= 'lines', x= list(forecast['ds']), y= list(forecast['trend_upper']), line= dict(color='#CB4335')))
    fig1.add_trace(go.Scatter(name= 'Upper Estimation', mode= 'markers', x= list(forecast['ds']), y= list(forecast['yhat_upper']), line= dict(color='#CB4335')))
    fig1.add_trace(go.Scatter(name= 'Lower Guide', mode= 'lines', x= list(forecast['ds']), y= list(forecast['trend_lower']), line= dict(color='#2ECC71')))
    fig1.add_trace(go.Scatter(name= 'Lower Estimation', mode= 'markers', x= list(forecast['ds']), y= list(forecast['yhat_lower']), line= dict(color='#2ECC71')))
    fig1.add_trace(go.Scatter(name= 'Trend Guide', mode= 'lines', x= list(forecast['ds']), y= list((forecast['trend'] + forecast['trend_lower']) / 2), line= dict(color='#34495E')))
    fig1.add_trace(go.Scatter(name= 'Trend', mode= 'markers', x= list(forecast['ds']), y= list((forecast['yhat'] + forecast['yhat_lower']) / 2), line= dict(color='#34495E')))
    fig1.update_layout(title= selected+' COVID-19 Recovered Cases Estimation', xaxis= dict(title= 'Day', ticklen= 2, zeroline= True), yaxis= dict(title= 'Cases', ticklen= 2, zeroline= True))
    fig1.show()

    components = m.plot_components(forecast)
    plt.show()
