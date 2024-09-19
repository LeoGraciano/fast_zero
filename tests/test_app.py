from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_return_ok_ola_mundo():
    client = TestClient(app)  # Arrange (organização)

    response = client.get("/")  # Act (execução)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)
    assert response.json() == {"message": "Olá Mundo!!"}  # Assert (verificação)
