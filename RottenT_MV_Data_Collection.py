import pandas as pd     # Importing pandas to work with and export the data
import requests         # Importing requests library to send requests and receive https responses from RT web server
from bs4 import BeautifulSoup   # Importing Web scraping library

# Creating the main function


def main():

    #   Creating a base url where all the ratings and synopsis of top 140 movies are present.
    #   This url is taken by navigation to the page:
    #   'https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/2/'

    base_site='https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/2/'

    # Receiving response by sending GET request to the base url above.
    response = requests.get(base_site)

    # Applying if statement to only collect the data if case the response received is positive.
    if response.status_code == 200:

        # Parsing the textual html response to create a soup object using an inbuilt parser (lxml)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')

        # Saving the parsed html content as web page.
        with open('Rotten_tomatoes.html', 'wb') as file:
            file.write(soup.prettify('utf-8'))

        # Capturing all the divs that contain movie names.
        # Tag names and class names are decided by looking at the html file in editor.
        divs = soup.find_all('div', {'class': 'col-sm-18 col-full-xs countdown-item-content'})

        # Extracting all the heading 2 info as all the required data is present in this tag h2.
        headings =[div.find('h2') for div in divs]

        # Extracting all the required info from the html text

        titles = [h.find('a').text for h in headings]
        years = [int(h.find('span', class_='start-year').string.strip('()')) for h in headings]
        scores = [int(h.find('span', class_='tMeterScore').string.strip('%')) for h in headings]
        adjusted_score = [float(d.find('div', class_='countdown-adjusted-score').text.strip('Adjusted Score: %')) for d
                          in divs]
        critics_consensus = [d.find('div', class_='critics-consensus').text.strip('Critics Consensus: ') for d in divs]
        synopsis = [d.find('div', class_='synopsis').text.strip('Synopsis: ') for d in divs]
        cast = [d.find('div', class_='cast').text.strip('\nStarring: ') for d in divs]
        director = [d.find('div', class_='director').text.strip('\nDirected By: ') for d in divs]

        # Creating a Pandas data frame from all the received data
        movies_collected_data = pd.DataFrame(data=[titles,years,scores,adjusted_score,critics_consensus,synopsis,cast,director],
                                             index=['Title', 'Year of Release', 'RT Scores', 'Adjusted score' , 'Critics consensus',
                                                    'Synopsis', 'Cast', 'Director'])

        movies_collected_data = movies_collected_data.transpose()

        movies_collected_data.to_csv('Movies_Collected_Data.csv', index=False)

    else:
        # Printing error if the response is not received successfully.
        print('Sorry, unable to proceed as the request status code is: ', str(response.status_code))


if __name__ == '__main__':
    main()
