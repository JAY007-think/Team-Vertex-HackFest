import pandas as pd
from sqlalchemy import create_engine, inspect, text
import numpy as np

def get_db_metadata(connection_string):
    """
    The Vertex Extraction Engine: 
    Extracts schema, identifies relationships, and performs statistical profiling.
    """
    engine = create_engine(connection_string)
    inspector = inspect(engine)
    all_tables = []
    
    # 1. Get all table names
    table_names = inspector.get_table_names()
    
    for table_name in table_names:
        # 2. Extract Basic Schema
        columns = inspector.get_columns(table_name)
        pk = inspector.get_pk_constraint(table_name).get('constrained_columns', [])
        fks = inspector.get_foreign_keys(table_name)
        
        # 3. Statistical Profiling & Quality Analysis
        try:
            # We use LIMIT 1000 to prevent crashing on massive enterprise tables
            query = text(f"SELECT * FROM {table_name} LIMIT 1000")
            df = pd.read_sql(query, engine)
            
            # --- Mathematical Statistical Analysis ---
            # Completeness: (Non-null values / total potential values)
            total_cells = df.size
            null_cells = df.isnull().sum().sum()
            completeness = round(((total_cells - null_cells) / total_cells) * 100, 2) if total_cells > 0 else 0
            
            # Uniqueness Score (average across columns)
            uniqueness = round(df.nunique().mean() / len(df) * 100, 2) if len(df) > 0 else 0
            
            # Descriptive Stats for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number])
            stats = {}
            if not numeric_cols.empty:
                stats = {
                    "mean": numeric_cols.mean().to_dict(),
                    "std_dev": numeric_cols.std().to_dict()
                }

        except Exception as e:
            completeness = 0
            uniqueness = 0
            df = pd.DataFrame()
            stats = {}

        # 4. Compile Metadata Object
        all_tables.append({
            "table_name": table_name,
            "columns": [col['name'] for col in columns],
            "column_details": [{"name": c['name'], "type": str(c['type'])} for c in columns],
            "primary_key": pk,
            "foreign_keys": fks, # Crucial for Lineage!
            "quality": f"{completeness}%",
            "uniqueness": f"{uniqueness}%",
            "row_count_sample": len(df),
            "stats": stats
        })
        
    return all_tables