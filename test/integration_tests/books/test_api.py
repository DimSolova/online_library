import pytest

from test.helpers.auth import login_as_author


@pytest.mark.parametrize("user, title, description, isbn, author, status_code",[
    ("author1", "Идиот", "Книга про идиота", "9785389071278", "Ф.М. Достоевский", 200),
    ("author1", "Идиот", "Книга про идиота", "9785389071278", "Ф.М. Достоевский", 409),
    ("author2", "Идиот", "Книга про идиота", "9735389071278", "Ф.М. Достоевский", 200),
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
