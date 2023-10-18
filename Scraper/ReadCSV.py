import pandas as pd

def getCSVFile():

    print("CSV should contain two columns only")
    print("Company Name and URLs")
    inp = input('Please paste the csv filename with full path')
    print("Reading and storing data")
    data = pd.read_csv('/Users/souravs/Documents/Documents/SEM-4/Scraper/healthcare_data_sample.csv')
    return data