import sqlite3
import os

DB_PATH = 'prototype.db'

def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Departments
    cursor.execute('''
    CREATE TABLE departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT
    )
    ''')
    
    # Create Projects
    cursor.execute('''
    CREATE TABLE projects (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT,
        project_status TEXT
    )
    ''')
    
    # Create Employees
    cursor.execute('''
    CREATE TABLE employees (
        employee_id INTEGER,
        employee_name TEXT,
        department_id INTEGER,
        project_id INTEGER,
        joining_date TEXT,
        salary REAL,
        location TEXT
    )
    ''')
    
    # Insert Departments
    cursor.executemany('INSERT INTO departments VALUES (?, ?)', [
        (1, 'Data Science'),
        (2, 'Data Analytics'),
        (3, 'Engineering')
    ])
    
    # Insert Projects
    cursor.executemany('INSERT INTO projects VALUES (?, ?, ?)', [
        (101, 'Customer Churn Analysis', 'Active'),
        (102, 'Sales Forecasting', 'Completed'),
        (103, 'Data Warehouse Migration', 'Active')
    ])
    
    # Insert Employees (with intentional errors)
    employees_data = [
        # Normal records
        (1001, 'Alice Smith', 1, 101, '2023-01-15', 850000.0, 'Pune'),
        (1002, 'Bob Jones', 2, 102, '2023-03-10', 720000.0, 'Mumbai'),
        (1003, 'Charlie Brown', 1, 101, '2023-05-22', 880000.0, 'Pune'),
        (1004, 'Diana Prince', 3, 103, '2022-11-01', 950000.0, 'Bangalore'),
        (1005, 'Evan Wright', 2, 101, '2023-08-14', 700000.0, 'Pune'),
        
        # INTENTIONAL ERRORS:
        # Duplicate record
        (1001, 'Alice Smith', 1, 101, '2023-01-15', 850000.0, 'Pune'),
        
        # NULL value in salary
        (1006, 'Frank Miller', 2, 102, '2023-09-01', None, 'Mumbai'),
        
        # Inconsistent value / Missing relationship (Department 99 does not exist)
        (1007, 'Grace Lee', 99, 103, '2023-10-12', 650000.0, 'Delhi')
    ]
    
    cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)', employees_data)
    
    conn.commit()
    conn.close()
    print("Database prototype.db created successfully with dummy data.")

if __name__ == '__main__':
    setup_db()
