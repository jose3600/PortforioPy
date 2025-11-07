import random
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from folium import Map, Marker

# ================== MENU ==================
def menu():
    print("""
========= MENU PRINCIPAL =========
A - Decisão e Repetição
B - Vetores e Matrizes
C - Funções e Bibliotecas
D - Registros
E - Arquivos em Disco
F - Recursividade
G - Complexidade de Tempo (Big O)
H - Uso de APIs externas (Clima)
I - Consultar Endereço pelo CEP
J - Consultar Cotação do Dólar
K - Monitoramento da Frota de Ônibus (SPTrans)
S - Sair
==================================
""")

# ================== A ==================
def decisao_repeticao():
    while True:
        print("\n--- Decisão e Repetição ---")
        n = int(input("Digite um número (0 para sair): "))
        if n == 0:
            break
        print("É par!" if n % 2 == 0 else "É ímpar!")
        if input("Deseja continuar nesta opção? (s/n): ").lower() != 's':
            break

# ================== B ==================
def vetores_matrizes():
    while True:
        print("\n--- Vetores e Matrizes ---")
        vetor = [random.randint(1, 100) for _ in range(5)]
        print("Vetor:", vetor)
        matriz = [[random.randint(1, 10) for _ in range(3)] for _ in range(3)]
        print("Matriz:")
        for linha in matriz:
            print(linha)
        if input("Deseja gerar novos vetores/matrizes? (s/n): ").lower() != 's':
            break

# ================== C ==================
def funcoes_bibliotecas():
    while True:
        print("\n--- Funções e Bibliotecas ---")
        def soma(a, b):
            return a + b
        x = int(input("Primeiro número: "))
        y = int(input("Segundo número: "))
        print(f"Soma = {soma(x, y)}")
        if input("Deseja continuar nesta opção? (s/n): ").lower() != 's':
            break

# ================== D ==================
def registros():
    while True:
        print("\n--- Registros (Dicionários) ---")
        pessoa = {
            "nome": input("Nome: "),
            "idade": int(input("Idade: ")),
            "cidade": input("Cidade: ")
        }
        print(f"Registro criado: {pessoa}")
        if input("Deseja criar outro registro? (s/n): ").lower() != 's':
            break

# ================== E ==================
def arquivos_disco():
    while True:
        print("\n--- Arquivos em Disco ---")
        with open("dados.txt", "a", encoding="utf-8") as f:
            texto = input("Digite algo para salvar no arquivo: ")
            f.write(texto + "\n")
        print("Texto salvo em 'dados.txt'!")

        if input("Deseja ver o conteúdo do arquivo? (s/n): ").lower() == 's':
            with open("dados.txt", "r", encoding="utf-8") as f:
                print("\nConteúdo do arquivo:")
                print(f.read())
        if input("Deseja continuar nesta opção? (s/n): ").lower() != 's':
            break

# ================== F ==================
def recursividade():
    print("\n--- Recursividade ---")
    def fatorial(n):
        if n == 0:
            return 1
        return n * fatorial(n - 1)

    while True:
        n = int(input("Número para calcular fatorial: "))
        print(f"Fatorial de {n} = {fatorial(n)}")
        if input("Deseja continuar nesta opção? (s/n): ").lower() != 's':
            break

# ================== G ==================
def complexidade_big_o():
    print("\n--- Complexidade de Tempo (Big O) ---")
    print("Exemplo: busca linear O(n)")
    lista = list(range(1, 1000000))
    alvo = int(input("Número para buscar (1 a 1.000.000): "))

    for i in lista:
        if i == alvo:
            print("Número encontrado!")
            break
    print("Busca concluída!")

# ================== H ==================
def uso_api_externa():
    print("\n--- API Externa: Clima ---")
    while True:
        cidade = input("Digite o nome da cidade: ")
        try:
            resposta = requests.get(f"https://wttr.in/{cidade}?format=3")
            print("Clima atual:", resposta.text)
        except:
            print("Erro ao consultar API.")
        if input("Deseja consultar outra cidade? (s/n): ").lower() != 's':
            break

