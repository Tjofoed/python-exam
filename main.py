import pandas, math, sys

# global variables
welcomeMessage = True
currentFile = ''

def main():
    global welcomeMessage
    while(True):
        # prints out welcome message the first time the program runs
        if(welcomeMessage):
            print('\n**** Welcome to the Criminal Law, Abstraction and Unification System: C.L.A.U.S! ****')
            welcomeMessage = False
        df = (fileSetup())
        print('\n---- file successfully loaded ----')
        menu(df)


def fileSetup():
    # allows the user to select a custom csv file or the default provided
    filename = input('\nPlease enter the filename of the desired list to use for this session.\nEnter "default" to use the default list or enter "exit" to exit the program.\n')
    if(filename.lower() == 'default'):
        try:
            return readFromFile('SacramentocrimeJanuary2006.csv')
        except IOError:
            print('\n---- default file not available ----\n')
            fileSetup()
    elif(filename.lower() == 'exit'):
        print('\nThank you and goodbye.')
        sys.exit()
    else:
        try:
            # adds '.csv' to filename if user input doesn't match csv format and reads file
            if not (filename.lower().endswith('.csv')):
                filename = f'{filename}.csv'
                return readFromFile(filename)
            else:
                return readFromFile(filename)
        except IOError:
            print('\n---- invalid filename ----\n')
            # reruns method on error
            fileSetup()


def menu(df):
    # menu with options
    print('\n**** MENU ****')
    choice = input('\nPlease select one of the following options:\n1) Search for entries in current list.\n2) Find all entries within a specific radius of a point.\n3) Add new crime to current list.\n4) Export current list.\n5) Load new list file.\n0) Exit program.\n')
    # search for specific entries in current list
    if(choice == '1'):
        column = chooseColumn(df)
        searchWord = input(f'\nPlease enter desired search word(s) in the category "{column}":\n')
        # runs search method and saves as result
        result = searchInDataframe(df, column, searchWord)
        # prints out message based on search results
        if (result.empty):
            print(f'\nNo entries found with the word(s) "{searchWord}".\n')
            print('\n---- returning to menu ----\n')
            menu(df)
        else:
            print(f'\n{len(result)} Entries found matching the word(s) "{searchWord}":\n')
            print(result)
            exportResult(df, result)


    # find all entries within a specific radius of a point
    elif(choice == '2'):
        # saves user input as floats to use in the check method
        while(True):
            try:
                lat = float(input('\nPlease enter the latitude of the point:\n'))
                break
            except:
                print('\n---- invalid entry ----')
        while(True):
            try:
                lon = float(input('\nPlease enter the longitude of the point:\n'))
                break
            except:
                print('\n---- invalid entry ----')
        while(True):
            try:
                radius = float(input('\nPlease enter the radius in kilometers of the point you wish to search for (eg. "5"):\n'))
                break
            except:
                print('\n---- invalid entry ----')
        result = checkRadius(df, lat, lon, radius)
        # prints out message based on search results
        if (result.empty):
            print(f'\nNo entries found with the coordinates "latitude: {str(lat)}" "longitude: {str(lon)}" "radius: {str(radius)}km".\n')
            print('\n---- returning to menu ----\n')
            menu(df)
        else:
            print(f'\nEntries found with the coordinates "latitude: {str(lat)}" "longitude: {str(lon)}" "radius: {str(radius)}km":\n')
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
        print('\nThank you and goodbye.')
        sys.exit()
    # invalid entry
    else:
        print('\n---- invalid entry ----\n')
        menu(df)


def exportResult(df, result):
    # loops in case of invalid user input
    while(True):
        subChoice = input('\nPlease select one of the following options:\n1) Export search results.\n0) Back to menu.\n')
        if(subChoice == '1'):
            # runs file format method and saves as fileFormat
            fileFormat = chooseFileFormat()
            filename = input('\nPlease enter desired filename (eg. "mySearchFile"):\n')
            # runs write to file method with result file and returns to menu
            writeToFile(result, filename, fileFormat)
            print(f'\nFile successfully saved as "{filename}.{fileFormat}" in your data folder.')
            print('\n---- returning to menu ----\n')
            menu(df)
        elif(subChoice == '0'):
            menu(df)
        else:
            print('\n---- invalid entry ----\n')


def exportCurrentList(df):
    # runs file format method and saves as fileFormat
    fileFormat = chooseFileFormat()
    filename = input('\nPlease enter desired filename (eg. "mySearchFile"):\n')
    writeToFile(df, filename, fileFormat)
    # runs write to file method and returns to menu
    print(f'\nFile successfully saved as "{filename}.{fileFormat}" in your data folder.')
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
    # instantiating global file
    global currentFile
    # creating DataFrame object by user input converted to uppercase
    appendDf = pandas.DataFrame({'cdatetime':[input('\nPlease enter data for the category "cdatetime":\n').upper()],'address':[input('\nPlease enter data for the category "address":\n').upper()],'district':[input('\nPlease enter data for the category "district":\n').upper()],'beat':[input('\nPlease enter data for the category "beat":\n').upper()],'grid':[input('\nPlease enter data for the category "grid":\n').upper()],'crimedescr':[input('\nPlease enter data for the category "crimedescr":\n').upper()],'ucr_ncic_code':[input('\nPlease enter data for the category "ucr_ncic_code":\n').upper()],'latitude':[input('\nPlease enter data for the category "latitude":\n').upper()],'longitude':[input('\nPlease enter data for the category "longitude":\n').upper()]})
    try:
        # appending user created DataFrame object to current list
        appendDf.to_csv(f'data/{currentFile}', mode='a', header=False, index=False)
        print(f'\nSuccessfully added data to file "{currentFile}":\n')
        print(appendDf)
        print('\n---- returning to menu ----\n')
        menu(df)
    except IOError:
        print('\n---- could not add to file ----\n')
        print('\n---- returning to menu ----\n')
        menu(df)


def checkRadius(df, lat, lon, radius):
    # creating blank DataFrame object with matching columns
    radiusDf = pandas.DataFrame(columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'])
    for index, row in df.iterrows():
        # calculating the distance between parameter lat/lon and row lat/lon by the Haversine formula
        d = 2*math.asin(math.sqrt((math.sin((lat-row['latitude'])/2))**2 + math.cos(lat)*math.cos(row['latitude'])*(math.sin((lon-row['longitude'])/2))**2))
        # multiplying the distance with the earths and appending row if less than parameter
        if(d * 6371 < radius):
            radiusDf = radiusDf.append(row)
    return radiusDf


def readFromFile(filename):
    # instantiating and saving global file by parameter
    global currentFile
    currentFile = filename
    return pandas.read_csv(f'data/{filename}')


def writeToFile(df, filename, fileFormat):
    try:
        # saving files as the different formats
        if fileFormat == 'json':
            df.to_json(f'data/{filename}.json')
        elif fileFormat == 'csv':
            df.to_csv(f'data/{filename}.csv', columns=['cdatetime','address','district','beat','grid','crimedescr','ucr_ncic_code','latitude','longitude'], index=False)
        elif fileFormat == 'html':
            df.to_html(f'data/{filename}.html')
    except IOError:
        print('\n---- could not create file ----\n')
        print('\n---- returning to menu ----\n')
        menu(df)


def searchInDataframe(df, column, searchPhrase):
    # searching in file by casting as strings and searching in uppercase
    return df.loc[df[column].astype(str).str.contains(searchPhrase.upper())]


if __name__== "__main__":
    main()
