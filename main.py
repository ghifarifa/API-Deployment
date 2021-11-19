from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
from starlette.responses import RedirectResponse

class Product(BaseModel):
	id: int
	name: str
	category: str
	price: int
	stock: int = 0

json_filename="menu.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

app = FastAPI()

@app.get('/')
def root():
    return RedirectResponse('/docs')

@app.get('/menu')
async def read_all_menu():
	return data['menu']


@app.get('/menu/{product_name}')
async def read_menu(product_name: int):
	for menu_product in data['menu']:
		if menu_product['name'] == product_name:
			return menu_product
	raise HTTPException(
		status_code=404, detail=f'product not found'
	)

@app.post('/menu')
async def add_menu(product: Product):
	product_dict = product.dict()
	product_found = False
	for menu_product in data['menu']:
		if menu_product['id'] == product_dict['id']:
			product_found = True
			return "Menu ID "+str(product_dict['id'])+" exists."
	
	if not product_found:
		data['menu'].append(product_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)
		return product_dict
	raise HTTPException(
		status_code=404, detail=f'product not found'
	)

@app.patch('/menu')
async def update_menu(product: Product):
	product_dict = product.dict()
	product_found = False
	for menu_idx, menu_product in enumerate(data['menu']):
		if menu_product['id'] == product_dict['id']:
			product_found = True
			data['menu'][menu_idx]=product_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	if not product_found:
		return "Product ID not found."
	raise HTTPException(
		status_code=404, detail=f'product not found'
	)

@app.delete('/menu/{product_id}')
async def delete_menu(product_id: int):
	product_found = False
	for menu_idx, menu_product in enumerate(data['menu']):
		if menu_product['id'] == product_id:
			product_found = True
			data['menu'].pop(menu_idx)
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	if not product_found:
		return "Product ID not found."
	raise HTTPException(
		status_code=404, detail=f'product not found'
	)