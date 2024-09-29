from http import HTTPStatus
from uuid import UUID


def test_read_root_return_ok_ola_mundo(client):
    response = client.get("/")  # Act (execução)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    assert response.json() == {"message": "Olá Mundo!!"}  # Assert (verificação)


def test_create_user(client):
    user_data = {"email": "test@example.com", "password": "123456"}  # Act (execução)
    response = client.post("/users", json=user_data)  # Act (execução)

    assert response.status_code == HTTPStatus.CREATED  # Assert (verificação)
    user_data.pop("password", None)  # Descarta a senha do retorno
    user_data["id"] = response.json().get("id")  # Pega o ID do retorno

    assert response.json() == user_data


def test_read_users(client):
    # Gera um novo usuário para testar a leitura de todos os usuários
    user_data = {"email": "test@example.com", "password": "123456"}
    client.post("/users", json=user_data)

    response = client.get("/users")  # Act (execução)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    users = response.json().get("users")
    assert len(users) > 0


def test_update_user(client):
    # Gera um novo usuário para testar a atualização de um usuário
    user_data = {"email": "test@example.com", "password": "123456"}
    response = client.post("/users", json=user_data)
    user_id = response.json().get("id")

    updated_user_data = {"email": "updated@example.com", "password": "654321"}
    response = client.put(f"/users/{user_id}", json=updated_user_data)
    updated_user_data["id"] = user_id
    updated_user_data.pop("password", None)
    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    assert response.json() == updated_user_data


def test_update_user_not_found(client):
    user_id = UUID("00000000-0000-0000-0000-000000000000")  # ID inexistente
    updated_user_data = {"email": "updated@example.com", "password": "654321"}
    response = client.put("/users/" + str(user_id), json=updated_user_data)
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (verificação)
    assert response.json().get("detail") == "NOT FOUND"


def test_delete_user(client):
    # Gera um novo usuário para testar a exclusão de um usuário
    user_data = {"email": "test@example.com", "password": "123456"}
    response = client.post("/users", json=user_data)
    user_id = response.json().get("id")

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    assert (
        response.json().get("message") == "User deleted successfully"
    )  # Assert (verificação)


def test_delete_user_not_found(client):
    user_id = UUID("00000000-0000-0000-0000-000000000000")  # ID inexistente
    response = client.delete("/users/" + str(user_id))
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (verificação)
    assert response.json().get("detail") == "NOT FOUND"


def test_get_user(client):
    # Gera um novo usuário para testar a leitura de um usuário específico
    user_data = {"email": "test@example.com", "password": "123456"}
    response = client.post("/users", json=user_data)
    user_id = response.json().get("id")

    response = client.get(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    assert response.json().get("id") == user_id  # Assert (verificação)
    assert response.json().get("email") == user_data.get(
        "email"
    )  # Assert (verificação)
    assert (
        response.json().get("password") is None
    )  # Assert (verificação)  # Senha não é retornada


def test_get_user_not_found(client):
    user_id = UUID("00000000-0000-0000-0000-000000000000")  # ID inexistente
    response = client.get("/users/" + str(user_id))
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (verificação)
    assert response.json().get("detail") == "NOT FOUND"
