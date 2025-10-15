from django.core.mail import send_mail
from django.http import HttpResponse
import csv

def filtrar_produtos(produtos, filtro):
    if filtro:
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos


def ordenar_produtos(produtos, ordem):
    if ordem == "menor-preco":
        produtos = produtos.order_by("preco")
    elif ordem == "maior-preco":
        produtos = produtos.order_by("-preco")
    elif ordem == "mais-vendidos":
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.total_vendas(), produto))
        lista_produtos = sorted(lista_produtos, reverse=True, key=lambda tupla: tupla[0])
        produtos = [item[1] for item in lista_produtos]
    return produtos

def enviar_email_compra(pedido):
    email = pedido.cliente.email
    assunto = f"Pedido Aprovado: {pedido.id}"
    corpo = f"""Agradecemos pela sua compra! Seu pedido foi aprovado, segue as informações!
            ID do pedido: {pedido.id}
            Valor total: {pedido.preco_total}
            Quantidade de produtos: {pedido.quantidade_total}
            Cliente: {pedido.cliente}
            Codigo da transação: {pedido.codigo_transacao}"""
    remetente = "alissonmendes707@gmail.com"
    send_mail(assunto, corpo, remetente, [email])

def exportar_csv(informacoes):
    colunas = informacoes.model._meta.fields
    nomes_colunas = [coluna.name for coluna in colunas]

    resposta = HttpResponse(content_type="text/csv")
    resposta["Content-Disposition"] = "attachment; filename=relatorio.csv"

    criador_csv = csv.writer(resposta, delimiter=";")
    criador_csv.writerow(nomes_colunas)

    for linha in informacoes.values_list():
        criador_csv.writerow(linha)
    return resposta

# formulario do webhook

# Query strings
# collection_id	128101935222
# collection_status	approved
# payment_id	128101935222
# status	approved
# external_reference	null
# payment_type	credit_card
# merchant_order_id	34390020968
# preference_id	2710795215-87feb383-9462-4a5a-becb-dc935db76d78
# site_id	MLB
# processing_mode	aggregator
# merchant_account_id	null