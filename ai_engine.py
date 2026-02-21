import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def get_ai_business_context(table_metadata):
    try:
        prompt = f"""
        You are a Senior Data Architect. Analyze this database table metadata and provide:
        1. A 2-line business summary.
        2. Who would use this data.
        3. One potential business risk.

        Metadata: {table_metadata}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


def get_sql_help(user_question, schema_context):
    try:
        prompt = f"""
        You are an expert SQL Assistant.
        Database Schema: {schema_context}

        User Question: {user_question}

        Instructions:
        - Provide correct SQL.
        - Brief explanation.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"
