import pytest


@pytest.mark.parametrize("username, email, password, status_code", [
    ("Solova", "Solova@gmail.com", "qwe", 201),
    ("Solova", "Solova@gmail.com", "qwe", 409),
    ("Kot", "Solovagmail.com", "qwe", 422),
    ("Kot", "Solova@gmailcom", "qwe", 422),
])
async def test_auth_flow(username: str, email: str, password: str, status_code: int, ac):
    resp_register = await ac.post(
        "/auth/register",
        json={
            "username":username,
            "email": email,
            "password": password
        }
    )

    assert resp_register.status_code == status_code
    if status_code != 201:
        return

    resp_login = await ac.post(
        "/auth/login",
        json={
          "email": email,
          "password": password
}
    )
    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()["data"]

    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()["data"]
    assert "id" in user
    assert "email" in user
    assert "role" in user