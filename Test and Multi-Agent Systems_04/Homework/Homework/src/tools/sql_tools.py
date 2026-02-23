import duckdb


class SQLTools:
    """Tools for querying DuckDB taxi dataset"""

    def __init__(self, db_file):
        self.con = duckdb.connect(db_file)

    def get_schema(self) -> str:
        """Get the schema of the trips table with column names and types"""
        rows = self.con.execute("DESCRIBE trips").fetchall()
        return "\n".join([f"{r[0]} ({r[1]})" for r in rows])

    def run_sql(self, query: str) -> str:
        """Execute a SQL query and return results as formatted text (max 50 rows)"""
        result = self.con.execute(query)
        columns = [d[0] for d in result.description]
        rows = result.fetchmany(50)

        output = " | ".join(columns) + "\n"
        output += "-" * 60 + "\n"
        for row in rows:
            output += " | ".join(str(x) for x in row) + "\n"

        return output
