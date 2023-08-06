import psycopg2

# TODO : config file
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "dont_scroll"
DB_PASSWORD = "passwd"
DB_NAME = "dont_scroll_db"
DB_TABLE = "public.slack_message"


class PostgreSQLClient:
    """
    PostgreSQL Client
    """
    def __init__(self, host: str, port: int, user: str, password: str, db_name: str, db_table: str):
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
        for key, value in data_dict.items():
            if key == "vector":
                values_placeholders.append(value)
            else:
                values_placeholders.append("%s")
        values = ", ".join(values_placeholders)

        query = f"INSERT INTO {self.db_table} ({columns}) VALUES ({values});"

        # 'vector' 값을 제외한 나머지 값들
        params = [v for k, v in data_dict.items() if k != "vector"]

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
    def delete_data(self, condition: str, params: list=None):
        """Delete
        :param str condition: HINT) "url = %s"
        :param list params: HINT) ["http://aaa"]
        """
        query = f"DELETE FROM {self.db_table} WHERE {condition};"
        self.execute_query(query, params)
        self.connection.commit()

    def close(self):
        """데이터베이스 연결 종료 메서드"""
        self.cursor.close()
        self.connection.close()


# 사용 예제:
if __name__ == "__main__":
    client = PostgreSQLClient(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db_name=DB_NAME,
    )
    if client.connection == None:
        # TODO : error logger
        print("Fail")
        exit()

    # Insert
    data = {
        "vector": "CUBE(ARRAY[2, 3, 4])",
        "url": "http://aaa",
    }
    client.insert_data(data)

    # Select
    result = client.execute_query("SELECT * FROM public.slack_message;")
    for row in result:
        print(row)

    # Delete
    client.delete_data("url = %s", ["http://aaa"])

    client.close()
