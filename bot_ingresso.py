from bs4 import BeautifulSoup
import random
import time
import requests

def bandeira():
    # ANSI escape codes for colors
    RED = "\033[41m"      # Red background
    WHITE = "\033[47m"    # White background
    BLACK = "\033[40m"    # Black background
    RESET = "\033[0m"     # Reset color

    bar_height = 1
    bar_width = 10

    def print_bar(color, width, height):
        for _ in range(height):
            print(color + " " * width + RESET)

    print_bar(RED, bar_width, bar_height)
    print_bar(WHITE, bar_width, bar_height)
    print_bar(BLACK, bar_width, bar_height)
    
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

    def verifica_ingresso(setor_escolhido, response):
        # Verifica se o setor escolhido está disponível no html parseado
        # Target do seletor: '.nameAndLot'
        dicionario_setores = [
            "Leste",
            "Arquibancada Vermelha - Norte",
            "Arquibancada Laranja - Organizadas",
        ]
        
        html_parseado = BeautifulSoup(response, 'html.parser')
        
        # TODO: Dar um jeito de pegar esse elemento abaixo 😡
        setores_pagina = html_parseado.find_all('label', class_='nameAndLot')
        
        for setor in dicionario_setores:
            if setor in setores_pagina:
                return True

        return False

    def disparo_alerta(link):
        print("🚨 Ingresso disponível agora:", time.strftime("%H:%M:%S"))
        print("➡️ Link:", link)
        return print("\n🎉 Bom jogo, Tricolor! Vamos São Paulo! 🇳🇱")

    def query(destino_bot, setor_escolhido):
        response = request(destino_bot)
        if response:
            html_parseado = BeautifulSoup(response, 'html.parser')
            link_pagina_compra = html_parseado.select('li a.btn.btn-primary')[0].get('href')

            status = verifica_ingresso(setor_escolhido, response)
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
            print('\n ✅ Pronto! Deixe a janela aberta deixe as máquinas trabalharem 🖐🏽 \n')
        while not encontrado:
            if tentativa >= 1:
                print(f"⚙️ Tentativa #{tentativa}:", time.strftime("%Y-%m-%d %H:%M:%S"))
            
            resultado_query = query(jogo_escolhido, setor_escolhido)
            
            if resultado_query["disponivel"]:
                encontrado = True
                disparo_alerta(resultado_query["link"])
            
            tentativa += 1
            time.sleep(random.choice(intervalo)) # respira um pouco.
    
    jogo_escolhido = lista_jogos()
    
    if jogo_escolhido:  # Verifica se um jogo foi escolhido
        setor_escolhido = escolha_setor()
        pesquisa_ingresso(jogo_escolhido, setor_escolhido)

# debug()
bot()
