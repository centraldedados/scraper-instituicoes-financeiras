scraper-instituicoes-financeiras
================================

Scraper para o dataset das instituições financeiras registadas em Portugal.
Cria uma dataset como o que pode ser visto em https://github.com/centraldedados/instituicoes-financeiras .

# Uso

```
python bank-list.py
```
Criará o ficheiro banks.json

```
python fetchy.py
```
Usa o ficheiro banks.json para ir buscar informação de cada um dos bancos

```
python bank-details.py
```
Cria o banks-info.json

```
python banksJSON-CSV.py
```
Cria o CSV final a partir dos ficheiros banks.json e banks-info.json .
