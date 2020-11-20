import pandas as pd
import wget
# remove existing fil
# --------

conf_df = pd.read_csv('Data2/time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv('Data2/time_series_covid19_deaths_global.csv')
recv_df = pd.read_csv('Data2/time_series_covid19_recovered_global.csv')


# conf_df.head()
# deaths_df.head()
# recv_df.head()
conf_df.columns
# deaths_df.columns
# recv_df.columns
conf_df.columns[4:]
dates = conf_df.columns[4:]

conf_df_long = conf_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                            value_vars=dates, var_name='Date', value_name='Confirmed')

deaths_df_long = deaths_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                            value_vars=dates, var_name='Date', value_name='Deaths')

recv_df_long = recv_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                            value_vars=dates, var_name='Date', value_name='Recovered')

recv_df_long = recv_df_long[recv_df_long['Country/Region']!='Canada']

print(conf_df_long.shape)
print(deaths_df_long.shape)
print(recv_df_long.shape)
# full_table = pd.concat([conf_df_long, deaths_df_long['Deaths'], recv_df_long['Recovered']],
#                        axis=1, sort=False)

full_table = pd.merge(left=conf_df_long, right=deaths_df_long, how='left',
                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
full_table = pd.merge(left=full_table, right=recv_df_long, how='left',
                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])

full_table.head()
full_table.shape
full_table.isna().sum()
full_table[full_table['Recovered'].isna()]['Country/Region'].value_counts()
full_table[full_table['Recovered'].isna()]['Date'].value_counts()
full_table['Recovered'] = full_table['Recovered'].fillna(0)
full_table['Recovered'] = full_table['Recovered'].astype('int')
full_table.isna().sum()
# renaming
# ========

# renaming countries, regions, provinces
full_table['Country/Region'] = full_table['Country/Region'].replace('Korea, South', 'South Korea')
# removing
# =======
# removing county wise data to avoid double counting
full_table = full_table[full_table['Province/State'].str.contains(',')!=True]
full_table.to_csv('Data2/covid_19_clean_complete.csv', index=False)
