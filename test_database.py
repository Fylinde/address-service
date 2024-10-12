from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user_addresses():
    response = client.get(
        "/addresses/users/29/addresses",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyOSwiaXNfYWRtaW4iOmZhbHNlLCJleHAiOjE3MjYzMTY1MzMsInN1YiI6IjI5In0.M6RPgJZF08ZvQDuf9YtG19JhOe5911caVyx7UHSpKcM"}
    )
    print(response.status_code)
    print(response.json())

test_get_user_addresses()
