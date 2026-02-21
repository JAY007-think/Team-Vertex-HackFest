import pandas as pd
import numpy as np
from sqlalchemy import create_engine, inspect, text

class VertexMetadataEngine:
    """
    The Core Extraction Engine for VertexLens.
    Optimized for the Brazilian E-Commerce (Olist) Dataset.
    """
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.inspector = inspect(self.engine)

    def get_schema_details(self):
        schema_data = []
        tables = self.inspector.get_table_names()
        
        print(f"🚀 Vertex Engine: Scanning {len(tables)} tables...")
        
        for table in tables:
            columns = self.inspector.get_columns(table)
            pk = self.inspector.get_pk_constraint(table).get('constrained_columns', [])
            fks = self.inspector.get_foreign_keys(table)
            
            # Fetch 1000 rows for realistic Olist profiling
            try:
                query = text(f"SELECT * FROM {table} LIMIT 1000")
                sample_df = pd.read_sql(query, self.engine)
            except:
                sample_df = pd.DataFrame()
            
            # --- Advanced Statistical Profiling (As per Slide 6) ---
            # Calculate Mean (μ) and Std Dev (σ) for Numeric Columns (Price, Freight, etc.)
            numeric_cols = sample_df.select_dtypes(include=[np.number])
            stats = {}
            if not numeric_cols.empty:
                stats = {
                    "mean": numeric_cols.mean().round(2).to_dict(),
                    "std_dev": numeric_cols.std().round(2).to_dict()
                }

            # Data Quality Metrics
            trust_score = self._calculate_trust_score(sample_df)
            
            table_info = {
                "table_name": table,
                "primary_key": pk,
                "foreign_keys": fks,
                "columns": [
                    {
                        "name": col['name'],
                        "type": str(col['type']),
                        "nullable": col['nullable'],
                        "sample_values": sample_df[col['name']].head(3).tolist() if not sample_df.empty else []
                    } for col in columns
                ],
                "stats": stats,
                "quality_score": f"{trust_score}%",
                "row_count_scanned": len(sample_df)
            }
            schema_data.append(table_info)
            print(f"✅ Analyzed: {table}")
            
        return schema_data

    def _calculate_trust_score(self, df):
        """Calculates Data Completeness Score."""
        if df.empty: return 0
        completeness = (df.notnull().sum().sum() / df.size) * 100
        return round(completeness, 2)

# Usage for Team Vertex (Demo Purpose)
if __name__ == "__main__":
    # Pointing to the Olist Database
    CONNECTION_STR = "sqlite:///olist_ecommerce.db"
    
    extractor = VertexMetadataEngine(CONNECTION_STR)
    metadata = extractor.get_schema_details()
    
    print("\n💠 VertexLens Discovery Complete!")
    print(f"Total Tables Processed: {len(metadata)}")