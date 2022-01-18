from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from .utils import process_uploaded_file

app = FastAPI(title="Alraedah-API", version="0.0.1")



@app.post('/top-products')
async def find_top_products(uploaded_file: UploadFile = File(...)):

    df = process_uploaded_file(uploaded_file)
    top_products = df[df['customer_avrage_rating'] == df['customer_avrage_rating'].max()]
    print(top_products)
    if top_products.shape[0] == 1:
        return {
            "top_product": list(top_products.product_name)[0],
            "product_rating": top_products.customer_avrage_rating[0]
        }
    else:
        return {
            "top_products": list(top_products.product_name),
            "product_rating": list(top_products.customer_avrage_rating)[0]
        }


@app.get('/')
async def index():
    return HTMLResponse(html_content)

html_content = """    
<head>
<title>Alraedah Task</title>
<style>
  body {margin:0 auto; width:450px; text-align: center;}
</style>
</head>
<body>
<h1>Alraedah Top Products</h1>
<form action="/top-products" method="post" enctype="multipart/form-data">
<input name="uploaded_file" type="file" accept=".csv" required>
<input type="submit">
</form>
</body>
"""