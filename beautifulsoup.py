import sys
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import xlsxwriter

url = str(sys.argv[1])
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

movie_name = soup.find('h1', attrs = {'data-testid': 'hero-title-block__title'}).text

year = soup.find('span', attrs = {'class': 'TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex'}).text

rating = soup.find('span', attrs = {'class': 'AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'}).text

director = soup.find('a', attrs = {'class': 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'}).text

actors = []
actors_data = soup.findAll('div', attrs = {'data-testid': 'title-cast-item'})
for stored in actors_data:
    aTags = stored.findAll('a', attrs = {'data-testid': 'title-cast-item__actor'})
    for tags in aTags:
        actors.append(tags.text)


workbook = xlsxwriter.Workbook("movie.csv", {'strings_to_numbers': True})

bold_format = workbook.add_format({'bold': True})

cell_format = workbook.add_format()
cell_format.set_text_wrap()
cell_format.set_align('top')
cell_format.set_align('left=')

worksheet = workbook.add_worksheet(movie_name)

worksheet.write('A1', 'Movie Name', bold_format)
worksheet.write('A2', movie_name, cell_format)
worksheet.write('B1', 'Release', bold_format)
worksheet.write('B2', year, cell_format)
worksheet.write('C1', 'IMDB Rating', bold_format)
worksheet.write('C2', rating, cell_format)
worksheet.write('D1', 'Director', bold_format)
worksheet.write('D2', director, cell_format)
worksheet.write('E1', 'Actors', bold_format)
for i in range(len(actors)):
    worksheet.write('E'+str(i+2), actors[i], cell_format)

worksheet.set_column(0, 4, width=20)

workbook.close()

