import google.generativeai as genai
import os

# API Key setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Using Gemini 1.5 Flash for high-speed metadata enrichment
model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_business_context(table_metadata):
    """
    Translates technical Olist schema into business-friendly insights.
    Uses Statistical metrics (Mean/Std Dev) to provide deeper context.
    """
    try:
        # Vertex System Prompt for Olist Dataset
        prompt = f"""
        You are a Senior Data Architect at an E-commerce firm. 
        Analyze this table metadata from the 'Brazilian E-Commerce (Olist)' dataset.
        
        Metadata: {table_metadata}
        
        Provide the following in a structured format:
        1. **Business Purpose**: A 2-line summary of what this table represents in the e-commerce lifecycle.
        2. **Stakeholders**: Who (e.g., Marketing, Logistics, Finance) would use this data.
        3. **Statistical Insight**: Interpret the provided Mean and Std Dev metrics (if available).
        4. **Data Risk**: One potential business risk (e.g., 'Null review scores might hide customer dissatisfaction').
        
        Keep it professional and crisp for a dashboard view.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Vertex AI Error: {str(e)}"


def get_sql_help(user_question, schema_context):
    """
    RAG-based SQL Assistant specialized in Olist multi-table joins.
    """
    try:
        prompt = f"""
        You are Vertex AI, an expert SQL Assistant for the Olist E-commerce database.
        
        Context (All Tables & Columns): {schema_context}
        
        User Question: {user_question}

        Instructions:
        - Provide accurate SQL for SQLite/PostgreSQL.
        - Use JOINs where necessary (e.g., link 'orders' to 'customers' using 'customer_id').
        - Explain the logic in 2 simple sentences.
        - If the question is not about the data, politely ask to stay on topic.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Vertex AI Error: {str(e)}"