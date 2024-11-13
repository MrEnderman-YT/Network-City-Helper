import asyncio
from netschoolapi import NetSchoolAPI
from netschoolapi.errors import AuthError


async def check_netschoolapi(login, password):
    ns = NetSchoolAPI('https://sgo.edu-74.ru')

    try:
        await ns.login(
            login,
            password,
            'МБОУ "СОШ № 99 г. Челябинска"',
        )
    except AuthError as e:
        print(f"Ошибка аутентификации!")
        return "AuthError"

    except Exception as e:
        print(f"Произошла ошибка")
        return "Error"

    role = await ns.role()
    names = await ns.name()
    clas = await ns.clas()

    role = role.role
    name = names.name
    surname = names.surname
    clas = clas.clas

    await ns.logout()

    return role, name, surname, clas
