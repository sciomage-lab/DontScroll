import psycopg2

class PostgreSQLClient:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        """쿼리 실행 메서드"""
        self.cursor.execute(query, params)
        if "SELECT" in query:
            return self.cursor.fetchall()

    def insert_data(self, table_name, data_dict):
        """INSERT 쿼리 실행 메서드"""
        columns = ', '.join(data_dict.keys())
        
        # 특별한 처리가 필요한 'vector' 값에 대한 처리
        values_placeholders = []
        for key, value in data_dict.items():
            if key == "vector":
                values_placeholders.append(value)
            else:
                values_placeholders.append('%s')
        values = ', '.join(values_placeholders)
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        
        # 'vector' 값을 제외한 나머지 값들
        params = [v for k, v in data_dict.items() if k != "vector"]
        
        self.execute_query(query, params)
        self.connection.commit()

    def close(self):
        """데이터베이스 연결 종료 메서드"""
        self.cursor.close()
        self.connection.close()

# 사용 예제:
if __name__ == "__main__":
    client = PostgreSQLClient(
        dbname="dont_scroll_db",
        user="cude_postgres",
        password="cude_postgres_password",
        host="127.0.0.1",
        port=5432
    )

    data = {
        "vector": "CUBE(ARRAY[2, 3, 4])",
        "url": "http://aaa",
    }
    client.insert_data("public.slack_message", data)

    result = client.execute_query("SELECT * FROM public.slack_message;")
    for row in result:
        print(row)

    client.close()