# ================== I ==================
def consulta_cep():
    print("\n--- Consultando Endereço pelo CEP ---")
    while True:
        cep = input("Digite o CEP (somente números): ")
        try:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            res = requests.get(url).json()
            if "erro" in res:
                print("CEP não encontrado.")
            else:
                print(f"Logradouro: {res['logradouro']}, Bairro: {res['bairro']}, Cidade: {res['localidade']}-{res['uf']}")
        except Exception as e:
            print("Erro ao consultar CEP:", e)
        if input("Deseja consultar outro CEP? (s/n): ").lower() != 's':
            break

# ================== J ==================
def cotar_dolar():
    print("\n--- Consultando Cotação do Dólar ---")

    def cotar(data):
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$format=json"
        res = requests.get(url).json()
        if res["value"]:
            return res["value"][0]["cotacaoVenda"]
        else:
            dia_anterior = datetime.strptime(data, "%m%d%Y") - timedelta(1)
            dia_anterior = datetime.strftime(dia_anterior, "%m%d%Y")
            return cotar(dia_anterior)

    while True:
        data = input("Digite a data (MMDDYYYY): ")
        try:
            cotacao = cotar(data)
            print(f"Cotação do Dólar em {data}: R$ {cotacao}")
        except Exception as e:
            print("Erro ao consultar cotação:", e)
        if input("Deseja consultar outra data? (s/n): ").lower() != 's':
            break

# ================== K ==================
def monitoramento_frota():
    print("\n--- Monitoramento da Frota de Ônibus (SPTrans) ---")

    load_dotenv(".env")
    token = os.getenv("SPTRANS_TOKEN")

    if not token:
        print("❌ Token SPTRANS não encontrado! Crie um arquivo .env com a variável SPTRANS_TOKEN.")
        return

    try:
        s = requests.Session()
        res = s.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}")
        if res.text.lower() != "true":
            print("❌ Falha na autenticação com a API SPTrans.")
            return

        termo = input("Digite um termo para buscar uma linha (ex: Lapa): ")
        linhas = s.get(f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={termo}").json()

        if not linhas:
            print("Nenhuma linha encontrada.")
            return

        print("\nLinhas encontradas:")
        for l in linhas[:5]:
            print(f"Código: {l['cl']} | Letreiro: {l['lt']} | Origem: {l['tp']} -> Destino: {l['ts']}")

        codigo = int(input("\nDigite o código de uma linha para ver as paradas: "))
        paradas = s.get(f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo}").json()

        if not paradas:
            print("Nenhuma parada encontrada para essa linha.")
            return

        # Cria mapa
        m = Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=13)
        for p in paradas:
            Marker(location=[p["py"], p["px"]], popup=p["np"]).add_to(m)
        m.save("paradas_onibus.html")

        print("🗺️ Mapa salvo como 'paradas_onibus.html'! Abra-o no navegador para visualizar.")
    except Exception as e:
        print("Erro ao consultar API SPTrans:", e)

# ================== LOOP PRINCIPAL ==================
while True:
    menu()
    opcao = input("Escolha uma opção: ").upper()

    if opcao == 'A': decisao_repeticao()
    elif opcao == 'B': vetores_matrizes()
    elif opcao == 'C': funcoes_bibliotecas()
    elif opcao == 'D': registros()
    elif opcao == 'E': arquivos_disco()
    elif opcao == 'F': recursividade()
    elif opcao == 'G': complexidade_big_o()
    elif opcao == 'H': uso_api_externa()
    elif opcao == 'I': consulta_cep()
    elif opcao == 'J': cotar_dolar()
    elif opcao == 'K': monitoramento_frota()
    elif opcao == 'S':
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida. Tente novamente.")
