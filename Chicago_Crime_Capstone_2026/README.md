# Chicago Crime Data Analytics and Reporting System

## 1. Project Overview

The Chicago Crime Data Analytics and Reporting System is a Python-based full-stack capstone project developed to analyze, visualize and report crime patterns using the supplied Chicago crime datasets.

The project covers data cleaning, exploratory data analysis, statistical analysis, SQLite database management and web application development. The Flask application provides an analytical dashboard with nine visualizations and a Police District Management module that supports GET, POST, PUT, PATCH, DELETE and search operations.

## 2. Project Objectives

- Clean and standardize the supplied crime datasets without losing valid records.
- Analyze yearly crime trends, crime categories and arrest patterns.
- Examine monthly, weekday and community-level crime distributions.
- Identify statistical relationships and outliers.
- Store structured data in a relational SQLite database.
- Generate analytical reports using SQL queries and views.
- Present analytical findings through a Flask dashboard.
- Manage police district records while maintaining data integrity.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and application development |
| Pandas | Data cleaning and exploratory analysis |
| NumPy | Numerical and statistical calculations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| SQLite3 | Relational database management |
| SQLAlchemy | Database connectivity and SQL execution |
| Flask | Web application and REST API development |
| HTML | Web page structure |
| CSS | External stylesheets for user interface styling and responsive layouts |
| Jupyter Notebook | Analytical use case implementation |
| Visual Studio Code | Development environment |

## 4. Project Structure

```
Chicago_Crime_Capstone_2026/
│
├── data/
│   ├── raw/
│   │   ├── chicago_city_community.csv
│   │   ├── chicago_crime_dataset.csv
│   │   ├── chicago_district_ps_info.csv
│   │   ├── chicago_police_beat_info.csv
│   │   ├── chicago_ward_offices.csv
│   │   └── iucr_codes.csv.csv
│   │
│   ├── cleaned/
│   │   ├── chicago_crime_cleaned.csv
│   │   └── chicago_crime_features.csv
│   │
│   └── chicago_crime.db
│
├── notebooks/
│   ├── 01_UC1_load_and_clean.ipynb
│   ├── 02_UC2_exploratory_analysis.ipynb
│   ├── 03_UC3_statistical_analysis.ipynb
│   └── 04_UC4_database_reporting.ipynb
│
├── src/
│   └── district_routes.py
│
├── static/
│   ├── charts/
│   │   ├── crime_trend_over_years.png
│   │   ├── top_10_crime_categories.png
│   │   ├── crime_month_weekday_heatmap.png
│   │   ├── top10_communities.png
│   │   ├── crime_hourly_distribution.png
│   │   ├── community_crime_boxplot.png
│   │   ├── crime_correlation_heatmap.png
│   │   ├── sql_yearly_crime_report.png
│   │   └── sql_crime_category_report.png
│   │
│   └── css/
│       ├── dashboard.css
│       └── districts.css
│
├── templates/
│   ├── dashboard.html
│   └── districts.html
│
├── app.py
├── config.py
├── README.md
└── requirements.txt
```

## 5. Dataset Description

The project uses six supplied CSV datasets.

| Dataset | Description |
|---|---|
| chicago_crime_dataset.csv | Primary crime incident records |
| chicago_city_community.csv | Community area and population information |
| chicago_district_ps_info.csv | Police district and station information |
| chicago_police_beat_info.csv | Police beat and sector information |
| chicago_ward_offices.csv | Ward office and administrative information |
| iucr_codes.csv.csv | Illinois Uniform Crime Reporting classification codes |

The primary crime dataset contains 498 records and 20 columns. Malformed quotation marks in the source CSV are handled through line-by-line parsing to preserve valid records.

The original datasets are retained in the `data/raw/` folder, while cleaned and feature-engineered datasets are stored separately in the `data/cleaned/` folder.

## 6. Project Workflow

