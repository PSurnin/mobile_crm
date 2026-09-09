async def test_create_lead(async_client):
    payload = {"name": "John", "phone":"911", "email":"john911@hotmail.com"}
    response = await async_client.post("/leads/add", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    assert response.json()["public_id"]

async def test_get_lead(async_client, make_lead):
    fake_lead = await make_lead()
    response = await async_client.get(f"/leads/get/{fake_lead.public_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"

async def test_fail_list_leads(async_client):
    response = await async_client.get(f"/leads/list?limit=999")
    assert response.status_code == 422

async def test_list_lead_limit(async_client, make_lead):
    for i in range(3):
        await make_lead()
    response = await async_client.get(f"/leads/list?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
