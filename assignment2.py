import argparse
import csv
import datetime
import logging
from py_compile import main
import urllib.request 


def download_data(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data 

def processData (csvData):
    personData = {}

    logger = logging.getLogger('assignment2')

    lines = csvData.decode('utf-8').splitlines()
    reader = csv.reader(lines)

    for lineNum, row in enumerate(reader, starter=1):

        if lineNum <= 2:
            continue

        personID = int(row[0])
        name = row[1]
        birthday = row[2]

    try:
        birthday = datetime.datetime.strptime(
            birthday, "%d/%m/%Y"
        )
        personData[personID] = (name, birthday)
    except ValueError:
        logger.error(
            "Error processing line #%d for ID #%d",
            lineNum, 
            personID
        )
    return personData


def displayPerson(id, personData):
    if id not in personData:
        print("No user found with that id")
    else:
        name, birthday = personData[id]

        print(
            "Person #%d is %s with a birhtday of %s"
            % (id, name, birthday.strftime("%Y-%m-%d"))
        )


    def main():
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--url',    
            required=True,
            help='URL to the CSV file'
        )

        args = parser.parse_args()

        try: 
            csvData = download_data(args.url)
        except Exception as e:
            print("Error downloading data:", e)
            return
        logging.basicConfig(
            filename= 'error.log',
            level=logging.ERROR,
            format='%(message)s'
        )

        personData = processData(csvData)

        while True:
            try:
                id = int(input("Enter an ID number: "))
            except ValueError:
                print("Please enter a number.")
                continue

            if id <= 0:
                break

            displayPerson(id, personData)



if __name__ == "__main__":
    main()

   
