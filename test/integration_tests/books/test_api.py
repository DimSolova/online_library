import pytest
from test.constants import TestUser
from test.helpers.auth import login_as_author

@pytest.mark.parametrize("user, title, description, isbn, author, status_code",[
    (TestUser.AUTHOR1.value, "Идиот", "Книга про идиота", "9785389071271", "Ф.М. Достоевский", 200),
    (TestUser.AUTHOR1.value, "Преступление и наказание", "Книга про идиота", "9785389071272", "Ф.М. Достоевский", 200),
    (TestUser.AUTHOR1.value, "Двойник", "Книга про идиота", "9785389071273", "Ф.М. Достоевский", 200),
    (TestUser.AUTHOR1.value, "Игрок", "Книга про идиота", "9785389071274", "Ф.М. Достоевский", 200),
    (TestUser.AUTHOR1.value, "Кэри", "Книга про идиота", "9785389071275", "С. Кинг", 200),
    (TestUser.AUTHOR1.value, "Идиот", "Книга про идиота", "9785389071271", "Ф.М. Достоевский", 409),
    (TestUser.AUTHOR2.value, "Идиот", "Книга про идиота", "9735389071278", "Ф.М. Достоевский", 200),
])
async def test_add_book(user, title, description, isbn, author, status_code, ac):
    resp_author = await login_as_author(ac, user)
    assert author

    response = await resp_author.post("/books",
                      json={
                          "author": author,
                          "description": description,
                          "isbn": isbn,
                          "title": title
}
                      )
    assert response.status_code == status_code

@pytest.mark.parametrize("user, book_id, title, description, isbn, author, status_code",[
    # 1. Владелец может редактировать свою книгу
    (TestUser.AUTHOR1.value, 1, "Умный", "Книга про идиота", "9785389071271", "Ф.М. Достоевский", 200),
    # 2. Другой автор НЕ может редактировать чужую книгу
    (TestUser.AUTHOR2.value, 1, "Умный", "Книга про идиота", "9785389071271", "Ф.М. Достоевский", 403),
    # 3. Нельзя установить ISBN, который уже существует у другой книги
    (TestUser.AUTHOR1.value, 2, "Умный", "Книга умного", "9785389071271", "Ф.М. Достоевский", 409),
],
     ids=[
         "author1_edits_own_book → 200 OK",
         "author2_edits_another_authors_book → 403 Forbidden",
         "author1_tries_to_set_existing_isbn → 409 Conflict",
     ],
                         )
async def test_edit_book(user, book_id, title, description, isbn, author, status_code, ac, db):
    resp_author = await login_as_author(ac, user)
    assert resp_author


    response = await resp_author.put(f"/books/{book_id}",
                                      json={
                                          "author": author,
                                          "description": description,
                                          "isbn": isbn,
                                          "title": title
                }
                                      )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "user, book_id, payload, status_code",
    [
        # 1. Автор редактирует свою книгу — только одно поле (классическое частичное обновление)
        (TestUser.AUTHOR1.value, 1, {"title": "Новое название книги"}, 200),

        # 2. Автор редактирует свою книгу — несколько полей
        (TestUser.AUTHOR1.value, 1, {
            "title": "Ещё одно новое название",
            "description": "Новое описание книги"
        }, 200),

        # 3. Другой автор НЕ может редактировать чужую книгу
        (TestUser.AUTHOR2.value, 1, {"title": "Попытка изменить чужую книгу"}, 403),

        # 4. Попытка установить уже существующий ISBN (даже при частичном обновлении)
        (TestUser.AUTHOR1.value, 2, {"isbn": "9785389071271"}, 409),
    ],
    ids=[
        "author1_partial_edit_title_only → 200",
        "author1_partial_edit_title_and_description → 200",
        "author2_cannot_edit_foreign_book → 403",
        "author1_tries_to_set_existing_isbn → 409",
    ],
)
async def test_partially_edit_book(user, book_id, payload, status_code, ac, db):
    resp_author = await login_as_author(ac, user)
    assert resp_author


    response = await resp_author.patch(f"/books/{book_id}",
                                      json=payload)

    assert response.status_code == status_code
