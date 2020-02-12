routers = {
    marisacatto: dict(
        default_language=possible_languages['default'][0],
        languages=[lang for lang in possible_languages if lang != 'default']
    )
}

routers = dict(
BASE = dict(default_application='marisacatto',
default_controller='default'),
)
