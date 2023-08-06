import pytest
import string
import random
from dont_scroll.core.db.postgresql import PostgreSQLClient

# TODO : config file
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "dont_scroll"
DB_PASSWORD = "passwd"
DB_NAME = "dont_scroll_db"
DB_TABLE = "public.slack_message"


# TODO : config
@pytest.mark.skip_docker
@pytest.mark.parametrize(
    "host, port, user, password, db_name, db_table, is_pass",
    [
        (
            "127.0.0.1",
            5432,
            "dont_scroll",
            "passwd",
            "dont_scroll_db",
            "public.slack_message",
            True,
        ),
        (
            "127.0.0.1",
            5433,
            "dont_scroll",
            "passwd",
            "dont_scroll_db",
            "public.slack_message",
            False,
        ),
        (
            "127.0.0.1",
            5432,
            "dont_scroll_2",
            "passwd_2",
            "dont_scroll_db",
            "public.slack_message",
            False,
        ),
    ],
)
@pytest.mark.skip_docker
def test_db_connect(host, port, user, password, db_name, db_table, is_pass):
    """
    Similar images
    """

    client = PostgreSQLClient(
        host=host,
        port=port,
        user=user,
        password=password,
        db_name=db_name,
        db_table=db_table,
    )

    if is_pass:
        assert client.connection != None
    if not is_pass:
        assert client.connection == None


def get_db_client():
    db_client = PostgreSQLClient(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db_name=DB_NAME,
        db_table=DB_TABLE,
    )
    return db_client


@pytest.mark.skip_docker
@pytest.fixture(scope="module")
def db():
    db_client = get_db_client()
    yield db_client  # 테스트 함수에서 사용할 수 있도록 db_client를 반환합니다.
    db_client.close()


def generate_random_string(length=10):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


@pytest.mark.skip_docker
def test_db_insert_select_delete(db):
    # randon data
    random_data = generate_random_string()
    data = {
        "vector": "CUBE(ARRAY[2, 3, 4])",
        "url": f"{random_data}",
    }

    # insert
    db.insert_data(data)

    # select
    result = db.select_data(f"url='{random_data}'")
    assert result is not None, "데이터 선택 실패"
    assert result[0]["url"] == random_data

    # delete
    db.delete_data("url", [random_data])
    result_after_delete = db.select_data(f"url='{random_data}'")
    assert result_after_delete is None, "데이터 삭제 실패"


if __name__ == "__main__":
    test_db_connect(
        "127.0.0.1",
        5432,
        "dont_scroll",
        "passwd",
        "dont_scroll_db",
        True,
    )

    db_client = get_db_client()
    test_db_insert_select_delete(db_client)
