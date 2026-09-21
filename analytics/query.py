import duckdb
from pathlib import Path
from load.warehouse import DB_PATH

SQL_DIR = Path(__file__).parent / "sql"

def main():
    con = duckdb.connect(str(DB_PATH), read_only=True)

    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        sql = sql_file.read_text(encoding="utf-8")
        df = con.execute(sql).fetchdf()
        print(f"\n=== {sql_file.name} ===")
        print(df.to_string(index=False))

    con.close()


if __name__ == "__main__":
    main()
