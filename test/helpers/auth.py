# ====================== ХЕЛПЕР ДЛЯ ЛОГИНА ======================
import json

from httpx import AsyncClient


async def login_as_author(ac: AsyncClient, username: str):
    """Логинит указанного автора и возвращает тот же клиент"""
    with open("test/mock_users_data.json", encoding="utf-8") as f:
        users_data = json.load(f)

    author = next((u for u in users_data if u["username"] == username), None)
    if not author:
        raise ValueError(f"Пользователь {username} не найден в mock_users_data.json")

    response = await ac.post(
        "/auth/login", json={"email": author["email"], "password": author["password"]}
    )
    assert response.status_code == 200, f"Не удалось залогиниться как {username}"
    assert "access_token" in ac.cookies, f"Куки access_token не появился для {username}"

    return ac
