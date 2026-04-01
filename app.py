from flask import Flask, render_template, request, jsonify
import PyPDF2
import io
import os
import openai
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import sqlalchemy_redshift
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Redshift connection configuration
def get_redshift_connection():
    """Create and return a Redshift connection using environment variables"""
    try:
        host = os.getenv('REDSHIFT_HOST')
        port = os.getenv('REDSHIFT_PORT', '5439')
        database = os.getenv('REDSHIFT_DATABASE')
        username = os.getenv('REDSHIFT_USERNAME')
        password = os.getenv('REDSHIFT_PASSWORD')
        
        if not all([host, database, username, password]):
            raise ValueError("Missing required Redshift connection parameters")
        
        # Use redshift+psycopg2 dialect for better Redshift compatibility
        connection_string = f"redshift+psycopg2://{username}:{password}@{host}:{port}/{database}"
        
        # Create engine with Redshift-specific settings
        engine = create_engine(
            connection_string,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={
                'sslmode': 'prefer',
                'connect_timeout': 30
            }
        )
        return engine
    except Exception as e:
        print(f"Error connecting to Redshift: {str(e)}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/redshift')
def redshift_dashboard():
    """Display Redshift dashboard page"""
    return render_template('redshift.html')

@app.route('/api/tables', methods=['GET'])
def get_tables():
    """Get list of tables from Redshift"""
    try:
        engine = get_redshift_connection()
        if not engine:
            return jsonify({'error': 'Failed to connect to Redshift'}), 500
        
        query = """
        SELECT schemaname, tablename 
        FROM pg_tables 
        WHERE schemaname NOT IN ('information_schema', 'pg_catalog', 'pg_internal')
        ORDER BY schemaname, tablename;
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            tables = [{'schema': row[0], 'table': row[1]} for row in result.fetchall()]
        
        return jsonify({'tables': tables})
    
    except Exception as e:
        return jsonify({'error': f'Error fetching tables: {str(e)}'}), 500

@app.route('/api/table-data', methods=['POST'])
def get_table_data():
    """Get data from a specific table"""
    try:
        data = request.get_json()
        schema_name = data.get('schema')
        table_name = data.get('table')
        limit = data.get('limit', 100)  # Default limit of 100 rows
        
        if not schema_name or not table_name:
            return jsonify({'error': 'Schema and table name are required'}), 400
        
        # Use raw psycopg2 connection for pandas compatibility
        try:
            host = os.getenv('REDSHIFT_HOST')
            port = os.getenv('REDSHIFT_PORT', '5439')
            database = os.getenv('REDSHIFT_DATABASE')
            username = os.getenv('REDSHIFT_USERNAME')
            password = os.getenv('REDSHIFT_PASSWORD')
            
            # Create raw psycopg2 connection for pandas
            conn = psycopg2.connect(
                host=host,
                port=int(port),
                database=database,
                user=username,
                password=password
            )
            
            # Get table data with limit
            query = f'SELECT * FROM "{schema_name}"."{table_name}" LIMIT {limit}'
            
            # Use raw connection with pandas
            df = pd.read_sql(query, conn)
            
            # Close the connection
            conn.close()
            
            # Convert DataFrame to JSON-serializable format
            # Handle datetime and other non-serializable types
            data_dict = df.to_dict(orient='records')
            for row in data_dict:
                for key, value in row.items():
                    if pd.isna(value):
                        row[key] = None
                    elif isinstance(value, (pd.Timestamp, datetime)):
                        row[key] = value.isoformat()
            
            # Get column names and types from DataFrame
            columns = [{'name': col, 'type': str(df[col].dtype)} for col in df.columns]
            
            return jsonify({
                'data': data_dict,
                'columns': columns,
                'row_count': len(data_dict),
                'schema': schema_name,
                'table': table_name
            })
            
        except Exception as db_error:
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error fetching table data: {str(e)}'}), 500

@app.route('/api/custom-query', methods=['POST'])
def execute_custom_query():
    """Execute a custom SQL query"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Basic security check - only allow SELECT statements
        if not query.upper().startswith('SELECT'):
            return jsonify({'error': 'Only SELECT queries are allowed'}), 400
        
        # Use raw psycopg2 connection for pandas compatibility
        try:
            host = os.getenv('REDSHIFT_HOST')
            port = os.getenv('REDSHIFT_PORT', '5439')
            database = os.getenv('REDSHIFT_DATABASE')
            username = os.getenv('REDSHIFT_USERNAME')
            password = os.getenv('REDSHIFT_PASSWORD')
            
            # Create raw psycopg2 connection for pandas
            conn = psycopg2.connect(
                host=host,
                port=int(port),
                database=database,
                user=username,
                password=password
            )
            
            # Use raw connection with pandas
            df = pd.read_sql(query, conn)
            
            # Close the connection
            conn.close()
            
            # Convert DataFrame to JSON-serializable format
            data_dict = df.to_dict(orient='records')
            for row in data_dict:
                for key, value in row.items():
                    if pd.isna(value):
                        row[key] = None
                    elif isinstance(value, (pd.Timestamp, datetime)):
                        row[key] = value.isoformat()
            
            return jsonify({
                'data': data_dict,
                'columns': [{'name': col, 'type': str(df[col].dtype)} for col in df.columns],
                'row_count': len(data_dict)
            })
            
        except Exception as db_error:
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error executing query: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            question = request.form.get('question', '').strip()
            if not question:
                return jsonify({'error': 'No question provided'}), 400
            # Compose the prompt
            prompt = f"PDF Content:\n{text}\n\nQuestion: {question}\nAnswer:"
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                return jsonify({'error': 'OpenAI API key not set in .env file'}), 500
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about PDF documents."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=128,
                    temperature=0
                )
                answer = response.choices[0].message.content.strip()
                return jsonify({'answer': answer})
            except Exception as e:
                return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
