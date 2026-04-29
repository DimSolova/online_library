async def test_get_books(ac):
    books = await ac.get("/books")
    print(f"{books=}")

    assert books.status_code == 200
