#!/bin/bash

# Define a URL padrão da API
default_host="localhost:8080"
echo -n "Informe o host da API (padrão é $default_host): "
read host_input
host=${host_input:-$default_host}

# Opções de laboratório
laboratorios=("CLAB" "AFIP" "FIDI")
echo "Escolha um laboratório:"
for i in "${!laboratorios[@]}"; do
  echo "$((i+1)). ${laboratorios[i]}"
done

echo -n "Digite o número do laboratório: "
read laboratorio_index
laboratorio=${laboratorios[$((laboratorio_index-1))]}

# Modo de entrada das datas
echo -n "Escolha o modo de entrada das datas ('padrão' ou 'lote'): "
read modo
modo=$(echo $modo | tr '[:upper:]' '[:lower:]')

if [ "$modo" == "lote" ]; then
  echo "Modo em lote selecionado. Insira as datas de início, separadas por vírgula (YYYY-MM-DD HH:MM:SS)."
  read datas_inicio
  IFS=',' read -ra datas_inicio_array <<< "$datas_inicio"

  echo "Agora, insira as datas finais, na mesma ordem, separadas por vírgula (YYYY-MM-DD HH:MM:SS)."
  read datas_final
  IFS=',' read -ra datas_final_array <<< "$datas_final"

  for i in "${!datas_inicio_array[@]}"; do
    inicio="${datas_inicio_array[i]}"
    final="${datas_final_array[i]}"

    if [[ "$inicio" > "$final" ]]; then
      echo "Erro: a data de início $inicio não pode ser maior que a data final $final."
      exit 1
    fi

    # Chamada da API para cada par de datas
    url="http://$host/processamento/job"
    data="{\"laboratorio\": \"$laboratorio\", \"dataInicio\": \"$inicio\", \"dataFinal\": \"$final\"}"
    response=$(curl -s -X POST "$url" -H "Content-Type: application/json" -d "$data")
    echo "Resposta da API: $response"
  done
else
  echo -n "Informe a data e hora de início (formato YYYY-MM-DD HH:MM:SS): "
  read data_inicio
  echo -n "Informe a data e hora final (formato YYYY-MM-DD HH:MM:SS): "
  read data_final

  if [[ "$data_inicio" > "$data_final" ]]; then
    echo "Erro: a data de início não pode ser maior que a data final."
    exit 1
  fi

  # Chamada da API para o par único de datas
  url="http://$host/processamento/job"
  data="{\"laboratorio\": \"$laboratorio\", \"dataInicio\": \"$data_inicio\", \"dataFinal\": \"$data_final\"}"
  response=$(curl -s -X POST "$url" -H "Content-Type: application/json" -d "$data")
  echo "Resposta da API: $response"
fi
