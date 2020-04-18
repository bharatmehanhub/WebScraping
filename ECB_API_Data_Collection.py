import requests   # Importing requests library to send requests and receive https responses from European Central Bank.
import pandas as pd    # Importing pandas library to


# Creating the main function.
def main():

    # Creating a base url to set start date, end date, required rates and base currency for the data we need.
    # This url is created using ECB documentation available at 'https://exchangeratesapi.io/'

    base_url='https://api.exchangeratesapi.io/history?start_at=2018-01-01&end_at=2020-03-31&symbols=EUR,GBP,INR&base=USD'

    # Receiving response by sending GET request to the base url above
    response = requests.get(base_url)

    # Applying if statement to only collect the data if case the response received is positive.
    if response.status_code == 200:

        # Parsing the textual JSON response to python dictionary using an inbuilt method .json()
        data_json = response.json()
        if type(data_json) == dict:
            data_frame = pd.read_json(response.content)

            # Separating out each of the currency value from the Dictionary
            data_frame['EUR'] = data_frame['rates'].apply(lambda x: x['EUR'])
            data_frame['INR'] = data_frame['rates'].apply(lambda x: x['INR'])
            data_frame['GBP'] = data_frame['rates'].apply(lambda x: x['GBP'])

            # Exporting the resulting data frame to a csv file which can be further cleaned
            data_frame.to_csv(r'Exchange_Rates.csv',sep=',', encoding='utf-8', index=True)
        else:

            # Printing error if the conversion of the response to Data Dictionary is not possible
            print('Sorry, seems like the response format is not as expected')

    else:
        # Printing error if the response is not received successfully.
        print('Sorry, unable to proceed as the request status code is: ', str(response.status_code))


if __name__ == '__main__':
    main()