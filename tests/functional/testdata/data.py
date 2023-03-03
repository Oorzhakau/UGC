from http import HTTPStatus

from tests.functional.enumerations.roles import RolesEnum

test_users_data = [
    {
        "username": "test_user",
        "email": "test_user@test.ru",
        "name": "Testi",
        "password": "qwerty_1234",
        "roles": [{"name": RolesEnum.BASE}],
    },
]

test_data_for_view = [
    (
        {
            "dt": "2023-02-23T01:03:45.729338",
            "movie_id": "matrix",
            "progress": 20
        },
        True,
        {
            "dt": "2023-02-23T01:03:45.729338",
            "movie_id": "matrix",
            "progress": 20
        },
        {"status": HTTPStatus.OK},
    ),
    (
        {
            "dt": "2023-02-23T01:03:45.729338",
            "movie_id": "matrix",
            "progress": 20
        },
        False,
        {
            "detail": "You don't have permissions for this api method"
        },
        {"status": HTTPStatus.FORBIDDEN},
    ),
]

test_data_for_etl = [
    {
        "dt": "2023-02-23T01:03:45.729338",
        "movie_id": "matrix",
        "progress": 20
    },
]
