import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from unidecode import unidecode

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)
browser.get("https://desafio.qa.bridge.ufsc.br/")

usuario = browser.find_element("xpath", '//*[@id="usuario"]')
usuario.send_keys("rafael2004.correa@gmail.com")
senha = browser.find_element("xpath", '//*[@id="password"]')
senha.send_keys("VcJWj5uzDcoAN8squARu9S")
termos = browser.find_element("xpath", '//*[@id="termos-de-uso"]')
termos.click()
acessar = browser.find_element("xpath", '/html/body/div/div[1]/button')
acessar.click()
time.sleep(1)
iniciar_desafio = browser.find_element("xpath", '/html/body/main/div/a')
iniciar_desafio.click()
time.sleep(1)

valores_base = {
    "cpf": "41545986860",
    "cns": "700004832030102",
    "nome-completo": "Rafael Corrêa Bitencourt",
    "data-nascimento": "20/02/2004",
    "sexo": "Masculino",
    "telefone-residencial": "48999999999",
    "telefone-celular": "48999999999"
}

campos = {
    "cpf": "cpf",
    "cns": "cns",
    "nome": "nome-completo",
    "data": "data-nascimento",
    "sexo": "sexo",
    "residencial": "telefone-residencial",
    "celular": "telefone-celular"
}

def find_element_by_id(id):
    return browser.find_element("xpath", f'//*[@id="{id}"]')

with open('testes.csv', newline='', encoding='utf-8') as csvfile:

    arquivo = csv.reader(csvfile)
    campo_atual = None
    next(arquivo)

    for coluna in arquivo:

        campo, mensagem_esperada, valor_entrada = coluna
        if campo in campos:

            if campo != campo_atual:
                campo_atual = campo
            
            for id, valor_base in valores_base.items():
                elemento = find_element_by_id(id)
                elemento.clear()
                elemento.send_keys(valor_base)

            elemento = find_element_by_id(campos[campo])
            elemento.clear()
            elemento.send_keys(valor_entrada)

            salvar = browser.find_element("xpath", '/html/body/div/footer/div/button[2]')
            salvar.click()
            time.sleep(1)

            mensagem = browser.find_element("xpath", '/html/body/div/footer/span')
            mensagem_ascii = unidecode(mensagem.text)

            if mensagem_ascii != unidecode(mensagem_esperada):
                print(f"-----------------")
                print(f"Teste falhou para: '{campo.upper()}'")
                print(f"Com entrada:       '{valor_entrada}'")
                print(f"Saida esperada:    '{unidecode(mensagem_esperada)}'")
                print(f"Saida obtida:      '{mensagem_ascii}'")

print(f"-----------------")
browser.quit()
