from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(status_ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)

def loja(request, nome_categoria=None):
    banners = Banner.objects.filter(status_ativo=True)
    produtos = Produto.objects.filter(ativo=True)
    if nome_categoria:
        produtos = produtos.filter(categoria__nome=nome_categoria)
    context = {"produtos": produtos, "banners": banners}
    return render(request, 'loja.html', context)

def ver_produto(request, id_produto):
    tem_estoque = False
    tamanhos = {}
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    if len(itens_estoque) > 0:
        tem_estoque = True
        tamanhos = {item.tamanho for item in itens_estoque}
    context = {"produto": produto, "itens_estoque": itens_estoque, "tem_estoque": tem_estoque, "tamanhos": tamanhos}
    return render(request, "ver_produto.html", context)

def checkout(request):
    return render(request, 'checkout.html')

def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        if not tamanho:
            return redirect('loja')
        # Pegar o cliente
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, status_pedido=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save()
        
        return redirect('carrinho')
    else:
        return redirect('loja')

def remover_carrinho(request):
    return redirect('carrinho')

def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, status_pedido=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = {"itens_pedido": itens_pedido, "pedido": pedido}
    return render(request, 'carrinho.html', context)

def minha_conta(request):
    return render(request, 'usuario/minha_conta.html')

def login(request):
    return render(request, 'usuario/login.html')