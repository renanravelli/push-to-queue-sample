# -*- coding: utf-8 -*-
# Arquivo enfileramento-range.py
import requests

def get_user_input():
    # Solicita ao usuário o host da API
    default_host = 'localhost:8080'
    host = input(f"Informe o host da API (padrão é {default_host}): ")
    host = host if host else default_host

    # Solicita ao usuário que escolha o laboratório
    laboratorios = ['CLAB', 'AFIP', 'FIDI']
    print("Escolha um laboratório:")
    for i, lab in enumerate(laboratorios, 1):
        print(f"{i}. {lab}")
    escolha = int(input("Digite o número do laboratório: "))
    laboratorio = laboratorios[escolha - 1]

    # Escolhe o modo de inserção das datas
    modo = input("Escolha o modo de entrada das datas ('padrão' ou 'lote'): ").lower()
    datas_inicio = []
    datas_final = []
    
    if modo == 'lote':
        print("Modo em lote selecionado. Insira as datas de início, separadas por vírgula (YYYY-MM-DD HH:MM:SS).")
        datas_inicio = input("Datas de início: ").split(',')
        print("Agora, insira as datas finais, na mesma ordem, separadas por vírgula (YYYY-MM-DD HH:MM:SS).")
        datas_final = input("Datas finais: ").split(',')

        # Remover espaços extras e verificar se as datas de início são menores que as finais
        datas_inicio = [data.strip() for data in datas_inicio]
        datas_final = [data.strip() for data in datas_final]
        pares_de_datas = list(zip(datas_inicio, datas_final))

        for inicio, final in pares_de_datas:
            if inicio > final:
                print(f"Erro: a data de início {inicio} não pode ser maior que a data final {final}.")
                return host, laboratorio, []

    else:
        data_inicio = input("Informe a data e hora de início (formato YYYY-MM-DD HH:MM:SS): ")
        data_final = input("Informe a data e hora final (formato YYYY-MM-DD HH:MM:SS): ")
        if data_inicio > data_final:
            print("Erro: a data de início não pode ser maior que a data final.")
            return host, laboratorio, []
        pares_de_datas = [(data_inicio, data_final)]

    return host, laboratorio, pares_de_datas

def call_api(host, laboratorio, data_inicio, data_final):
    url = f'http://{host}/processamento/job'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'laboratorio': laboratorio,
        'dataInicio': data_inicio,
        'dataFinal': data_final
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError:
        print(f"Não foi possível conectar ao servidor no endereço {url}. Verifique se o endereço está correto e se o servidor está operacional.")
    except requests.exceptions.HTTPError as err:
        print(f"Erro HTTP ocorrido: {err.response.status_code} - {err.response.reason}")
    except requests.exceptions.RequestException as err:
        print(f"Ocorreu um erro ao fazer a solicitação: {err}")

def main():
    host, laboratorio, pares_de_datas = get_user_input()
    for data_inicio, data_final in pares_de_datas:
        print(f"Enviando dados para o período de {data_inicio} a {data_final}")
        response = call_api(host, laboratorio, data_inicio, data_final)
        if response:
            print("Chamada API realizada com sucesso!")
            print("Resposta:", response.text)

if __name__ == "__main__":
    main()
