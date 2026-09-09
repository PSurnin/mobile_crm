async def test_user_get_me(async_client):
    response = await async_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == "manager@test.com"
