from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_currency_data():
    response = client.get("/currencies/select_one?currency_code=eur_pln")
    assert response.status_code == 200
    assert "rate_date" in response.json()[0]
    assert "eur_pln" in response.json()[0]


def test_get_many_currency_data():
    response = client.get("/currencies/select_many?selected_columns=eur_pln&selected_columns=usd_pln")
    assert response.status_code == 200
    assert "rate_date" in response.json()[0]
    assert "eur_pln" in response.json()[0]
    assert "usd_pln" in response.json()[0]


def test_get_average_currency_rate():
    response = client.get("/currencies/eur_pln/average")
    assert response.status_code == 200
    assert "avarage for eur_pln" in response.json()


def test_get_maximum_currency_rate():
    response = client.get("/currencies/eur_pln/maximum")
    assert response.status_code == 200
    assert "maximum for eur_pln" in response.json()


def test_get_minimum_currency_rate():
    response = client.get("/currencies/eur_pln/minimum")
    assert response.status_code == 200
    assert "minimum for eur_pln" in response.json()


def test_get_currency_rate_date_range():
    response = client.get("/currencies/eur_pln/date-range?start_date=2023-11-01&end_date=2023-12-12")
    assert response.status_code == 200
    assert "rate_date" in response.json()[0]
    assert "eur_pln" in response.json()[0]
