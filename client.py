from datetime import datetime

import tweepy as tw
import requests
import time
import dados as d            # Local onde está armazenado meus tokens cujos quais não irei divulgar publicamente.

# Código criado por LOKOZ

# Autenticando o Bot.
client = tw.Client(
    consumer_key=d.consumer_key,
    consumer_secret=d.consumer_secret,
    access_token=d.access_token,
    access_token_secret=d.access_token_secret
)

# Fazendo uma requisição inicial.
try:
    req_inicial = requests.get('http://economia.awesomeapi.com.br/json/last/USD-BRL')
    req_inicial_dic = req_inicial.json()
    cot_dolar_inicio = req_inicial_dic['USDBRL']['bid']
    print(' ESTAMOS ONLINE ')

except Exception as e:
    print('[ERROR] Ocorreu algum erro na requisição da API.')
    print(e)

# Loop para o programa rodar infinitamente.
while True:
    i = 0
    while i < 1:
        print('\n')
        time.sleep(60)
        i = i + 1

    try:
        requisicao = requests.get('http://economia.awesomeapi.com.br/json/last/USD-BRL')
        requisicao_dic = requisicao.json()
        cot_dolar = requisicao_dic['USDBRL']['bid']

    except TimeoutError:
        print(datetime.now().strftime('%d/%m/%Y %H:%M:%S - Timeout Error'))
    except Exception as e:
        print(datetime.now().strftime('%d/%m/%Y %H:%M:%S - ERROR'))
        print(e)

    # Formatando os números.
    try:
        cot_dolar_inicio = float(cot_dolar_inicio)
        cot_dolar = float(cot_dolar)

    except NameError as E:
        datetime.now().strftime('%d/%m/%Y %H:%M:%S - Name Error')

    except Exception as E:
        print(datetime.now().strftime('%d/%m/%Y %H:%M:%S - Error'))
        print(E)

    # Pegar data e hora atuais.
    data_e_hora_atuais = datetime.now()

    cot_dolar_inicio = "{:.2f}".format(cot_dolar_inicio)
    cot_dolar = '{:.2f}'.format(cot_dolar)

    print(data_e_hora_atuais.strftime('\n\n%d/%m/%Y %H:%M COTAÇÃO:'))
    print(f'\nCOTAÇÃO ANTERIOR: {cot_dolar_inicio}')
    print(f'COTAÇÃO ATUAL: {cot_dolar}\n\n')

    # Calculando variação.
    variacao_descida = float(cot_dolar_inicio) - float(cot_dolar)
    variacao_subida = float(cot_dolar) - float(cot_dolar_inicio)

    if cot_dolar_inicio > cot_dolar:
        print('OCORREU UMA ALTERAÇÃO... POSTANDO')
        response = client.create_tweet(
            text=f'''

• [{data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')}]


📉 Dolár desceu

💵 Foi para: R${cot_dolar} 
🤓 Variação de: R$-{round(variacao_descida, 2)}
                  '''
        )
        print(f"https://twitter.com/user/status/{response.data['id']}")
        cot_dolar_inicio = cot_dolar

    elif cot_dolar_inicio < cot_dolar:
        print('OCORREU UMA ALTERAÇÃO... POSTANDO')
        response = client.create_tweet(
            text=f'''

• [{data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')}]


📈 Dolár subiu

💵 Foi para: R${cot_dolar} 
🤓 Variação de: R$+{round(variacao_subida, 2)}

                  '''
        )
        print(f"https://twitter.com/user/status/{response.data['id']}")
        cot_dolar_inicio = cot_dolar

    else:
        pass
