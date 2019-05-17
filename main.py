import pandas
import math, os, sys


def main():
    os.chdir('./python-exam') # TODO remove
    print('Welcome to the Criminal Law, Abstraction and Unification System: C L A U S!')


    df = (fileSetup())
    print('\n---- file successfully loaded ----')
    menu(df)

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

def fileSetup():
    df = input('\nPlease enter the filename of the desired list. (enter "default" to use the default list)\n')
    if(df == 'default' or df == 'Default'):
        try:
            return readFromFile('SacramentocrimeJanuary2006.csv')
        except IOError:
            print('\n---- default file not available ----\n')
            fileSetup()
    else:
        try:
            if(df[-4:] != '.csv'):
                df = df+'.csv'
                return readFromFile(df)
            else:
                return readFromFile(df)
        except IOError:
            print('\n---- invalid filename ----\n')
            fileSetup()


def menu(df):
    print('\n**** MENU ****')
    choice = input('\nPlease select one of the following options:\n1) Search for a specific crime in a list.\n2) Find all crimes committed within a specific radius of a point.\n3) Add new crime to an existing list.\n4) Export current list.\n5) Change list file.\n0) Exit.\n')

    # Search for a specific crime in a list
    if(choice == '1'):
        arg1 = input()
        arg2 = input()
        arg3 = input()
        searchInDataframe(df, 'address', 'OCCIDENTAL')

    # Find all crimes committed within a specific radius of a point
    elif(choice == '2'):
        arg1 = input()

    # Add new crime to an existing list
    elif(choice == '3'):
        arg1 = input()

    # Export current list
    elif(choice == '4'):
        arg1 = input()

    # Change list file
    elif(choice == '5'):
        main()

    # Exit
    elif(choice == '0'):
        sys.exit('Thank you and goodbye')

    else:
        print('\n---- invalid entry ----\n')
        menu(df)


def appendToFile(filename):
    appendDf = pandas.DataFrame({'cdatetime':['test'],'address':['test'],'district':['test'],'beat':['test'],'grid':['test'],'crimedescr':['test'],'ucr_ncic_code':['test'],'latitude':['test'],'longitude':['test']})
    appendDf.to_csv(filename, mode='a', header=False)



def checkRadius(df, lat, lon, radius):
    radiusDf = pandas.DataFrame(columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'])

    for index, row in df.iterrows():
        d = 2*math.asin(math.sqrt((math.sin((lat-row['latitude'])/2))**2 + math.cos(lat)*math.cos(row['latitude'])*(math.sin((lon-row['longitude'])/2))**2))
        if(d * 6371 < radius):
            radiusDf = radiusDf.append(row)
    radiusDf.to_csv('data/radiusdataframe.csv', index=False)
    return radiusDf



def readFromFile(filename):
    return pandas.read_csv('data/'+filename, encoding="latin1")



def writeToFile(df, filename, format):
    if format == 'json':
        df.to_json('data/'+filename +'.json')
    elif format == 'csv':
        df.to_csv('data/'+filename +'.csv', columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'], index=False)
    elif format == 'html':
        df.to_html('data/'+filename +'.html', index=False)



def searchInDataframe(df, column, searchPhrase):
    return df.loc[df[column].str.contains(searchPhrase)]



if __name__== "__main__":
  main()
