import mercadopago


public_key = "APP_USR-1380f063-875b-44fd-b899-04032742e739"
token = "APP_USR-1801120348173075-092615-dba48d6f74dc55196c8a604aea045e6a-2710795215"

def criar_pagamento(itens_pedido, link):
	sdk = mercadopago.SDK(token)

	itens = []
	for item in itens_pedido:
		quantidade = int(item.quantidade)
		nome_produto = item.item_estoque.produto.nome
		preco = float(item.item_estoque.produto.preco)
		itens.append({"title": nome_produto,
				"quantity": quantidade,
				"unit_price": preco})

	request = {
		"items": itens,
		"auto_return": "all",
		"back_urls": {
			"success": link,
			"failure": link,
			"pending": link,
		},
	}

	resposta = sdk.preference().create(request)
	link_pagamento = resposta["response"]["init_point"]
	id_pagamento = resposta["response"]["id"]
	return link_pagamento, id_pagamento


# ],
# 	"marketplace_fee": 0,
# 	"payer": {
# 		"name": "Test",
# 		"surname": "User",
# 		"email": "your_test_email@example.com",
# 		"phone": {
# 			"area_code": "11",
# 			"number": "4444-4444",
# 		},
# 		"identification": {
# 			"type": "CPF",
# 			"number": "19119119100",
# 		},
# 		"address": {
# 			"zip_code": "06233200",
# 			"street_name": "Street",
# 			"street_number": 123,
# 		},
# 	},

# ,
# 	"differential_pricing": {
# 		"id": 1,
# 	},
# 	"expires": False,
# 	"additional_info": "Discount: 12.00",
# 	"auto_return": "all",
# 	"binary_mode": True,
# 	"external_reference": "1643827245",
# 	"marketplace": "marketplace",
# 	"notification_url": "https://notificationurl.com",
# 	"operation_type": "regular_payment",
# 	"payment_methods": {
# 		"default_payment_method_id": "master",
# 		"excluded_payment_types": [
# 			{
# 				"id": "ticket",
# 			},
# 		],
# 		"excluded_payment_methods": [
# 			{
# 				"id": "",
# 			},
# 		],
# 		"installments": 5,
# 		"default_installments": 1,
# 	},
# 	"shipments": {
# 		"mode": "custom",
# 		"local_pickup": False,
# 		"default_shipping_method": None,
# 		"free_methods": [
# 			{
# 				"id": 1,
# 			},
# 		],
# 		"cost": 10,
# 		"free_shipping": False,
# 		"dimensions": "10x10x20,500",
# 		"receiver_address": {
# 			"zip_code": "06000000",
# 			"street_number": 123,
# 			"street_name": "Street",
# 			"floor": "12",
# 			"apartment": "120A",
# 		},
# 	},
# 	"statement_descriptor": "Test Store",
# }