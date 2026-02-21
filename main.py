import pandas as pd
from sqlalchemy import create_engine, inspect

class MetadataEngine:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.inspector = inspect(self.engine)

    def get_schema_details(self):
        schema_data = []
        tables = self.inspector.get_table_names()
        
        for table in tables:
            columns = self.inspector.get_columns(table)
            # Fetch sample data for AI context
            sample_df = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", self.engine)
            
            # Data Quality Metrics (Completeness)
            null_counts = sample_df.isnull().sum().to_dict()
            
            table_info = {
                "table_name": table,
                "columns": [
                    {
                        "name": col['name'],
                        "type": str(col['type']),
                        "nullable": col['nullable'],
                        "sample_values": sample_df[col['name']].tolist()
                    } for col in columns
                ],
                "row_count_sample": len(sample_df),
                "trust_score": self._calculate_trust_score(sample_df)
            }
            schema_data.append(table_info)
        return schema_data

    def _calculate_trust_score(self, df):
        if df.empty: return 0
        # Simple logic: (Non-null values / Total values) * 100
        completeness = (df.notnull().sum().sum() / df.size) * 100
        return round(completeness, 2)

# Example Usage (Postgres/SQLite)
# extractor = MetadataEngine("postgresql://user:pass@localhost:5432/db")
# metadata = extractor.get_schema_details()