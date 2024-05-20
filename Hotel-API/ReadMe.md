# API de Gestão de Reservas de Hotel

Este é uma API para gestão de reservas de hotel, desenvolvida utilizando o framework FastAPI e banco de dados SQLite3.

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


## Funcionalidades

- Criar uma nova reserva de hotel.
- Obter todas as reservas de hotel.
- Obter quartos disponiveis.
- Obter uma reserva pelo numero de BI.
- Cancelar reserva pelo numero de BI.
- Atualizar reserva pelo numero de BI.


## Uso

1. Execute o servidor(dentro do diretorio FastAPI):

    ```bash
    uvicorn run:app --reload
    ```

2. Acesse a documentação da API em seu navegador:

    ```
    http://localhost:8000/docs
    ```

## Exemplos de Requisições

### Criar uma nova reserva

- **URL**: `/criar_reserva/`
- **Método**: `POST`
- **Payload**:
    ```json
    {
        "numero_BI": "123456789",
        "nome_cliente": "John Doe",
        "email_cliente": "john.doe@example.com",
        "telefone_cliente": "1234567890",
        "tipo_quarto": "A",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-05T12:00:00",
        "status": "confirmada"
    }
    ```
- **Resposta**:
    ```json
    {
        "numero_BI": "123456789",
        "nome_cliente": "John Doe",
        "email_cliente": "john.doe@example.com",
        "telefone_cliente": "1234567890",
        "tipo_quarto": "A",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-05T12:00:00",
        "status": "confirmada"
    }
    ```

### Obter todas as reservas

- **URL**: `/reservas/`
- **Método**: `GET`
- **Resposta**:
    ```json
    [
        {
            "numero_BI": "123456789",
            "nome_cliente": "John Doe",
            "email_cliente": "john.doe@example.com",
            "telefone_cliente": "1234567890",
            "tipo_quarto": "A",
            "check_in": "2024-06-01T14:00:00",
            "check_out": "2024-06-05T12:00:00",
            "status": "confirmada"
        }
    ]
    ```

### Cancelar uma reserva

- **URL**: `/cancelar_reserva/{numero_BI}/`
- **Método**: `DELETE`
- **Resposta**:
    ```json
    {
        "message": "Reserva cancelada com sucesso."
    }
    ```

### Obter disponibilidade dos quartos

- **URL**: `/quartos-disponiveis/`
- **Método**: `GET`
- **Resposta**:
    ```json
    {
        "Quartos disponíveis": {
            "Classe A": 5,
            "Classe B": 15,
            "Classe C": 30
        }
    }
    ```

### Buscar uma reserva pelo número de BI

- **URL**: `/buscar_reserva/{numero_BI}/`
- **Método**: `GET`
- **Resposta**:
    ```json
    {
        "numero_BI": "123456789",
        "nome_cliente": "John Doe",
        "email_cliente": "john.doe@example.com",
        "telefone_cliente": "1234567890",
        "tipo_quarto": "A",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-05T12:00:00",
        "status": "confirmada"
    }
    ```

### Atualizar uma reserva

- **URL**: `/atualizar_reserva/{numero_BI}/`
- **Método**: `PUT`
- **Payload**:
    ```json
    {
        "numero_BI": "123456789",
        "nome_cliente": "John Doe",
        "email_cliente": "john.doe@example.com",
        "telefone_cliente": "1234567890",
        "tipo_quarto": "A",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-05T12:00:00",
        "status": "confirmada"
    }
    ```
- **Resposta**:
    ```json
    {
        "numero_BI": "123456789",
        "nome_cliente": "John Doe",
        "email_cliente": "john.doe@example.com",
        "telefone_cliente": "1234567890",
        "tipo_quarto": "A",
        "check_in": "2024-06-01T14:00:00",
        "check_out": "2024-06-05T12:00:00",
        "status": "confirmada"
    }

```
### To Do

- [x] Cancelar reserva pelo ID;
- [x] Criar Base de Dados;
- [x] Definir uma quantidade limitada de quartos e categorias;
