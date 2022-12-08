
# Estudo | AIRFLOW - FASTAPI -ETL

Esse projeto foi feito para estudo sobre Aiflow, Fastapi e ETL.

O ETL extrai os dados de usuários fake pela API Randomuser. O número de dados a ser extraído é definido pela variável `STUDYETL_DATACOUNT`.
Depois da checagem de validação pela DAG os dados são inseridos via API, em caso de válidos ou pelo Pandas para uma outra tabela.

Depois de inseridos são gravados no diretório na pasta `extracted/DIA/HORA/data.csv` sendo coletados pela API.



## Documentação da API

#### Autenticação


``http
  POST /login
``

| Parâmetro   | Tipo       | Valor padrão                           |
| :---------- | :--------- | :---------------------------------- |
| `username` | `string` |  admin |
 `password` | `string` |  admin

#### Adiciona os dados
 
```http
  POST /add
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `user_id` | `string` |Necessita autenticação  |
 `name` | `string` | 
 `email` | `string` | 
 `gender` | `string` |
 `phone` | `string` |
 `city` | `string` | 
 `timestamp` | `string` 
 

#### Retorna os usuários cadastrados 

```http
  GET /getallusers
```

