import requests
from bs4 import BeautifulSoup


url = r'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
ClassNameToExtract = r'wikitable sortable static-row-numbers plainrowheaders srn-white-background'
DataNameToExtract = r'static-row-header'


table = soup.find("table", {"class":ClassNameToExtract})

print(   table      )

# if table:
#     # Extraer los encabezados
#     headers = [th.text.strip() for th in table.find_all("th")]
    
#     # Extraer las filas de datos
#     rows = []
#     for tr in table.find_all("tr")[1:]:  # Omitir la primera fila si es el encabezado
#         cells = [td.text.strip() for td in tr.find_all("td")]
#         rows.append(cells)

#     # Convertir a un DataFrame de Pandas para manipulación más fácil
#     df = pd.DataFrame(rows, columns=headers)

#     # Mostrar la tabla
#     print(df)
# else:
#     print("No se encontró la tabla con la clase " + ClassNameToExtract)
