import psycopg2

from dont_scroll import config
from dont_scroll.logger import applogger
from dont_scroll.utils import generate_random_hash


class PostgreSQLClient:
    """
    PostgreSQL Client
    """

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        db_name: str,
        db_table: str,
    ):
        """
        Init connect PostgreSQL
        :param host:
        :param port:
        :param user:
        :param password:
        :param db_name:
        :param db_table:
        """
        try:
            # Connect PostgreSQL
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=db_name,
                connect_timeout=3,
                client_encoding="utf8",
            )
            self.cursor = self.connection.cursor()

            # DB Table name
            self.db_table = db_table

        except psycopg2.OperationalError as e:
            print(f"DB connect fail : {e}")
            self.connection = None
            self.cursor = None
            self.db_table = None

    def execute_query(self, query: str, params=None):
        """쿼리 실행 메서드
        :param query:
        :param params:
        """
        self.cursor.execute(query, params)
        if "SELECT" in query:
            return self.cursor.fetchall()

    def insert_data(self, data_dict: dict):
        """INSERT 쿼리 실행 메서드
        :param dict data_dict:
        """
        columns = ", ".join(data_dict.keys())

        # 특별한 처리가 필요한 'vector' 값에 대한 처리
        values_placeholders = []
        params = []
        for key, value in data_dict.items():
            if key == "vector":
                values_placeholders.append(value)
            else:
                values_placeholders.append("%s")
                params.append(value)

        values = ", ".join(values_placeholders)

        query = f"INSERT INTO {self.db_table} ({columns}) VALUES ({values}) ON CONFLICT DO NOTHING;"

        self.execute_query(query, params)
        self.connection.commit()

    def select_data(self, condition):
        self.cursor.execute(f"SELECT * FROM {self.db_table} WHERE {condition}")
        result = self.cursor.fetchall()
        if result:
            col_names = [desc[0] for desc in self.cursor.description]
            return [dict(zip(col_names, row)) for row in result]
        return None

    def select_vector(self, vector, n):
        """Select vector
        :param list vector : query vector
        :param n int : top-n
        """
        self.cursor.execute(
            f"SELECT * FROM {self.db_table} ORDER BY vector <-> cube(ARRAY{vector}) LIMIT {n}"
        )
        result = self.cursor.fetchall()
        if result:
            col_names = [desc[0] for desc in self.cursor.description]
            return [dict(zip(col_names, row)) for row in result]
        return None

    # Delete
    def delete_data(self, condition: str, params: list = None):
        """Delete
        :param str condition: HINT) "file_url = %s"
        :param list params: HINT) ["http://aaa"]
        """
        query = f"DELETE FROM {self.db_table} WHERE {condition} = ANY(%s);"
        self.execute_query(query, (params,))
        self.connection.commit()

    def close(self):
        """데이터베이스 연결 종료 메서드"""
        self.cursor.close()
        self.connection.close()


# 사용 예제:
if __name__ == "__main__":
    path = os.path.join(os.path.expanduser("~"), ".config/dont_scroll/config.toml")
    config.load(path)

    client = PostgreSQLClient(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db_name=config.DB_NAME,
        db_table=config.DB_TABLE,
    )
    if client.connection == None:
        applogger.critical("client connection fail")
        exit()

    # Insert
    test_id = f"test-{generate_random_hash()}"
    data = {
        "vector": "CUBE(ARRAY[2, 3, 4])",
        "file_url": "http://aaa",
        "client_msg_id": test_id,
        "text": None,
    }
    client.insert_data(data)

    # Select
    result = client.execute_query("SELECT * FROM public.slack_message;")
    for row in result:
        print(row)

    # Delete
    client.delete_data("file_url", ["http://aaa"])

    client.close()
