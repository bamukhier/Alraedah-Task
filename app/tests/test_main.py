from fastapi.testclient import TestClient
from src.main import app, html_content
import os

client = TestClient(app)

def test_home_page():
    res = client.get('/')
    assert res.status_code == 200
    assert res.text == html_content

def test_non_csv_upload():
    file_path = 'test-data/non-csv.txt'
    res = client.post('/top-products', files={'uploaded_file': open(file_path)})
    assert res.status_code == 400
    assert res.json() == {
        "detail": "The uploaded file must be a CSV file"
    }

def test_single_top_product():
    file_path = 'test-data/single-top-product.csv'
    res = client.post('/top-products', files={'uploaded_file': open(file_path)})
    print(res)
    assert res.status_code == 200
    assert res.json() == {
            "top_product": "Massoub gift card",
            "product_rating": 5.0
    }

def test_multiple_top_products():
    file_path = 'test-data/multiple-top-products.csv'
    res = client.post('/top-products', files={'uploaded_file': open(file_path)})
    assert res.status_code == 200
    assert res.json() == {
        "top_products": 
        [
            "Massoub gift card",
            "Mandi gift card"
        ],
        "product_rating": 5.0
    }

def test_duplicate_top_products():
    file_path = 'test-data/duplicates-top-products.csv'
    res = client.post('/top-products', files={'uploaded_file': open(file_path)})
    assert res.status_code == 200
    assert res.json() == {
            "top_product": "Massoub gift card",
            "product_rating": 5.0
    }

def test_invalid_file_structure():
    file_path = 'test-data/invalid-structure.csv'
    res = client.post('/top-products', files={'uploaded_file': open(file_path)})
    assert res.status_code == 400
    assert res.json() == {
        "detail": "The CSV file is either empty or malformated. The file must contain at least one row of products and two columns <product_name>, <customer_avrage_rating>"
    }