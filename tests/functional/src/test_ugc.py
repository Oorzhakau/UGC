import pytest

from tests.functional.testdata.data import test_users_data, test_data_for_view
from tests.functional.settings import settings


@pytest.mark.asyncio
class TestUGC:
    @pytest.mark.parametrize(
        "request_body, authorization, expected_body, expected_answer", test_data_for_view
    )
    async def test_ugc_send_view(
            self,
            registration_user,
            make_post_request,
            kafka_consumer,
            request_body: dict,
            authorization: bool,
            expected_body: dict,
            expected_answer: dict,
    ):
        headers = None
        if authorization:
            response = await make_post_request(
                url=settings.AUTH_LOGIN_URL,
                data={"username": test_users_data[0]["username"],
                      "password": test_users_data[0]["password"]}
            )
            headers = {
                "Authorization": f"Bearer {response.body['access_token']}",
            }
        response = await make_post_request(url=settings.UGC_URL, data=request_body, headers=headers)
        response_body = {key: value for key, value in response.body.items() if key not in ["dt", "user_id"]}

        assert response.status == expected_answer["status"]
        assert response_body == {key: value for key, value in expected_body.items() if key not in ["dt", "user_id"]}

        if authorization:
            kafka_answer = {}
            async for msg in kafka_consumer:
                kafka_answer = {
                    "progress": int(msg.value),
                    "movie_id": msg.key.decode('utf-8').split('+')[1],
                }
                break
            assert kafka_answer == {key: value for key, value in expected_body.items() if key != "dt"}
