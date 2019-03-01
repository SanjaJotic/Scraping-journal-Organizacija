from requests import get
from bs4 import BeautifulSoup
import os
no = 1
dir = os.getcwd()

response = get('http://organizacija.fov.uni-mb.si/index.php/organizacija/issue/archive')
html_soup = BeautifulSoup(response.text, 'html.parser')

links = html_soup.find_all('div', attrs={'id':'issue'})
for link in links:
    link_na = link.find('a').get('href')

    response2 = get(link_na)
    html = BeautifulSoup(response2.text, 'html.parser')
    radovi = html.find_all('td', class_ = 'tocTitle')

    for rad in radovi:
        if rad.find('a') is not None:
            link_na_rad = rad.find('a').get('href')

            response3 = get(link_na_rad)
            html_rad = BeautifulSoup(response3.text, 'html.parser')

            autor = html_rad.find('div', attrs={'id': 'authorString'}).text.replace('\n','').replace('\t','').replace(' ,', ',').replace('  ', ' ').strip('\n').lstrip().rstrip()
            naslov = "rad" + str(no)
            no += 1

            with open(dir + "\\autori.txt", "a+", encoding="utf-8") as f:
                f.write(naslov + "|" + autor + "\n")

            pdf_link = html_rad.find('a', class_ = 'file').get('href')
            pregled_pdfa = get(pdf_link)
            html_pdf = BeautifulSoup(pregled_pdfa.text, 'html.parser')

            if html_pdf.find('a', class_ = 'action') is not None:
                download_link = html_pdf.find('a', class_ = 'action').get('href')

                # downloading pdfs
                pdf = get(download_link)
                if pdf is not None:
                    with open(dir + "\\radovi\\" + naslov + '.pdf', 'wb') as f:
                        f.write(pdf.content)
                else:
                    with open(dir + "\\radovi\\" + naslov + '.pdf', 'wb') as f:
                        f.write(pregled_pdfa.content)
