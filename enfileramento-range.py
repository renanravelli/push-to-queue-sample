# -*- coding: utf-8 -*-

# Arquivo enfileramento-range.py
import requests

def get_user_input():
    # Solicita ao usuário o host da API
    default_host = 'localhost:8080'
    host = raw_input("Informe o host da API (padrão é {}): ".format(default_host))
    host = host if host else default_host

    # Solicita ao usuário que escolha o laboratório
    laboratorios = ['CLAB', 'AFIP', 'FIDI']
    print("Escolha um laboratório:")
    for i, lab in enumerate(laboratorios, 1):
        print("{}. {}".format(i, lab))
    escolha = int(raw_input("Digite o número do laboratório: "))
    laboratorio = laboratorios[escolha - 1]

    # Escolhe o modo de inserção das datas
    modo = raw_input("Escolha o modo de entrada das datas ('padrão' ou 'lote'): ").lower()
    datas_inicio = []
    datas_final = []
    
    if modo == 'lote':
        print("Modo em lote selecionado. Insira as datas de início, separadas por vírgula (YYYY-MM-DD HH:MM:SS).")
        datas_inicio = raw_input("Datas de início: ").split(',')
        print("Agora, insira as datas finais, na mesma ordem, separadas por vírgula (YYYY-MM-DD HH:MM:SS).")
        datas_final = raw_input("Datas finais: ").split(',')

        # Remover espaços extras e verificar se as datas de início são menores que as finais
        datas_inicio = [data.strip() for data in datas_inicio]
        datas_final = [data.strip() for data in datas_final]
        pares_de_datas = zip(datas_inicio, datas_final)

        for inicio, final in pares_de_datas:
            if inicio > final:
                print("Erro: a data de início {} não pode ser maior que a data final {}.".format(inicio, final))
                return host, laboratorio, []

    else:
        data_inicio = raw_input("Informe a data e hora de início (formato YYYY-MM-DD HH:MM:SS): ")
        data_final = raw_input("Informe a data e hora final (formato YYYY-MM-DD HH:MM:SS): ")
        if data_inicio > data_final:
            print("Erro: a data de início não pode ser maior que a data final.")
            return host, laboratorio, []
        pares_de_datas = [(data_inicio, data_final)]

    return host, laboratorio, pares_de_datas

def call_api(host, laboratorio, data_inicio, data_final):
    url = 'http://{}/processamento/job'.format(host)
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
        print("Não foi possível conectar ao servidor no endereço {}. Verifique se o endereço está correto e se o servidor está operacional.".format(url))
    except requests.exceptions.HTTPError as err:
        print("Erro HTTP ocorrido: {} - {}".format(err.response.status_code, err.response.reason))
    except requests.exceptions.RequestException as err:
        print("Ocorreu um erro ao fazer a solicitação: {}".format(err))

def main():
    host, laboratorio, pares_de_datas = get_user_input()
    for data_inicio, data_final in pares_de_datas:
        print("Enviando dados para o período de {} a {}".format(data_inicio, data_final))
        response = call_api(host, laboratorio, data_inicio, data_final)
        if response:
            print("Chamada API realizada com sucesso!")
            print("Resposta:", response.text)

if __name__ == "__main__":
    main()