```
Original CSV Datasets
         |
         v
Data Loading and Cleaning
         |
         v
Feature Engineering
         |
         v
Missing Value Analysis
         |
         v
SQLite Database Creation and Insertion
         |
         v
Exploratory Data Analysis
         |
         v
Statistical Analysis
         |
         v
SQL Database Reporting
         |
         v
Flask Web Application
         |
         +-- Crime Analytics Dashboard
         |
         +-- Police District Management
```

## 7. Use Case Implementation

### Use Case 1: Data Loading and Cleaning

Notebook: `01_UC1_load_and_clean.ipynb`

- Load the primary crime dataset into a Pandas DataFrame.
- Inspect the first ten records, dataset dimensions, schema and data types.
- Handle malformed CSV quotation marks without discarding valid records.
- Convert the date column into datetime format.
- Identify and handle missing values in key fields.
- Standardize categorical values by removing unnecessary whitespace and unifying case.
- Generate Year, Month and DayOfWeek features while validating the existing year column.
- Perform missing value analysis using NumPy.
- Evaluate columns exceeding the 50% missing value threshold.
- Create and populate the SQLite database.
- Validate record counts and unique identifiers.
- Answer the assessment questions related to crime categories and date anomalies.

### Use Case 2: Exploratory Data Analysis

Notebook: `02_UC2_exploratory_analysis.ipynb`

- Analyze yearly crime trends using a line chart.
- Identify the top ten crime categories with counts and percentages.
- Calculate overall and yearly arrest rates.
- Examine monthly and weekday crime distributions using a heatmap.
- Identify the top ten community areas based on recorded crime counts.
- Generate analytical charts with relevant observations.
- Answer the assessment questions related to crime categories, arrest rate consistency and monthly crime frequency.

### Use Case 3: Statistical Analysis

Notebook: `03_UC3_statistical_analysis.ipynb`

- Examine hourly crime distribution and identify limitations in the source timestamps.
- Calculate community-level crime statistics using NumPy.
- Apply the Interquartile Range (IQR) method to identify outliers.
- Visualize community crime distribution using a box plot.
- Generate a correlation matrix for selected numerical variables.
- Visualize statistical relationships using a correlation heatmap.
- Interpret statistical findings and their limitations.

### Use Case 4: Database Reporting

Notebook: `04_UC4_database_reporting.ipynb`

- Store reference datasets and analytical summaries in SQLite.
- Generate structured summary tables for crime and arrest reporting.
- Retrieve yearly crime counts using SQL queries.
- Identify the top five crime categories with their percentages.
- Calculate yearly arrest counts.
- Create SQL views for yearly and category-wise reporting.
- Retrieve SQL view results into Pandas DataFrames.
- Generate visualizations using SQL-derived results.
- Validate database records and analytical summaries.

## 8. Database Design

Database: `data/chicago_crime.db`

The SQLite database stores crime records, related reference information and analytical summaries.

### Main Tables

| Table | Description |
|---|---|
| crime_records | Primary crime incident records |
| iucr_codes | Crime classification information |
| police_districts | Police district information |
| ward_offices | Ward office information |
| community_areas | Community area information |
| police_beats | Police beat information |

### Summary Tables

| Table | Description |
|---|---|
| summary_crime_yearly | Year-wise crime counts |
| summary_crime_by_category | Category-wise crime counts and percentages |
| summary_arrests_yearly | Year-wise arrest statistics |

### SQL Views

| View | Purpose |
|---|---|
| vw_crime_yearly | Year-wise crime reporting |
| vw_crime_by_category | Category-wise crime counts and percentages |

### Database Relationships

| Crime Records Column | Reference Table | Reference Column |
|---|---|---|
| iucr_code | iucr_codes | iucr |
| district_code | police_districts | district_code |
| ward_no | ward_offices | ward |
| community_code | community_areas | community_code |
| beat_num | police_beats | beat_num |

Related records are connected through corresponding reference columns. Data integrity is supported through primary keys, relationship validation, SQL joins and applicable database constraints.

