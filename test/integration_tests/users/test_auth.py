from src.services.users import UserService


def test_decode_and_encode_token():
    data = {"user_id": 1}
    jwt_token = UserService().create_access_token(data)
    assert jwt_token
    assert isinstance(jwt_token, str)
    payload = UserService().decode_token(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]
