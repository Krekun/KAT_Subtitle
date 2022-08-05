import sqlite3


class edit_database:
    def __init__(self) -> None:
        # Setup database
        self.dbname = "main.db"
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS api_table(name STRING PRIMARY KEY, api_key STRING)"
        )
        conn.commit()
        conn.close()

    def update_api_table(self, api_name, url):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT  * FROM api_table WHERE name=?)", (api_name,))
        is_data_exist = cur.fetchone()[0]
        if is_data_exist == 0:
            value_to_update = (api_name, url)
            cur.execute("INSERT INTO api_table values(?, ?)", value_to_update)
        else:
            value_to_update = (url, api_name)
            cur.execute("UPDATE api_table set api_key=? where name=?", value_to_update)
        conn.commit()
        conn.close()

    def get_api_table(self, api_name):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT api_key from api_table where name =?", (api_name,))
        temp = cur.fetchone()
        conn.close()
        return temp
