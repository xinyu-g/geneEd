from bs4 import BeautifulSoup as BS
import json
import requests

url = "https://genomics.senescence.info/genes/allgenes.php"
soup = BS(requests.get(url).content, features="html.parser")
gene_names = []
src = soup.find_all('td', align="left")
cnt = 0
for s in src:
    if not cnt % 6:
        gene_names.append(s.string)
    cnt += 1
gene_names = gene_names[0:-2]
print(gene_names)
with open('gene_names', 'w') as file:
    json.dump(gene_names, file, indent=6)
with open('gene_names', 'r') as file:
    gene = json.load(file)
print(gene)
