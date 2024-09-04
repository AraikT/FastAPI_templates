from fastapi import APIRouter


def modify_standart_auth_endpoints(
    router: APIRouter, old_path: str, new_path: str
) -> None:
    """### Модификация пути стандартного роутера авторизации в fastapi-users.

    Новый путь в парметрах:

        route.path = '/login'
        route.path_format = '/login'

    должен совпадать с путем в настройках fastapi-users:

        bearer_transport = BearerTransport(tokenUrl='/login')

    если это условие соблюдено - кнопка "Autorize" в swagger будет работать как
    OAuth2PasswordBearer (OAuth2, password)

    Args:
        router (APIRouter): _description_
    """
    for route in router.routes:
        if route.path == old_path:
            route.path = new_path
            route.path_format = new_path
            route.include_in_schema = False
