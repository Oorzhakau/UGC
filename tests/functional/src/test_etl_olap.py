import asyncio

import pytest
import time
from clickhouse_driver.errors import Error

from tests.functional.testdata.data import test_users_data, test_data_for_etl
from tests.functional.settings import settings


@pytest.mark.asyncio
class TestETLOlap:
    @pytest.mark.parametrize(
        "request_body", test_data_for_etl
    )
    async def test_etl(
            self,
            registration_user,
            clickhouse_client,
            make_post_request,
            request_body: dict,
    ):
        response = await make_post_request(
            url=settings.AUTH_LOGIN_URL,
            data={"username": test_users_data[0]["username"],
                  "password": test_users_data[0]["password"]}
        )
        headers = {
            "Authorization": f"Bearer {response.body['access_token']}",
        }
        time_for_waiting = time.time() + settings.ETL_SLEEP_TIME + 5
        delta = time_for_waiting
        rows = []
        while delta > 0:
            try:
                await make_post_request(url=settings.UGC_URL, data=request_body, headers=headers)
                rows = clickhouse_client.execute("SELECT * FROM views LIMIT 1 ")
            except Error:
                await asyncio.sleep(2)
            delta = time_for_waiting - time.time()
            if rows:
                break
        if not rows:
            assert False, "Data doesn't load to Clickhouse"
        assert (rows[0][2], rows[0][3]) == (request_body["movie_id"], request_body["progress"])
