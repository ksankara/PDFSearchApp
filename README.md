# Data Dashboard Application

A comprehensive web application that combines PDF data extraction with Amazon Redshift database connectivity. This application provides two main functionalities:

1. **PDF Data Extractor**: Upload PDF files and ask questions about their content using OpenAI
2. **Redshift Dashboard**: Connect to Amazon Redshift and explore database tables with an interactive interface

## Features

### PDF Data Extraction
- Upload PDF files through web interface
- Ask natural language questions about PDF content
- Get AI-powered answers using OpenAI GPT

### Redshift Database Dashboard
- Connect to Amazon Redshift databases
- Browse all available tables and schemas
- View table data with customizable row limits (50, 100, 500, 1000 rows)
- Execute custom SQL queries
- Interactive table display with responsive design

## Prerequisites

- Python 3.8 or higher
- Amazon Redshift cluster with access credentials
- OpenAI API key (for PDF functionality)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository>
   cd PDFSearchApp
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```
   
   Edit `.env` file with your actual credentials:
   ```
   # OpenAI API Configuration (for PDF extraction)
   OPENAI_API_KEY=your_openai_api_key_here

   # Amazon Redshift Configuration
   REDSHIFT_HOST=your-redshift-cluster-endpoint.region.redshift.amazonaws.com
   REDSHIFT_PORT=5439
   REDSHIFT_DATABASE=your_database_name
   REDSHIFT_USERNAME=your_username
   REDSHIFT_PASSWORD=your_password
   ```

## Redshift Setup Requirements

### Connection Details
Your Redshift cluster must be:
- **Accessible** from your application environment
- **Configured** with proper security groups allowing PostgreSQL connections (port 5439)
- **Credentials** with read access to the databases and tables you want to explore

### Required Permissions
The Redshift user should have:
- `CONNECT` permission on the database
- `USAGE` permission on schemas
- `SELECT` permission on tables you want to query

### Security Groups
Ensure your Redshift cluster's security group allows:
- **Port**: 5439 (default Redshift port)
- **Source**: Your application's IP address or CIDR block

## Usage

### Starting the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### PDF Data Extraction

1. Navigate to the home page (`/`)
2. Upload a PDF file using the file input
3. Enter a question about the PDF content
4. Click "Submit" to get AI-generated answers

### Redshift Dashboard

1. Navigate to `/redshift` or click "Redshift Dashboard" in the navigation
2. Click "Load Tables" to fetch all available tables from your Redshift cluster
3. **Browse Tables**: 
   - Tables are organized by schema in the left sidebar
   - Click on any table name to view its data
   - Use the row limit dropdown to control how many rows are displayed
4. **Custom Queries**:
   - Switch to the "Custom Query" tab
   - Enter any SELECT statement
   - Click "Execute Query" to run it

## API Endpoints

### Redshift API Endpoints

- **GET** `/api/tables` - Fetch all tables and schemas
- **POST** `/api/table-data` - Get data from a specific table
  ```json
  {
    "schema": "public",
    "table": "users",
    "limit": 100
  }
  ```
- **POST** `/api/custom-query` - Execute custom SQL query
  ```json
  {
    "query": "SELECT * FROM public.users WHERE created_date > '2024-01-01' LIMIT 50"
  }
  ```

### PDF API Endpoints

- **POST** `/upload` - Upload PDF and ask question

## Dependencies

### Core Dependencies
- **Flask 2.3.3** - Web framework
- **psycopg2-binary 2.9.7** - PostgreSQL/Redshift database adapter
- **pandas 2.0.3** - Data manipulation and analysis
- **sqlalchemy 2.0.20** - SQL toolkit and ORM

### PDF Processing
- **PyPDF2 3.0.1** - PDF text extraction
- **openai** - OpenAI API integration

### Deployment
- **gunicorn** - WSGI server for production

## Security Considerations

1. **Environment Variables**: Never commit `.env` file with real credentials
2. **SQL Injection Protection**: Custom queries are limited to SELECT statements only
3. **Connection Security**: Use SSL/TLS for Redshift connections in production
4. **Access Control**: Implement proper authentication for production use

## Troubleshooting

### Common Connection Issues

1. **"Failed to connect to Redshift"**
   - Verify your credentials in `.env` file
   - Check if your IP is whitelisted in Redshift security groups
   - Ensure the cluster is publicly accessible or you're on the correct VPC

2. **"Error fetching tables"**
   - Verify the user has proper permissions
   - Check if the database name is correct

3. **Query execution errors**
   - Ensure you're using valid SQL syntax
   - Check that referenced tables exist and are accessible

### Performance Tips

1. **Large Tables**: Use appropriate LIMIT values when exploring large tables
2. **Complex Queries**: Be mindful of query execution time for complex operations
3. **Network**: Ensure stable network connection to Redshift cluster

## Development

### Project Structure
```
PDFSearchApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   ├── index.html        # PDF extraction interface
│   └── redshift.html     # Redshift dashboard interface
├── netlify.toml          # Netlify configuration
├── Procfile              # Heroku deployment configuration
└── windsurf_deployment.yaml
```

### Adding New Features

1. **Database Connections**: Add new database types by creating similar connection functions
2. **Query Features**: Extend the query interface with saved queries, query history, etc.
3. **Visualizations**: Add charts and graphs using libraries like Chart.js or D3.js
4. **Export Features**: Add CSV/Excel export functionality for query results

## Deployment

The application includes configuration files for various deployment platforms:

### Heroku
Use the included `Procfile`:
```
web: gunicorn app:app
```

### Netlify
Use the included `netlify.toml` configuration.

### Manual Deployment
Set environment variables and run:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Click the "Upload PDF" button
2. Select a PDF file from your computer
3. Click "Upload PDF" to process the file
4. The extracted text will be displayed below
