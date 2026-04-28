import pytest

from test.helpers.auth import login_as_author

@pytest.mark.parametrize("user, user_id, role_id, status_code",[
    ("admin", 2, 3, 200),
    #Проверка на автора
    ("author1", 2, 3, 403),
    #проверка на Пользователя
    ("testuser", 2, 3, 403),
    #не существует пользователя
    ("admin", 55, 3, 401),
    # не существует роли
    ("admin", 55, 5, 401),

    ("admin", 3, 2, 200),
    ("admin", 2, 2, 200),
])
async def test_change_user_role(user, user_id, role_id, status_code, ac, db):
    resp_admin = await login_as_author(ac, user)
    response = await resp_admin.patch(f"/auth/{user_id}/role",
                           json={
                               "role_id": role_id
                           }
                           )
    assert response.status_code == status_code
    if status_code != 200:
        return
    user = await db.users.get_one(id=user_id)
    assert user.role_id == role_id

@pytest.mark.parametrize("user, user_id, is_active, status_code",[
    ("admin", 2, True, 200),
    # Проверка на автора
    ("author1", 2, False, 403),
    # проверка на Пользователя
    ("testuser", 2, False, 403),
    # не существует пользователя
    ("admin", 55, True, 401),
    #неверный ввод
    ("admin", 2, 'qwe', 422),
    #изменяем роль
    ("admin", 2, False, 200),
    #Изменяем обратно
    ("admin", 2, True, 200),
])
async def test_change_user_active(user, user_id, is_active, status_code,ac, db):
    resp_admin = await login_as_author(ac, user)
    response = await resp_admin.patch(f"/auth/{user_id}/active",
                           json={
                               "is_active": is_active
                           }
                           )
    assert response.status_code == status_code
    if status_code != 200:
        return
    user = await db.users.get_one(id=user_id)
    assert user.is_active == is_active