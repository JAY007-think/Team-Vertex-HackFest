import google.generativeai as genai
import os
from dotenv import load_dotenv
import PIL.Image # Image processing ke liye

load_dotenv()

# Step 1: API Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Model Initialization
# Gemini 1.5 Flash is mandatory for Vision/Images
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

# --- New Functions for Round 2 ---

def analyze_image(uploaded_file):
    """Processes ER-Diagrams or Schema screenshots using Vision"""
    try:
        img = PIL.Image.open(uploaded_file)
        prompt = """
        Analyze this image of a database schema or ER diagram.
        1. List all tables identified.
        2. Identify primary and foreign key relationships.
        3. Provide a brief business summary of what this database manages.
        """
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Vision Error: {str(e)}"

def analyze_url(url):
    """Extracts business context from a provided documentation URL"""
    try:
        # Simple RAG prompt: In a real app, you'd scrape the URL first. 
        # Here we ask Gemini to use its internal knowledge about the URL if public.
        prompt = f"""
        Analyze the documentation at this URL: {url}
        Extract the core business objectives, data entities, and potential stakeholders.
        Focus on how it relates to the Olist E-commerce ecosystem.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"URL Analysis Error: {str(e)}"

# --- Existing Functions ---

def get_ai_business_context(table_metadata):
    """Translates technical schema into business insights"""
    try:
        prompt = f"Analyze this Olist metadata: {table_metadata}. Give Business Purpose, Stakeholders, and interpret Mean ($\mu$) and Std Dev ($\sigma$)."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Context Error: {str(e)}"

def get_sql_help(user_question, schema_context):
    """Specialized SQL Assistant for Olist"""
    try:
        prompt = f"Context: {schema_context}. Question: {user_question}. Output valid SQL and logic."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"SQL Error: {str(e)}"