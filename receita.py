import pyttsx3
import requests
from bs4 import BeautifulSoup
from time import sleep

maquina = pyttsx3.init()

def dizer(palavra):
    maquina = pyttsx3.init()
    print(palavra)
    maquina.say(f"{palavra}")
    maquina.runAndWait()

lista_ingredientes = [] # criar uma lista vazia

site_base = r"https://www.tudogostoso.com.br/busca?q=" # site base para pegar receitas
nome_receita = str(input("Qual receita quer procurar?\nResponda aqui: ")) # receber nome da receita
site = requests.get(site_base + nome_receita.replace(' ', '+')) # ir até um site de receitas pesquisando pela receita escolhida

soup = BeautifulSoup(site.content, "html.parser") # pegar informações da página
receita = soup.find("a", {"class": "link row m-0"}) # encontrar posição HTML da receita
link = "https://www.tudogostoso.com.br" + receita["href"] # site da receita escolhida

site = requests.get(link) # ir até o site da receita escolhida
soup = BeautifulSoup(site.content, "html.parser") # pegar informações da página


def pegar_ingredientes(): # criar função
    ingredientes = soup.find_all("span", {"class": "p-ingredient"}) # posição HTML dos ingredientes

    for ingrediente in ingredientes: # para cada ingrediente em ingredientes
        lista_ingredientes.append(ingrediente.get_text()) # adicionar o ingrediente a uma lista

    for valor in lista_ingredientes: # para valorda lista com ingredientes
        valor.replace("(", "de") # substituir os parentes abertos "(" por um "de"


    # maquina dizendo que começará a listagem de ingredientes
    dizer(f"Para fazer essa receita você precisará de:")

    for valor in lista_ingredientes: # para cada valor na lista de ingredientes
        valor.replace(r"\xa0", "")  # remover todos os "\xa0"
        print(f"{valor}",end=', ') # mostrar na tela cada ingrediente

        # maquina dizendo os ingredientes necessários
        maquina.say(valor.replace("(", "de"))
        maquina.runAndWait()

    print("Fim.") # mostrar mensagem que a listagem de ingredientes chegou ao fim

def pegar_modo_de_preparo(): # criar função
    informações = soup.find("div", {"class": "instructions e-instructions"}) # posição HTML do modo de preparo


    # maquina avisar que começará a listagem do modo de preparo
    dizer("Modo de preparo:")

    for informação in informações: # para cada informação em informações
        sleep(1) # esperar um segundo

        # print(informação)
        try:
            dizer(informação.get_text().replace(".", ". "))
        except:
            continue

# chamar funções
pegar_ingredientes()
pegar_modo_de_preparo()