## 9. Flask Web Application

The Flask application consists of two main modules: Crime Analytics Dashboard and Police District Management. The user interface is developed using HTML and external CSS without JavaScript.

Separate stylesheets are maintained for the dashboard and district management pages.

| HTML Template | Stylesheet |
|---|---|
| templates/dashboard.html | static/css/dashboard.css |
| templates/districts.html | static/css/districts.css |

### 9.1 Crime Analytics Dashboard

The dashboard presents four Key Performance Indicators (KPIs):

- Total crime records.
- Overall arrest rate.
- Number of crime categories.
- Most frequently reported crime category.

The dashboard includes nine analytical visualizations.

| Visualization | Key Insight |
|---|---|
| Yearly Crime Trend | The highest recorded crime count is in 2016, with 490 incidents. |
| Top 10 Crime Categories | THEFT is the most frequent category, accounting for 105 cases (21.08%). |
| Monthly and Weekday Crime Distribution | Recorded crime frequencies vary across months and weekdays. |
| Top 10 Community Areas | Austin has the highest recorded crime count, with 34 incidents. |
| Hourly Crime Distribution | Midnight values result from date-only timestamps rather than actual occurrence times. |
| Community Crime Distribution | The box plot identifies communities with unusually high recorded crime counts. |
| Crime Correlation Heatmap | The heatmap illustrates statistical relationships between selected numerical variables. |
| SQL Yearly Crime Report | SQL analysis confirms that 490 of the 498 records belong to 2016. |
| SQL Crime Category Report | SQL analysis confirms THEFT as the leading crime category. |

Each visualization includes an analytical observation to help users understand the results.

### 9.2 Police District Management

The Police District Management module provides an interface for managing records in the `police_districts` table.

| Operation | Description |
|---|---|
| GET | Retrieves complete details of a specific district using its unique identifier. |
| POST | Creates a new police district record. |
| PUT | Updates all editable fields of an existing district using its unique identifier. |
| PATCH | Updates selected fields without modifying the remaining fields. |
| DELETE | Removes a specific district using its unique identifier, subject to referential integrity constraints. |
| Search | Retrieves records matching the specified search criteria. |
| Clear | Resets the input or search filters and returns to the main district page. |

The GET operation allows users to manually enter a district code and retrieve all 15 district fields. District details can also be accessed directly from the existing records table.

Search functionality supports filtering by district code, district name, address, city or ZIP code.

The six editable fields are:

- District Name
- Address
- City
- State
- ZIP Code
- Phone Number

The district code is assigned during record creation and remains protected during updates. The remaining original district fields are preserved.

### 9.3 Application Routes and REST API Endpoints

| HTTP Method | Endpoint | Operation |
|---|---|---|
| GET | `/` | Display the analytics dashboard |
| GET | `/districts` | Display all police districts |
| GET | `/districts?search=keyword` | Search district records |
| GET | `/districts/get?district_code=1` | Retrieve a district using a manually entered code |
| GET | `/districts/<district_code>` | Display complete district details |
| POST | `/districts` | Create a new district |
| GET | `/districts/<district_code>/edit` | Display the full update form |
| POST | `/districts/<district_code>/edit` | Process the browser full update |
| GET | `/districts/<district_code>/patch` | Display the partial update form |
| POST | `/districts/<district_code>/patch` | Process the browser partial update |
| GET | `/districts/<district_code>/delete` | Display the deletion confirmation |
| POST | `/districts/<district_code>/delete` | Process the browser deletion |
| GET | `/api/districts/<district_code>` | Retrieve district details in JSON format |
| PUT | `/api/districts/<district_code>` | Update all editable fields |
| PATCH | `/api/districts/<district_code>` | Update selected fields |
| DELETE | `/api/districts/<district_code>` | Delete an unreferenced district |

Browser-based operations use native HTML GET and POST requests. Dedicated REST API endpoints support actual PUT, PATCH and DELETE requests without requiring JavaScript.

