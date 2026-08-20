import sqlite3
import pandas as pd
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_PATH = 'prototype.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_validation_stats():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    
    total_records = len(df)
    duplicates = df[df.duplicated(subset=['employee_id'], keep=False)]
    duplicate_count = len(duplicates)
    
    null_salary = df[df['salary'].isnull()]
    null_count = len(null_salary)
    
    inconsistent = df[~df['department_id'].isin([1, 2, 3])]
    inconsistent_count = len(inconsistent)
    
    valid_records = total_records - (duplicate_count + null_count + inconsistent_count)
    if valid_records < 0: valid_records = 0
        
    return {
        'total': total_records,
        'valid': valid_records,
        'duplicates': duplicate_count,
        'nulls': null_count,
        'inconsistent': inconsistent_count
    }

@app.route('/')
def index():
    stats = get_validation_stats()
    return render_template('index.html', stats=stats)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/database')
def database():
    conn = get_db_connection()
    
    # Get table info
    tables = ['employees', 'departments', 'projects']
    schema_info = {}
    
    for table in tables:
        # Get count
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        # Get schema
        columns = conn.execute(f"PRAGMA table_info({table})").fetchall()
        schema_info[table] = {
            'count': count,
            'columns': [dict(col) for col in columns]
        }
        
    conn.close()
    return render_template('database.html', schema_info=schema_info)

@app.route('/sql', methods=['GET', 'POST'])
def sql():
    result = None
    columns = None
    error = None
    query = request.form.get('query', 'SELECT department_id, COUNT(*) AS employee_count\nFROM employees\nGROUP BY department_id;')
    
    if request.method == 'POST' and query:
        try:
            conn = get_db_connection()
            cursor = conn.execute(query)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()
            else:
                conn.commit()
                result = "Query executed successfully. (No data returned)"
            conn.close()
        except Exception as e:
            error = str(e)
            
    return render_template('sql.html', query=query, result=result, columns=columns, error=error)

@app.route('/validation')
def validation():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    
    total_records = len(df)
    
    # Check duplicates
    duplicates = df[df.duplicated(subset=['employee_id'], keep=False)]
    duplicate_count = len(duplicates)
    
    # Check nulls (specifically salary)
    null_salary = df[df['salary'].isnull()]
    null_count = len(null_salary)
    
    # Missing relationships (department not in 1,2,3)
    # Our setup script will have a bad department ID 99
    inconsistent = df[~df['department_id'].isin([1, 2, 3])]
    inconsistent_count = len(inconsistent)
    
    valid_records = total_records - (duplicate_count + null_count + inconsistent_count)
    if valid_records < 0:
        valid_records = 0
        
    stats = {
        'total': total_records,
        'valid': valid_records,
        'duplicates': duplicate_count,
        'nulls': null_count,
        'inconsistent': inconsistent_count
    }
    
    return render_template('validation.html', stats=stats, 
                           duplicates=duplicates.to_dict('records'),
                           nulls=null_salary.to_dict('records'),
                           inconsistent=inconsistent.to_dict('records'))

@app.route('/analysis')
def analysis():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    dept_df = pd.read_sql_query("SELECT * FROM departments", conn)
    conn.close()
    
    # KPIs
    kpis = {
        'total_employees': len(df['employee_id'].unique()), # rough estimate handling duplicates
        'avg_salary': round(df['salary'].mean(), 2) if not df['salary'].isnull().all() else 0,
        'total_departments': len(dept_df)
    }
    
    # Prepare chart data
    dept_counts = df['department_id'].value_counts().to_dict()
    # Map department ID to names
    dept_map = dict(zip(dept_df['department_id'], dept_df['department_name']))
    
    labels_dept = [dept_map.get(k, f"Unknown ({k})") for k in dept_counts.keys()]
    data_dept = list(dept_counts.values())
    
    return render_template('analysis.html', kpis=kpis, labels_dept=labels_dept, data_dept=data_dept)

@app.route('/reporting')
def reporting():
    return render_template('reporting.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
