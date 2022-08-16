import sqlite3


class Edit_database:
    def __init__(self) -> None:
        # Setup database
        self.dbname = "main.db"
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS api_table(name STRING PRIMARY KEY, api_key STRING NOT NULL)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS spoken_sentences"
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT,spoken_sentence STRING NOT NULL,"
            "created TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')))"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS avatar_config"
            "(blueprint STRING PRIMARY KEY ,update_date TIMESTAMP , value json NOT NULL,"
            "created TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')))"
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

    def update_spoken_sentences(self, sentence):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        value_to_update = (sentence,)
        cur.execute(
            "INSERT INTO spoken_sentences(spoken_sentence) values(?)", value_to_update
        )
        conn.commit()
        conn.close()

    def get_spoken_sentences(self):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT * from spoken_sentences")
        temp = cur.fetchall()
        conn.close()
        return temp

    def update_avatar_config(self, blueprint, date, value):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        temp = str(value).replace("'", '"') #Without this replace, json will be broken
        cur.execute(
            "SELECT EXISTS(SELECT  * FROM avatar_config WHERE blueprint=?)",
            (blueprint,),
        )
        is_data_exist = cur.fetchone()[0]
        if is_data_exist == 0:
            cur.execute(
                "INSERT INTO avatar_config(blueprint,update_date,value) values(?,?,?)",
                (blueprint, date, temp),
            )
        else:
            pass
            # cur.execute(
            #     "UPDATE avatar_config set value = ?  WHERE blueprint=?",
            #     (
            #         temp,
            #         blueprint,
            #     ),
            # )
        conn.commit()
        conn.close()

    def get_avatar_config(self, blueprint):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT value from avatar_config where blueprint =?", (blueprint,))
        temp = cur.fetchone()
        conn.close()
        return temp
