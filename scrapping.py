#import requests
#from bs4 import BeautifulSoup

#req = requests.get("https://concursosnobrasil.com/concursos/br/")

#soup = BeautifulSoup(req.content, "html.parser")


#print(soup.get_text())

# Import libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


# Fazer a requisição para a página
req = requests.get("https://concursosnobrasil.com/concursos/br/")
soup = BeautifulSoup(req.content, "html.parser")

# Encontrar os elementos que contêm as informações dos concursos
concurso_elements = soup.find("div", class_="list-concursos")

# Criar uma lista para armazenar os títulos das colunas
headers = []
for th in concurso_elements.find_all('th'):
    headers.append(th.text)

# Criar uma lista para armazenar as informações dos concursos
concurso_info = []
for row in concurso_elements.find_all('tr')[1:]:
    row_data = row.find_all('td')
    concurso_info.append([i.text for i in row_data])


# Criar o DataFrame com as informações
mydata = pd.DataFrame(concurso_info, columns=headers)

# Gerar o arquivo PDF
output_file = "tabelas_concursos.pdf"

# Criar o documento PDF usando o ReportLab
doc = SimpleDocTemplate(output_file, pagesize=letter)
elements = []

# Converter o DataFrame em uma lista de listas para a tabela do ReportLab
data = [headers] + concurso_info

# Configurações da tabela
t = Table(data)
t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                       ('GRID', (0, 0), (-1, -1), 1, colors.black)]))


# Adicionar a tabela ao documento
elements.append(t)

# Construir o documento PDF
doc.build(elements)

print(f"Arquivo PDF '{output_file}' gerado com sucesso!")