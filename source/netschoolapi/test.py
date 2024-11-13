import asyncio
from netschoolapi import NetSchoolAPI
from netschoolapi.errors import AuthError


async def check_netschoolapi():
    ns = NetSchoolAPI('https://sgo.edu-74.ru')

    try:
        await ns.login(
            "АлексеевР1Р",
            "999999",
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

    name = names.name
    surname = names.surname
    role = role.role
    clas = clas.clas
    await ns.logout()
    print(role, f"{name} {surname}", clas)
    return role, name, clas

if __name__ == '__main__':
    asyncio.run(check_netschoolapi())