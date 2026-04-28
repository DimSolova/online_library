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
])
async def test_change_user_role(user, user_id, role_id, status_code,ac):
    resp_admin = await login_as_author(ac, user)
    response = await resp_admin.patch(f"/auth/{user_id}/role",
                           json={
                               "role_id": role_id
                           }
                           )
    assert response.status_code == status_code