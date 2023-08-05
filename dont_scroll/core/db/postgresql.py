import psycopg2

# TODO : config file
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "dont_scroll"
DB_PASSWORD = "passwd"
DB_NAME = "dont_scroll_db"
DB_TABLE = "public.slack_message"


class PostgreSQLClient:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                connect_timeout=3,
            )
            self.cursor = self.connection.cursor()
        except psycopg2.OperationalError as e:
            print(f"DB connect fail : {e}")
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=None):
        """쿼리 실행 메서드"""
        self.cursor.execute(query, params)
        if "SELECT" in query:
            return self.cursor.fetchall()

    def insert_data(self, table_name, data_dict):
        """INSERT 쿼리 실행 메서드"""
        columns = ", ".join(data_dict.keys())

        # 특별한 처리가 필요한 'vector' 값에 대한 처리
        values_placeholders = []
        for key, value in data_dict.items():
            if key == "vector":
                values_placeholders.append(value)
            else:
                values_placeholders.append("%s")
        values = ", ".join(values_placeholders)

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

        # 'vector' 값을 제외한 나머지 값들
        params = [v for k, v in data_dict.items() if k != "vector"]

        self.execute_query(query, params)
        self.connection.commit()

    def select_data(self, table_name, condition):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition}")
        result = self.cursor.fetchall()
        if result:
            col_names = [desc[0] for desc in self.cursor.description]
            return [dict(zip(col_names, row)) for row in result]
        return None

    # Delete
    def delete_data(self, table_name, condition, params=None):
        """DELETE 쿼리 실행 메서드"""
        query = f"DELETE FROM {table_name} WHERE {condition};"
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
        dbname=DB_NAME,
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
    client.insert_data(DB_TABLE, data)

    # Select
    result = client.execute_query("SELECT * FROM public.slack_message;")
    for row in result:
        print(row)

    # Delete
    client.delete_data(DB_TABLE, "url = %s", ["http://aaa"])

    client.close()
