import pandas, math, os, sys

welcomeMessage = True

def main():
    global welcomeMessage
    if(welcomeMessage):
        print('Welcome to the Criminal Law, Abstraction and Unification System: C.L.A.U.S!')
        welcomeMessage = False


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
    df = input('\nPlease enter the filename of the desired list.\nEnter "default" to use the default list or enter "exit" to exit the program.\n')
    if(df == 'default' or df == 'Default'):
        try:
            return readFromFile('SacramentocrimeJanuary2006.csv')
        except IOError:
            print('\n---- default file not available ----\n')
            fileSetup()
    elif(df == 'exit' or df == 'Exit'):
        print('Thank you and goodbye')
        sys.exit()
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
    choice = input('\nPlease select one of the following options:\n1) Search for specific crimes in current list.\n2) Find all crimes committed within a specific radius of a point.\n3) Add new crime to current list.\n4) Export current list.\n5) Load new list file.\n0) Exit program.\n')

    # Search for specific crimes in current list
    if(choice == '1'):
        column = chooseColumn(df)
        searchWord = input('\nPlease enter desired search word(s) in the category "'+column+'":\n')
        result = searchInDataframe(df, column, searchWord)

        if (result.empty):
            print('\nNo entries found with the word(s) "'+searchWord+'".\n')
            print('\n---- returning to menu ----\n')
            menu(df)
        else:
            print('\nEntries found matching the word(s) "'+searchWord+'":\n')
            print(result)
            while(True):
                subChoice = input('\nPlease select one of the following options:\n1) Export search results.\n2) Back to menu.\n')
                if(subChoice == '1'):
                    fileFormat = chooseFileFormat()
                    filename = input('\nPlease enter desired filename (eg. "mySearchFile"):\n')
                    writeToFile(result, filename, fileFormat)
                    print('\nFile successfully saved as "'+filename+'.'+fileFormat+'" in your data folder')
                    print('\n---- returning to menu ----\n')
                    menu(df)
                elif(subChoice == '2'):
                    menu(df)
                else:
                    print('\n---- invalid entry ----\n')


    # Find all crimes committed within a specific radius of a point
    elif(choice == '2'):
        arg1 = input()

    # Add new crime to current list
    elif(choice == '3'):
        arg1 = input()

    # Export current list
    elif(choice == '4'):
        arg1 = input()

    # Load new list file
    elif(choice == '5'):
        main()

    # Exit program
    elif(choice == '0'):
        print('Thank you and goodbye')
        sys.exit()

    # Invalid entry
    else:
        print('\n---- invalid entry ----\n')
        menu(df)


def chooseFileFormat():
    while(True):
        Choice = input('\nPlease select the desired format:\n1) CSV.\n2) JSON.\n3) HTML.\n')
        if(Choice == '1'):
            return 'csv'
        elif(Choice == '2'):
            return 'json'
        elif(Choice == '3'):
            return 'html'
        else:
            print('\n---- invalid entry ----\n')



def chooseColumn(df):
    choice = input('\nPlease select one of the following categories to search in:\n1) cdatetime.\n2) address.\n3) district.\n4) beat.\n5) grid.\n6) crimedescr.\n7) ucr_ncic_code.\n8) latitude.\n9) longitude.\n0) Back to menu.\n')

    # cdatetime
    if(choice == '1'):
        return 'cdatetime'

    # address
    elif(choice == '2'):
        return 'address'

    # district
    elif(choice == '3'):
        return 'district'

    # beat
    elif(choice == '4'):
        return 'beat'

    # grid
    elif(choice == '5'):
        return 'grid'

    # crimedescr
    elif(choice == '6'):
        return 'crimedescr'

    # ucr_ncic_code
    elif(choice == '7'):
        return 'ucr_ncic_code'

    # latitude
    elif(choice == '8'):
        return 'latitude'

    # longitude
    elif(choice == '9'):
        return 'longitude'

    # back
    elif(choice == '0'):
        print('\n---- returning to menu ----')
        menu(df)

    # invalid entry
    else:
        print('\n---- invalid entry ----\n')
        chooseColumn(df)



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



def writeToFile(df, filename, fileFormat):
    if fileFormat == 'json':
        df.to_json('data/'+filename +'.json')
    elif fileFormat == 'csv':
        df.to_csv('data/'+filename +'.csv', columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'], index=False)
    elif fileFormat == 'html':
        df.to_html('data/'+filename +'.html')



def searchInDataframe(df, column, searchPhrase):
    return df.loc[df[column].str.contains(searchPhrase.upper())]



if __name__== "__main__":
    main()
