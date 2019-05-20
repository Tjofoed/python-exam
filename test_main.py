import unittest, pandas, json
import main

class test_main(unittest.TestCase):

    def setUp(self):
        pass

    # returns True if main.welcomeMessage is True
    def test_welcomeMessage(self):
        self.assertTrue(main.welcomeMessage)

    # returns True if method returns a DataFrame object
    def test_dataFrame(self):
        self.assertTrue(isinstance(main.readFromFile('SacramentocrimeJanuary2006.csv'), pandas.DataFrame))

    # returns True if currentFile equals the name of the loaded file after readFromFile method call
    def test_currentFile(self):
        main.readFromFile('SacramentocrimeJanuary2006.csv')
        self.assertEqual(main.currentFile, 'SacramentocrimeJanuary2006.csv')

    # returns True if method returns a DataFrame object with the shape of (11, x)
    def test_radius(self):
        self.assertEqual(main.checkRadius(main.readFromFile('SacramentocrimeJanuary2006.csv'), 38.55, -121.41, 10).shape[0], 11)

    # returns True if file saved as .json can load as json object
    def test_json(self):
        main.writeToFile(main.readFromFile('SacramentocrimeJanuary2006.csv'), 'jsontest', 'json')
        self.assertTrue(json.load(open('data/jsontest.json')))


if __name__ == '__main__':
    # ignoring warning for ResourceWarning on test_json
    unittest.main(warnings='ignore')