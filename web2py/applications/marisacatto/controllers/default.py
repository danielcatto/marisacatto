# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ---


def index():
    import random

    form = SQLFORM.factory(
        Field('valor')
        )

    if form.process().accepted:
        valor_informado =  form.vars.valor
    else:
        valor_informado = 1
    
    valor_area_str = valor_informado #
    valor_area = int(valor_area_str)
    resultado_perimentro = valor_area * 4
    resultado_area = valor_area * valor_area
    resultado = valor_area, resultado_perimentro , resultado_area
    
   

    k = random.randint(0, 100)
    if k % 4 == 0:
        a = str(k), ' is divisible by 4'
    elif k%2 == 0:
        a = str(k), ' is even'
    else:
        a = str(k), ' is odd'

    res = 700 / 4


    if not session.counter:
        session.counter = 1
    else:
        session.counter += 1
    

    return dict(counter=session.counter, carrinho=session.carrinho, a=a, res=res, resultado=resultado, form=form)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)



# ---- novo controles --- ##
###########################################
############## CLIENTES ###################
###########################################




@auth.requires_login()
def cadastro_cliente():
    form = SQLFORM(Clientes)
    if form.process().accepted:
        session.flash = 'Cliente Cadastrado'
        redirect(URL('clientes'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Preencha todos os campos"
    return dict(form=form)

#lista todos os clientes
@auth.requires_login()
def clientes():
    clientes = db(Clientes).select()
    return dict(clientes=clientes)

@auth.requires_login()
def detalhar_cliente():
    cli = db(Clientes.id == request.args(0)).select()
    return dict(cli=cli)

@auth.requires_login()
def editar_cliente():
    form = SQLFORM(Clientes, request.args(0))
    if form.process().accepted:
        session.flash = "Cliente atualizado"
        
    elif form.errors:
        response.flash = "Erros no formulário"
    else:
        if not response.flash:
            response.flash = "Preencha o formulário"
    return dict(form=form)


def login():
    return dict(login=login)



###########################################
############## VENDAS #####################
###########################################
@auth.requires_login()
def vendas():
    return dict(vendas=vendas)

#vendas
@auth.requires_login()
def itens_compras():
    pass


@auth.requires_login()
def vender():
    cart=tuple()
    if not session.carrinho:
        session.carrinho = list()
        session.sub = 0
    
    form = SQLFORM.factory(
        Field('codigo', requires=IS_NOT_EMPTY(), label='Código'),
        Field('quantidade',requires=IS_NOT_EMPTY())
        )

    if form.process().accepted:
        produtos = db(Produtos.id == form.vars.codigo).select()
        if produtos:
            qtd = form.vars.quantidade
            total =  float(produtos[0]['valor']) * float(qtd)
            session.sub += total

            print('#'*80)
            print(session.sub)
            print('#'*80)
            cart = (produtos, qtd, total)
            session.carrinho.append(cart)
        else:
            print('#################\n\n\n\n\n\n\nferrou')
    else:
        produtos = 'vazio'
    print(type(produtos))
    return dict(form=form)

def finalizar():
    pass

#movimentação do caixa
@auth.requires_login()
def caixa():
    return dict(caixa=caixa)


#teste com data 
@auth.requires_login()
def contado_data():

    ano= 2019       #formato AAA
    mes=  5       #usar numeros
    dia= 22
    import datetime

    datapadrao = datetime.date(ano, mes, dia)
    hoje = datetime.date.today()

    if datapadrao > hoje:
        delta = datapadrao - hoje

    elif datapadrao <= hoje:
        delta = hoje - datapadrao

    resultado_delta = delta.days

    return resultado_delta


###########################################
############## PRODUTOS####################
###########################################
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