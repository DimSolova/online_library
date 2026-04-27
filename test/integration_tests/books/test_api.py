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
    (TestUser.AUTHOR1.value, 2, "Умный", "Книга умного", "9785389071271", "Ф.М. Достоевский", 408),
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
