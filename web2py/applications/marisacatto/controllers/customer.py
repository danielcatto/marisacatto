# -*- coding: utf-8 -*-d

def index():
    
    query = db(Clientes).select()
    return dict(query=query)


@auth.requires_login()
def customer_registration():
    form = SQLFORM(Clientes)
    if form.process().accepted:
        session.flash = 'registered customer'
        redirect(URL('index'))
    elif form.errors:
        response.flash = "Erro"
    else:
        response.flash = "Fill in all fields"
    return dict(form=form)

#lista todos os clientes
@auth.requires_login()
def customers():
    query = ''
    form = SQLFORM.factory(
        Field('nome', requires=IS_NOT_EMPTY(), label='customer name')
        )
    if form.process().accepted:
        query = db(Clientes.nome.like('%'+request.vars.nome+'%')).select()
        if query:
            nome = query[0]['nome']
    return dict(query=query, form=form) 
    


@auth.requires_login()
def customer_detail():
    cli = db(Clientes.id == request.args(0)).select()
    return dict(cli=cli)

@auth.requires_login()
def customer_edit():
    form = SQLFORM(Clientes, request.args(0))
    if form.process().accepted:
        redirect(URL('customer/customer_detail', request.vars.id))
        
        session.flash = "updated client"
        
    elif form.errors:
        response.flash = "Erros no formulário"
    else:
        if not response.flash:
            response.flash = "Fill in all fields"
    return dict(form=form)


def login():
    return dict(login=login)
