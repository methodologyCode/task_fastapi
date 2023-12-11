from httpx import AsyncClient
import pytest

jwt_token = None
task_id = None


def auth_header():
    global jwt_token
    return {"Authorization": f"Bearer {jwt_token}"}


@pytest.mark.anyio
async def test_async_create_user(async_client: AsyncClient):
    response = await async_client.post("/api/v1/register/", json={"username": "viz1",
                                                          "password": "viz1",
                                                          "email": "viz1@test.com"})
    assert response.status_code == 200
    assert "username" in response.json()
    assert "email" in response.json()
    assert "password" not in response.json()


@pytest.mark.anyio
async def test_login(async_client: AsyncClient):
    global jwt_token

    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    response = await async_client.post("/api/v1/login/", data={"username": "viz1", "password": "viz1"},
                                       headers=headers)
    jwt_token = response.json().get("access_token")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"


@pytest.mark.anyio
async def test_read_user(async_client: AsyncClient):
    response = await async_client.get("/api/v1/about_me/", headers=auth_header())
    assert response.status_code == 200
    assert response.json()["username"] == "viz1"
    assert response.json()["email"] == "viz1@test.com"


@pytest.mark.anyio
async def test_create_task(async_client: AsyncClient):
    global task_id
    response = await async_client.post("/api/v1/tasks/", headers=auth_header(),
                                       json={"title": "Test Title",
                                             "description": "12345"})
    assert response.status_code == 200
    assert "id" in response.json()
    task_id = response.json()["id"]
    assert response.json()["title"] == "Test Title"
    assert response.json()["description"] == "12345"
    assert response.json()["completed"] is False


@pytest.mark.anyio
async def test_read_task(async_client: AsyncClient):
    response = await async_client.get(f"/api/v1/tasks/{task_id}", headers=auth_header())
    assert response.json()["title"] == "Test Title"
    assert response.json()["description"] == "12345"
    assert response.json()["completed"] is False


@pytest.mark.anyio
async def test_update_task(async_client: AsyncClient):
    response = await async_client.put(f"/api/v1/tasks/{task_id}", headers=auth_header(),
                                      json={"title": "test",
                                            "description": "123",
                                            "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "test"
    assert response.json()["description"] == "123"
    assert response.json()["completed"] is True


@pytest.mark.anyio
async def test_delete_task(async_client: AsyncClient):
    response = await async_client.delete(f"/api/v1/tasks/{task_id}", headers=auth_header())
    assert response.json()["title"] == "test"
    assert response.json()["description"] == "123"
    assert response.json()["completed"] is True
