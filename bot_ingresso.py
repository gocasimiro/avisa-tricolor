from bs4 import BeautifulSoup
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bandeira():
    VERMELHO = "\033[41m"      
    BRANCO = "\033[47m"
    PRETO = "\033[40m"
    RESET = "\033[0m"

    barra_altura = 1
    barra_largura = 10

    def barra(color, width, height):
        for _ in range(height):
            print(color + " " * width + RESET)

    barra(VERMELHO, barra_largura, barra_altura)
    barra(BRANCO, barra_largura, barra_altura)
    barra(PRETO, barra_largura, barra_altura)
    
    return


def bot():
    intervalo = [30, 45, 18, 20]
    encontrado = False

    def request(destino_bot):    
        response = requests.get(destino_bot)
        if response.status_code == 200:
            return response.text
        else:
            print("Erro:", response.status_code)
        return None

    def lista_jogos():
        destino_bot = "https://www.spfcticket.net/"
        response = requests.get(destino_bot)
        html_parseado = BeautifulSoup(response.text, 'html.parser')
        todos_jogos = html_parseado.select('.card-jogo')

        jogos_disponiveis = []

        if todos_jogos:
            bandeira()
            print("\nBilheteria aberta \n")
            for index, jogo in enumerate(todos_jogos):
                botao_comprar = jogo.select_one('a.btn.btn-primary') 

                if botao_comprar and 'Comprar agora' in botao_comprar.text:
                    nome = jogo.select_one('.jogo-title').text.strip()
                    link = botao_comprar.get('href')
                    print(f"  [{index}] - {nome}")
                    jogos_disponiveis.append(link)            

            if jogos_disponiveis:
                escolha = int(input("\n * Digite a opção e escolha o jogo 👉 "))
                return jogos_disponiveis[escolha]
        
        else:
            bandeira()
            print("\n❌ Nenhum jogo disponível, volte mais tarde e tente novamente.")
            print("\n⚽️ Enquanto isso, assista o antológico Gol 100 do Rogério Ceni: \n➡️ https://www.youtube.com/watch?v=q0bzabZyWNk")
            return None

    def escolha_setor():
        setores_disponiveis = [
            "  [0] - Arquibancada Azul - Leste",
            "  [1] - Arquibancada Vermelha - Norte",
            "  [2] - Arquibancada Laranja - Organizadas",
        ]
        
        print("\n  🏟  Setores disponíveis: \n")

        for setor in setores_disponiveis:
            print(setor)

        setor_escolhido = int(input("\n * Agora escolha o setor 👉 "))
        return setor_escolhido 

    def verifica_ingresso(setor_escolhido, link):

        def renderiza_pagina(link):
            params = webdriver.ChromeOptions()
            params.add_argument('--headless') 
            navegador = webdriver.Chrome(options=params)
            navegador.get(link)            
            
            try:
                WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nameAndLot")))
            except:
                print("\n ⚙️ Nenhum ingresso disponível, tentando novamente... \n")

            pagina_renderizada = BeautifulSoup(navegador.page_source, "html.parser")
            navegador.quit()
            return pagina_renderizada
        
        html_parseado = renderiza_pagina(link)
        
        dicionario_setores = [
            "Leste",
            "Arquibancada Vermelha - Norte",
            "Arquibancada Laranja - Organizadas",
            "CAMAROTE"
        ]
        
        setores_pagina = html_parseado.find_all('label', class_='nameAndLot')
        
        # Finalizar verificação de ingresso disponível
            # Listar os setores do Morumbis no dicionário
            # Transformar o dicionário dos setores em uma lista enumerada que corresponda às opções iniciais apresentadas ao usuário
            # Escolher o setor baseado no setor_escolhido
            # Verificar se o setor escolhido está disponível na página


        for setor in dicionario_setores:
            for setor_disponivel in setores_pagina:
                if setor in setor_disponivel.text:
                    return True

        return False

    def disparo_alerta(link):
        print("🚨 Ingresso disponível agora:", time.strftime("%H:%M:%S"))
        print("➡️ Link:", link)
        return print("\n🎉 Bom jogo, Tricolor! Vamos São Paulo! 🇳🇱")

    def query(destino_bot, setor_escolhido):
        response = request(destino_bot)
        if response:
            html_parseado_jogos = BeautifulSoup(response, 'html.parser')
            link_pagina_compra = html_parseado_jogos.select('li a.btn.btn-primary')[0].get('href')
            status = verifica_ingresso(setor_escolhido, link_pagina_compra)
            return {
                "disponivel": status,
                "link": link_pagina_compra
            }
        
        else:
            return {"disponivel": False}

    def pesquisa_ingresso(jogo_escolhido, setor_escolhido):
        tentativa = 0
        nonlocal encontrado
        if tentativa == 0: 
            print('\n ✅ Pronto! Deixe a janela aberta, aguarde e deixe as máquinas trabalharem 🖐🏽 \n')
        while not encontrado:
            if tentativa >= 1:
                print(f"⚙️ Tentativa #{tentativa}:", time.strftime("%H:%M:%S"))
            
            resultado_query = query(jogo_escolhido, setor_escolhido)
            
            if resultado_query["disponivel"]:
                encontrado = True
                return disparo_alerta(resultado_query["link"])
            
            tentativa += 1
            time.sleep(random.choice(intervalo)) # respira um pouco.
    
    jogo_escolhido = lista_jogos()
    
    if jogo_escolhido:
        setor_escolhido = escolha_setor()
        pesquisa_ingresso(jogo_escolhido, setor_escolhido)

bot()