### 9.4 Validation and Database Integrity

- Required field validation.
- Positive integer district code validation.
- Duplicate district code prevention.
- Parameterized SQL queries to prevent SQL injection.
- Restricted editable fields.
- Protection of unique district identifiers during updates.
- SQLite foreign key enforcement enabled for CRUD connections.
- Reference validation before district deletion.
- Protection against deletion of districts linked to existing crime records.
- Operation success and error messages.

## 10. Key Analytical Findings

| Metric | Result |
|---|---|
| Original crime records | 498 |
| Original dataset columns | 20 |
| Cleaned crime records | 498 |
| Records discarded during cleaning | 0 |
| Feature-engineered dataset columns | 22 |
| Recorded arrests | 124 |
| Overall arrest rate | 24.90% |
| Unique crime categories | 23 |
| Most frequent crime category | THEFT |
| Total theft records | 105 |
| Theft percentage | 21.08% |
| Year with highest recorded crime count | 2016 |
| Highest yearly crime count | 490 |
| Community area with highest crime count | Austin |
| Crime records in Austin | 34 |
| Community areas identified as IQR outliers | 3 |

The findings represent the supplied dataset rather than complete Chicago citywide crime statistics.

## 11. Installation and Execution

### Step 1: Open the Project

Open the `Chicago_Crime_Capstone_2026` folder in Visual Studio Code.

Ensure Python and the VS Code Python and Jupyter extensions are installed.

### Step 2: Install Dependencies

Open the terminal in the project root directory and execute:

```bash
python -m pip install -r requirements.txt
```

### Step 3: Execute the Analytical Notebooks

To reproduce the analytical outputs, execute the notebooks in the following order:

1. `01_UC1_load_and_clean.ipynb`
2. `02_UC2_exploratory_analysis.ipynb`
3. `03_UC3_statistical_analysis.ipynb`
4. `04_UC4_database_reporting.ipynb`

The notebooks generate the processed datasets, SQLite database, analytical reports and visualization charts.

If these outputs are already available, the Flask application can be started directly. Back up the database before rerunning notebooks that recreate or populate database tables.

### Step 4: Validate Project Configuration

```bash
python config.py
```

Expected output:

```
Database: Available
Charts folder: Available
Flask configuration: Ready
```

### Step 5: Verify Flask Routes

```bash
python -m flask --app app routes
```

This command displays the registered application routes and their supported HTTP methods.

### Step 6: Start the Flask Application

```bash
python app.py
```

### Step 7: Access the Application

Crime Analytics Dashboard:

http://127.0.0.1:5000/

Police District Management:

http://127.0.0.1:5000/districts

To stop the application, press `Ctrl + C` in the terminal.

## 12. Data Limitations

- The analysis is limited to the 498 supplied crime records and does not represent complete Chicago crime statistics.
- Uneven yearly data coverage limits reliable comparisons of long-term crime trends.
- The source dates do not contain meaningful time-of-day information.
- Midnight values introduced during datetime conversion do not represent actual crime occurrence times.
- Community-level crime counts are not adjusted for population differences.
- Correlation results describe statistical relationships and do not establish causation.
- Dashboard charts are generated through analytical notebooks rather than live crime data.
- Police district CRUD operations do not automatically regenerate analytical charts.

## 13. Conclusion

The Chicago Crime Data Analytics and Reporting System brings together data preprocessing, exploratory analysis, statistical analysis, SQL reporting and web application development in a single project.

The analytical notebooks transform the supplied crime data into structured reports and visualizations while preserving valid records. The Flask dashboard presents the key findings, and the Police District Management module supports record retrieval, creation, full updates, partial updates, deletion and search.

The project demonstrates how Python, SQLite and Flask can be used together to develop a practical data analytics and reporting application while maintaining data integrity and acknowledging the limitations of the supplied dataset.

---

**Project:** Chicago Crime Data Analytics and Reporting System

**Project Type:** Python Full-Stack Capstone

