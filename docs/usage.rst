========
Usage
========

Translation
-----------

**Complilar textos a serem traduzidos**

* Criar uma pasta locale dentro de cada App que será traduzido.

* Criar arquivo para as mensagens a serem traduzidas::

    django-admin makemessages -l en

*O ultimo parametro é referente a linguagem que o arquivo será traduzida

* Traduzir o arquivo django.po

* Compliar arquivo traduzido::

    django-admin compilemessages

**NOTES**

* Não traduzir palavras dentro de {} pois são variáveis usadas pelo django e não texto a ser traduzido.

Pagination
----------
Pode usar parametros como filtros que os links da paginação irão redirecionar para a pagina certa com o link dos filtros ativos.

Na view::

    parametros = ''
    for item, value in request.GET.dict().items():
        if not item == 'page':
            parametros += '&{}={}'.format(item, value)
    parametros = parametros.replace(' ', '+')
     paginator = Paginator(queryset_list, PAGINACAO_QUANTIDADE_POR_PAGINA)

    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    [...]
    context['parametros'] = parametros
     return render(request, [...])

No template::

    {% include 'widgets/pagination.html' with object_list=query_list pagination_section='#section_target' %}

Criar o arquivo widgets/pagination.html na pasta templates com o seguinte conteudo::

    <div class="row">
        {% if object_list.paginator.num_pages > 1 %}
            <ul class="pagination">
                {% with ''|center:object_list.paginator.num_pages as range %}
                    {% for _ in range %}
                        <li{% if forloop.counter == object_list.number %} class="active"{% endif %}><a href="?page={{ forloop.counter }}{{ parametros }}{{ pagination_section }}">{{ forloop.counter }}</a></li>
                    {% endfor %}
                {% endwith %}
            </ul>
        {% endif %}
    </div>
