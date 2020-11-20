import numpy as np
import pandas as pd
import plotly.express as px
import calmap
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')


full_table = pd.read_csv('Data2/covid_19_clean_complete.csv', parse_dates=['Date'])
full_grouped = full_table.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()

temp = full_grouped.groupby(['Country/Region', 'Date', ])['Confirmed', 'Deaths', 'Recovered']
temp = temp.sum().diff().reset_index()
mask = temp['Country/Region'] != temp['Country/Region'].shift(1)

temp.loc[mask, 'Confirmed'] = np.nan
temp.loc[mask, 'Deaths'] = np.nan
temp.loc[mask, 'Recovered'] = np.nan
temp.columns = ['Country/Region', 'Date', 'New cases', 'New deaths', 'New recovered']

full_grouped = pd.merge(full_grouped, temp, on=['Country/Region', 'Date'])
full_grouped = full_grouped.fillna(0)
cols = ['New cases', 'New deaths', 'New recovered']
full_grouped[cols] = full_grouped[cols].astype('int')
full_grouped['New cases'] = full_grouped['New cases'].apply(lambda x: 0 if x<0 else x)

# table
day_wise = full_grouped.groupby('Date')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()

# number cases per 100 cases
day_wise['Deaths / 100 Cases'] = round((day_wise['Deaths']/day_wise['Confirmed'])*100, 2)
day_wise['Recovered / 100 Cases'] = round((day_wise['Recovered']/day_wise['Confirmed'])*100, 2)
day_wise['Deaths / 100 Recovered'] = round((day_wise['Deaths']/day_wise['Recovered'])*100, 2)

# no. of countries
day_wise['No. of countries'] = full_grouped[full_grouped['Confirmed']!=0].groupby('Date')['Country/Region'].unique().apply(len).values

# fillna by 0
cols = ['Deaths / 100 Cases', 'Recovered / 100 Cases', 'Deaths / 100 Recovered']
day_wise[cols] = day_wise[cols].fillna(0)

day_wise.head()


temp = full_table[full_table['Date'] == max(full_table['Date'])]


fig = px.choropleth(full_grouped, locations="Country/Region", locationmode='country names', color=np.log(full_grouped["Confirmed"]),
                    hover_name="Country/Region", animation_frame=full_grouped["Date"].dt.strftime('%Y-%m-%d'),
                    title='Cases over time', color_continuous_scale=px.colors.sequential.Blues)
fig.update(layout_coloraxis_showscale=False)
fig.show()

fig_a = px.choropleth(full_grouped, locations="Country/Region", locationmode='country names',
                      color=np.log(full_grouped["Confirmed"]), hover_name="Country/Region", hover_data=['Confirmed'])

temp = full_grouped[full_grouped['Deaths']>0]
fig_b = px.choropleth(temp, locations="Country/Region", locationmode='country names',
                      color=np.log(temp["Deaths"]), hover_name="Country/Region", hover_data=['Deaths'])

temp = full_grouped[full_grouped['Recovered']>0]
fig_c = px.choropleth(temp, locations="Country/Region", locationmode='country names',
                      color=np.log(temp["Recovered"]), hover_name="Country/Region", hover_data=['Recovered'])

# Plot
fig = make_subplots(rows=1, cols=3, subplot_titles = ['Confirmed', 'Deaths', 'Recovered'],
                    specs=[[{"type": "choropleth"}, {"type": "choropleth"}, {"type": "choropleth"}]])

fig.add_trace(fig_a['data'][0], row=1, col=1)
fig.add_trace(fig_b['data'][0], row=1, col=2)
fig.add_trace(fig_c['data'][0], row=1, col=3)

fig.update(layout_coloraxis_showscale=False)
fig.show()

cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801'


# ===============================

fig_1 = px.line(day_wise, x="Date", y="Deaths / 100 Cases", color_discrete_sequence = [dth])
fig_2 = px.line(day_wise, x="Date", y="Recovered / 100 Cases", color_discrete_sequence = [rec])
fig_3 = px.line(day_wise, x="Date", y="Deaths / 100 Recovered", color_discrete_sequence = ['#333333'])

fig = make_subplots(rows=1, cols=3, shared_xaxes=False,
                    subplot_titles=('Deaths / 100 Cases', 'Recovered / 100 Cases', 'Deaths / 100 Recovered'))

fig.add_trace(fig_1['data'][0], row=1, col=1)
fig.add_trace(fig_2['data'][0], row=1, col=2)
fig.add_trace(fig_3['data'][0], row=1, col=3)

fig.update_layout(height=480)
fig.show()

# ===================================

fig_d = px.bar(day_wise, x="Date", y="New cases", color_discrete_sequence = [act])
fig_e = px.bar(day_wise, x="Date", y="No. of countries", color_discrete_sequence = [dth])

fig = make_subplots(rows=1, cols=2, shared_xaxes=False, horizontal_spacing=0.1,
                    subplot_titles=('No. of new cases everyday', 'No. of countries'))

fig.add_trace(fig_d['data'][0], row=1, col=1)
fig.add_trace(fig_e['data'][0], row=1, col=2)

fig.update_layout(height=480)
fig.show()
