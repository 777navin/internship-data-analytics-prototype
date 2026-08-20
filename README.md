# Data Analytics & SQL Validation Workflow Prototype

## 1. Project Objective
This is a functional prototype web application built for the **Review-1 presentation** of my internship as a Trainee Engineer – Data Science & Analytics at ProAzure Software Solutions Pvt. Ltd., Kharadi, Pune.

## 2. Problem Statement
Demonstrating the standard engineering workflow for structured data analysis, tracking the journey from raw requirements to final reporting while emphasizing data validation.

## 3. Proposed Workflow
**Requirement → Data Understanding → Database Exploration → SQL Query → Data Validation → Analysis → Reporting**

## 4. Architecture & 5. Technology Stack
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Data Processing**: Pandas
- **Charting**: Chart.js

## 6. Database Structure
Fictional representation of an internal HR/Project system:
- **Employees**: employee_id, employee_name, department_id, project_id, joining_date, salary, location
- **Departments**: department_id, department_name
- **Projects**: project_id, project_name, project_status

*(Note: Data contains intentional issues for validation testing.)*

## 7. Validation Approach
Uses Pandas to check for:
- Duplicate records
- NULL values
- Relational inconsistencies

## 8. SQL Functionality
Includes a built-in SQL runner against the SQLite database supporting joins, aggregations, and subqueries.

## 9. How to run the project
```bash
# Ensure Python is installed
pip install -r requirements.txt

# Initialize database
python setup_db.py

# Run the Flask app
python app.py
```
Then open `http://127.0.0.1:5000` in your web browser.

## 10. Prototype Limitations
- Sample dataset (not real production data)
- In-memory/SQLite database rather than a scalable cloud data warehouse
- Validation rules are hardcoded for demo purposes.

## 11. Future Scope
- Connect to a live MySQL/PostgreSQL database.
- Build dynamic validation rule configuration.
- Implement advanced predictive modeling in the Analysis module.

---
### How This Prototype Relates to My Internship
This prototype connects academic concepts (DBMS, SQL, Python) with an industry-oriented engineering workflow. It demonstrates how Data, Databases, SQL, Validation, Analysis, and Reporting interact holistically in a production setting.
