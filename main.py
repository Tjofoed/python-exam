import pandas
import math

def main():
    df = readFromFile('SacramentocrimeJanuary2006.csv')

    print('Welcome! Please enter:')
    print(menu(input()))

    # --- search for crimes based on the data
    # searchInDataframe(df, 'address', 'OCCIDENTAL')

    # --- take lon-lat point and return list of crimes within 5km
    # checkRadius(df, 38.55, -121.41, 5)


    # --- be able to add new record to file
    # appendToFile('radiusdataframe.csv')

    # --- export dataset to json and html
    # writeToFile(df, 'json')
    # writeToFile(df, 'csv')
    # writeToFile(df, 'html')

    # --- export search results to json and html
    # writeToFile(df, 'SacramentocrimeJanuary2006_modified', 'json')
    # writeToFile(df, 'SacramentocrimeJanuary2006_modified', 'csv')
    # writeToFile(df, 'SacramentocrimeJanuary2006_modified', 'html')



def menu(input):
    return {
        'a': 'you have chosen "a"! now enter something else',
        'b': 2,
        '0': 'you suck'
    }.get(input, 'error')



def appendToFile(filename):
    appendDf = pandas.DataFrame({'cdatetime':['test'],'address':['test'],'district':['test'],'beat':['test'],'grid':['test'],'crimedescr':['test'],'ucr_ncic_code':['test'],'latitude':['test'],'longitude':['test']})
    appendDf.to_csv(filename, mode='a', header=False)



def checkRadius(df, lat, lon, radius):
    radiusDf = pandas.DataFrame(columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'])

    for i, row in df.iterrows():
        d = 2*math.asin(math.sqrt((math.sin((lat-row['latitude'])/2))**2 + math.cos(lat)*math.cos(row['latitude'])*(math.sin((lon-row['longitude'])/2))**2))
        if(d * 6371 < radius):
            radiusDf = radiusDf.append(row)
    radiusDf.to_csv('radiusdataframe.csv', index=False)
    return radiusDf



def readFromFile(filename):
    return pandas.read_csv(filename)



def writeToFile(df, filename, format):
    if format == 'json':
        df.to_json(filename +'.json')
    elif format == 'csv':
        df.to_csv(filename +'.csv', columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'], index=False)
    elif format == 'html':
        df.to_html(filename +'.html', index=False)



def searchInDataframe(df, column, searchPhrase):
    return df.loc[df[column].str.contains(searchPhrase)]



if __name__== "__main__":
  main()
