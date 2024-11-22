from bs4 import BeautifulSoup
import random
import time
import requests
from selenium import webdriver
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

    opcoes_setores = [
        "  [0] - Arquibancada Norte Oreo - Meia",
        "  [1] - Arquibancada Norte Oreo - Inteira",
        "  [2] - Arquibancada Leste Lacta - Meia",
        "  [3] - Arquibancada Leste Lacta - Inteira",
        "  [4] - Arquibancada Sul Diamante Negro - Meia",
        "  [5] - Arquibancada Sul Diamante Negro - Inteira",
        "  [6] - Arquibancada Visitante Ouro Branco - Meia",
        "  [7] - Arquibancada Visitante Ouro Branco - Inteira",
        "  [8] - Cadeira Superior Norte Oreo - Inteira",
        "  [9] - Cadeira Superior Sul Diamante Negro - Meia",
        "  [10] - Cadeira Superior Sul Diamante Negro - Inteira",
        "  [11] - Cadeira Especial Oeste Ouro Branco - Especial Meia",
        "  [12] - Cadeira Especial Oeste Ouro Branco - Especial Inteira",
        "  [13] - Cadeira Térrea Oeste Ouro Branco - Meia",
        "  [14] - Cadeira Térrea Oeste Ouro Branco - Inteira",
        "  [15] - Camarote Corporativo SPFC - Único",
        "  [16] - Camarote dos Ídolos - Único"
    ]

    dicionario_setores = [
        "ARQUIBANCADA NORTE OREO - Meia",
        "ARQUIBANCADA NORTE OREO - Inteira",
        "ARQUIBANCADA LESTE LACTA - Meia",
        "ARQUIBANCADA LESTE LACTA - Inteira",
        "ARQUIBANCADA SUL DIAMANTE NEGRO - Meia",
        "ARQUIBANCADA SUL DIAMANTE NEGRO - Inteira",
        "ARQUIBANCADA VISITANTE OURO BRANCO - Meia",
        "ARQUIBANCADA VISITANTE OURO BRANCO - Inteira",
        "CADEIRA SUPERIOR NORTE OREO - Inteira",
        "CAD. SUP. SUL DIAMANTE NEGRO - Meia",
        "CAD. SUP. SUL DIAMANTE NEGRO - Inteira",
        "CAD. ESP. OESTE OURO BRANCO - Especial Meia",
        "CAD. ESP. OESTE OURO BRANCO - Especial Inteira",
        "CAD. TÉRREA OESTE OURO BRANCO - Meia",
        "CAD. TÉRREA OESTE OURO BRANCO - Inteira",
        "CAMAROTE CORPORATIVO SPFC - Único",
        "CAMAROTE DOS ÍDOLOS - Único"
   ] 

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
            
            for index, jogo in enumerate(todos_jogos):
                botao_comprar = jogo.select_one('a.btn.btn-primary') 

                if botao_comprar and 'Comprar agora' in botao_comprar.text:
                    nome = jogo.select_one('.jogo-title').text.strip()
                    link = botao_comprar.get('href')
                    bandeira()
                    print("\nBilheteria aberta \n")
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

            
        else:
            return None        
        

    def escolha_setor():
        print("\n  🏟  Setores do MorumBIS: \n")

        for setor in opcoes_setores:
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
        
        setores_disponiveis = html_parseado.find_all('div', class_='cart-product-group-item')

        for setor in setores_disponiveis:
            if dicionario_setores[setor_escolhido] in setor.text and 'Esgotado' not in setor.text:
                return True

        return False

    def disparo_alerta(link):
        print("🚨 Ingresso disponível agora:", time.strftime("%H:%M:%S"))
        print("➡️ Link:", link)
        return print("\n🎉 Bom jogo, Tricolor! Vamos São Paulo! 🇳🇱")

    def query(destino_bot, setor_escolhido):
        def parseador_link(link):
            response = request(link)
            html_parseado_jogos = BeautifulSoup(response, 'html.parser')
            link_pagina_compra = html_parseado_jogos.select('li a.btn.btn-primary')[0].get('href')
            return link_pagina_compra
        
        link_parseado = parseador_link(destino_bot)

        if link_parseado:
            if 'cart' not in link_parseado:
               link_parseado = parseador_link(link_parseado)
            status = verifica_ingresso(setor_escolhido, link_parseado)
            return {
                "disponivel": status,
                "link": link_parseado 
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
        return pesquisa_ingresso(jogo_escolhido, setor_escolhido)

bot()

