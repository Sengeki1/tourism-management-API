# API de Gestão de Reservas de Hotel

Este é uma API simples para gestão de reservas de hotel, desenvolvida utilizando o framework FastAPI e banco de dados SQLite3.

### Requisitos Funcionais:

1. **Criar uma Nova Reserva:**
   - O endpoint `/reservas/` deve permitir a criação de uma nova reserva de hotel.
   - Os dados da reserva (nome do cliente, email, telefone, tipo de quarto, número do quarto, datas de check-in e check-out e status) devem ser enviados em formato JSON.
   - Os dados da reserva devem ser armazenados no banco de dados.

2. **Obter Todas as Reservas:**
   - O endpoint `/reservas/` deve permitir a obtenção de todas as reservas de hotel.
   - As reservas devem ser retornadas em formato JSON.

### Requisitos Não Funcionais:

1. **Banco de Dados:**
   - O sistema deve utilizar um banco de dados SQLite3 para armazenar as reservas de hotel.
   - O banco de dados deve ser criado automaticamente se não existir.

2. **Segurança:**
   - A API deve garantir a segurança dos dados dos clientes.


### Requisitos de Interface:

1. **Endpoint para Criar uma Nova Reserva:**
   - `POST /reservas/`

2. **Endpoint para Obter Todas as Reservas:**
   - `GET /reservas/`

Espero que isso ajude!

## Funcionalidades

- Criar uma nova reserva de hotel.
- Obter todas as reservas de hotel.


## Uso

1. Execute o servidor:

    ```bash
    uvicorn main:app --reload
    ```

2. Acesse a documentação da API em seu navegador:

    ```
    http://localhost:8000/docs
    ```

## Exemplos de Requisições

### Criar uma Nova Reserva

Envie um POST request para `/reservas/` com os dados da reserva em formato JSON.

Exemplo:

```json
{
  "nome_cliente": "João da Silva",
  "email_cliente": "joao@example.com",
  "telefone_cliente": "(+238) 999-9999",
  "tipo_quarto": "Standard Duplo",
  "numero_quarto": "101",
  "check_in": 1620648000,  // Timestamp para 10 de maio de 2021, 12:00:00
  "check_out": 1621104000, // Timestamp para 16 de maio de 2021, 12:00:00
  "status": "confirmada"
}
```

### Obter Todas as Reservas

Envie um GET request para `/reservas/`.

Exemplo de resposta:

```json
{
  "reservas": [
    {
      "id": 1,
      "nome_cliente": "João da Silva",
      "email_cliente": "joao@example.com",
      "telefone_cliente": "(+238) 999-9999",
      "tipo_quarto": "Standard Duplo",
      "numero_quarto": "101",
      "check_in": 1620648000,
      "check_out": 1621104000,
      "status": "confirmada"
    },
    {
      "id": 2,
      "nome_cliente": "Maria Oliveira",
      "email_cliente": "maria@example.com",
      "telefone_cliente": "(+238) 999-9999",
      "tipo_quarto": "Suíte Presidencial",
      "numero_quarto": "201",
      "check_in": 1622552400,
      "check_out": 1623330000,
      "status": "pendente"
    }
  ]
}
