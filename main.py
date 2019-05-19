import pandas, math, sys

welcomeMessage = True
currentFile = ''

def main():
    global welcomeMessage
    while(True):
        if(welcomeMessage):
            print('\n#### Welcome to the Criminal Law, Abstraction and Unification System: C.L.A.U.S! ####')
            welcomeMessage = False
        df = (fileSetup())
        print('\n---- file successfully loaded ----')
        menu(df)


def fileSetup():
    global currentFile
    filename = input('\nPlease enter the filename of the desired list to use for this session.\nEnter "default" to use the default list or enter "exit" to exit the program.\n')
    if(filename == 'default' or filename == 'Default'):
        try:
            return readFromFile('SacramentocrimeJanuary2006.csv')
        except IOError:
            print('\n---- default file not available ----\n')
            fileSetup()
    elif(filename == 'exit' or filename == 'Exit'):
        print('Thank you and goodbye')
        sys.exit()
    else:
        try:
            if(filename[-4:] != '.csv'):
                filename = filename+'.csv'
                currentFile = filename
                return readFromFile(filename)
            else:
                currentFile = filename
                return readFromFile(filename)
        except IOError:
            print('\n---- invalid filename ----\n')
            fileSetup()


def menu(df):
    print('\n**** MENU ****')
    choice = input('\nPlease select one of the following options:\n1) Search for entries in current list.\n2) Find all entries within a specific radius of a point.\n3) Add new crime to current list.\n4) Export current list.\n5) Load new list file.\n0) Exit program.\n')
    # search for specific entries in current list
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
            exportResult(df, result)


    # find all entries within a specific radius of a point
    elif(choice == '2'):
        lat = float(input('\nPlease enter the latitude of the point:\n'))
        lon = float(input('\nPlease enter the longitude of the point:\n'))
        radius = float(input('\nPlease enter the radius in kilometers of the point you wish to search for (eg. "5"):\n'))
        result = checkRadius(df, lat, lon, radius)
        # checkRadius(df, 38.55, -121.41, 5)
        if (result.empty):
            print('\nNo entries found with the coordinates "latitude: '+str(lat)+'" "longitude: '+str(lon)+'" "radius: '+str(radius)+'".\n')
            print('\n---- returning to menu ----\n')
            menu(df)
        else:
            print('\nEntries found with the coordinates "latitude: '+str(lat)+'" "longitude: '+str(lon)+'" "radius: '+str(radius)+'":\n')
            print(result)
            exportResult(df, result)


    # add new crime to current list
    elif(choice == '3'):
        appendToFile(df)
    # export current list
    elif(choice == '4'):
        exportCurrentList(df)
    # load new list file
    elif(choice == '5'):
        main()
    # exit program
    elif(choice == '0'):
        print('Thank you and goodbye')
        sys.exit()
    # invalid entry
    else:
        print('\n---- invalid entry ----\n')
        menu(df)


def exportResult(df, result):
    while(True):
                subChoice = input('\nPlease select one of the following options:\n1) Export search results.\n0) Back to menu.\n')
                if(subChoice == '1'):
                    fileFormat = chooseFileFormat()
                    filename = input('\nPlease enter desired filename (eg. "mySearchFile"):\n')
                    writeToFile(result, filename, fileFormat)
                    print('\nFile successfully saved as "'+filename+'.'+fileFormat+'" in your data folder.')
                    print('\n---- returning to menu ----\n')
                    menu(df)
                elif(subChoice == '0'):
                    menu(df)
                else:
                    print('\n---- invalid entry ----\n')


def exportCurrentList(df):
    fileFormat = chooseFileFormat()
    filename = input('\nPlease enter desired filename (eg. "mySearchFile"):\n')
    writeToFile(df, filename, fileFormat)
    print('\nFile successfully saved as "'+filename+'.'+fileFormat+'" in your data folder.')
    print('\n---- returning to menu ----\n')
    menu(df)


def chooseFileFormat():
    while(True):
        Choice = input('\nPlease select the desired file format:\n1) CSV.\n2) JSON.\n3) HTML.\n')
        # csv
        if(Choice == '1'):
            return 'csv'
        # json
        elif(Choice == '2'):
            return 'json'
        # html
        elif(Choice == '3'):
            return 'html'
        # invalid entry
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


def appendToFile(df):
    global currentFile
    appendDf = pandas.DataFrame({'cdatetime':[input('\nPlease enter data for the category "cdatetime":\n')],'address':[input('\nPlease enter data for the category "address":\n')],'district':[input('\nPlease enter data for the category "district":\n')],'beat':[input('\nPlease enter data for the category "beat":\n')],'grid':[input('\nPlease enter data for the category "grid":\n')],'crimedescr':[input('\nPlease enter data for the category "crimedescr":\n')],'ucr_ncic_code':[input('\nPlease enter data for the category "ucr_ncic_code":\n')],'latitude':[input('\nPlease enter data for the category "latitude":\n')],'longitude':[input('\nPlease enter data for the category "longitude":\n')]})
    try:
        appendDf.to_csv('data/'+currentFile, mode='a', header=False, index=False)
        print('\nSuccessfully added data to file "'+currentFile+'":\n'+appendDf)
        print('\n---- returning to menu ----\n')
        menu(df)
    except IOError:
        print('\n---- could not add to file ----\n')
        print('\n---- returning to menu ----\n')
        menu(df)


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
    try:
        if fileFormat == 'json':
            df.to_json('data/'+filename +'.json')
        elif fileFormat == 'csv':
            df.to_csv('data/'+filename +'.csv', columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'], index=False)
        elif fileFormat == 'html':
            df.to_html('data/'+filename +'.html')
    except IOError:
        print('\n---- could not create file ----\n')
        print('\n---- returning to menu ----\n')
        menu(df)


def searchInDataframe(df, column, searchPhrase):
    return df.loc[df[column].astype(str).str.contains(searchPhrase.upper())]


if __name__== "__main__":
    main()
