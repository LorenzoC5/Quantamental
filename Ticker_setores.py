import yfinance as yf
import csv

# Caminho para o arquivo de tickers(VER NO SEU PC QUAL É!!)
caminho_arquivo_tickers = r'C:\Users\loren\Downloads\top_50_msgarch_tickers.txt'

# Ler os tickers do arquivo e extrair apenas o símbolo antes da vírgula(Utilizei o MSGARCH)
with open(caminho_arquivo_tickers, 'r') as arquivo:
    tickers = [linha.strip().split(',')[0] for linha in arquivo if linha.strip()]

# Lista para armazenar os dados
dados = []

# Obter informações de setor para cada ticker
for ticker in tickers:
    try:
        acao = yf.Ticker(ticker)
        info = acao.info
        setor = info.get('sector', 'N/A')
        dados.append({'Ticker': ticker, 'Setor': setor})
    except Exception as e:
        print(f"Erro ao obter dados para {ticker}: {e}")
        dados.append({'Ticker': ticker, 'Setor': 'Erro'})

# Escrever os dados em um arquivo CSV
with open('tickers_setores.csv', 'w', newline='', encoding='utf-8') as csvfile:
    campos = ['Ticker', 'Setor']
    escritor = csv.DictWriter(csvfile, fieldnames=campos)

    escritor.writeheader()
    for linha in dados:
        escritor.writerow(linha)
