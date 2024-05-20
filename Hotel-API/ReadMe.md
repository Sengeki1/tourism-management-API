# API de Gestão de Reservas de Hotel

Este é uma API para gestão de reservas de hotel, desenvolvida utilizando o framework FastAPI e banco de dados SQLite e SQLAlchemy.

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

### To Do

- [x] Cancelar reserva pelo ID;
- [x] Criar Base de Dados;
- [x] CRUD Completo;
- [x] Definir uma quantidade limitada de quartos e categorias;
- [ ] Criar Diagramas Explicando o Codigo;
