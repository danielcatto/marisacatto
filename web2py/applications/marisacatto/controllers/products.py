# -*- coding: utf-8 -*-
def index():
    return dict(produtos=produtos)


def show_products():
    if request.vars.category:
        product_list = db(db.product.default_category == request.vars.category).select(limitby=(0,20),
                                                                            orderby=db.product.name)
    else:
        product_list = db(db.product).select(limitby=(0,20), orderby=~db.product.name)
    return locals()
    
@auth.requires_login()
def cadastro_produto():
    form = SQLFORM(Produtos)

    if form.process().accepted:
        session.flash = 'Produto Cadastrado'
        redirect(URL('produtos'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Preencha todos os campos"
    return dict(form=form)

@auth.requires_login()
def produtos():
    produtos = db(Produtos).select()

    return dict(produtos=produtos)


@auth.requires_login()
def detalhe_produto():
    produtos = db(Produtos.id == request.args(0)).select()
    return dict(produtos=produtos)


@auth.requires_login()
def editar_produto():
    form = SQLFORM(Produtos, request.args(0))
    if form.process().accepted:
        session.flash = "Produto atualizado"

        
    elif form.errors:
        response.flash = "Erros no formulário"
    else:
        if not response.flash:
            response.flash = "Preencha o formulário"
    return dict(form=form)


@auth.requires_login()
def gerenciar_produtos():
    return dict(produtos=produtos)

@auth.requires_login()
def categorias():
    categorias = db(Categorias).select()
    return dict(categorias=categorias)


@auth.requires_login()
def cadastro_categorias():
    form = SQLFORM(Categorias)
    if form.process().accepted:
        session.flash = 'Nova categoria cadastrada: %s' % form.vars.nome_categoria
        redirect(URL('categorias'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Preencha todos os campos"
    return dict(form=form)