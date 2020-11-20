import csv

def openDataFile():
    fileData = []
    with open('Data2/covid_19_clean_complete.csv', newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)

        dates = []
        daysSince = -1
        timeStamps = []

        for row in csvReader:
            fileData.append(row)


    for row in fileData:
        if row[4] not in dates:
            dates.append(row[4])


    cleanData = []
    for date in dates:

        print(date)
        processed = []
        daysSince+= 1
        for i in range(len(fileData)):
            if fileData[i][4] == date:
                if fileData[i][1] not in processed:
                    province = ''
                    country = fileData[i][1]
                    processed.append(country)
                    lat = fileData[i][2]
                    long = fileData[i][3]
                    conf = 0
                    death = 0
                    recov = 0

                    for j in range(i, len(fileData)):
                        if fileData[j][1] == country and fileData[j][4] == date:
                            conf+= int(fileData[j][5])
                            if fileData[j][6] == '':
                                death+= 0
                            else:
                                death+= int(float(fileData[j][6]))
                            recov+= int(fileData[j][7])

                    cleanData.append([province, country, lat, long, date, str(conf), str(death), str(recov)])


    with open('Data2/data_by_country.csv', mode='w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerow(['Province/State', 'Country/Region', 'Lat', 'Long', 'Date', 'Confirmed', 'Deaths', 'Recovered'])
        for row in cleanData:
            csvWriter.writerow(row)

    return cleanData, processed


def splitByCountrySave(countries, cleanData):
    for country in countries:
        print(country)
        with open('Countries/' + country + '.csv', mode='w') as csvfile:
            csvWriter = csv.writer(csvfile, delimiter=',')

            csvWriter.writerow(['Province/State', 'Country/Region', 'Lat', 'Long', 'Date', 'Confirmed', 'Deaths', 'Recovered'])

            for i in range(len(cleanData)):
                if country == cleanData[i][1]:
                    csvWriter.writerow(cleanData[i])


if __name__== "__main__":

    cleanData, countries = openDataFile()
    splitByCountrySave(countries, cleanData)
