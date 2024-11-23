<h1>Building an Efficient ETL Pipeline for Property Records in Real Estate</h1>

  <h2>Project Description</h2>
    <p>
        This project focuses on building a robust ETL (Extract, Transform, Load) pipeline to handle property records data 
        for real estate analysis. The pipeline ingests data from an external API, performs transformations to clean and 
        structure the data, and loads it into a PostgreSQL database. Additionally, the project automates query execution 
        and result generation using SQL scripts, saving results in various formats. The workflow is scheduled using 
        Windows Task Scheduler, ensuring periodic updates and seamless integration into real estate analytics workflows.
    </p>
    <p>
        The repository provides all the necessary components, including the ETL script, query execution logic, and task 
        scheduling setup.
    </p>

  <h2>Key Features</h2>
    <ul>
        <li>
            <strong>Data Ingestion:</strong>
            <ul>
                <li>Data is fetched from the <em>Realty Mole Property API</em>.</li>
                <li>Up to 10,000 property records are ingested in JSON format using secure HTTP requests.</li>
            </ul>
        </li>
        <li>
            <strong>Data Transformation:</strong>
            <ul>
                <li>Cleaning and standardizing data (e.g., handling missing values, type conversions).</li>
                <li>
                    Extracting features and creating normalized data tables:
                    <ul>
                        <li>Fact Table: Captures key property attributes.</li>
                        <li>Dimension Tables: Stores data about location, sales, and property features.</li>
                    </ul>
                </li>
                <li>Conversion of nested JSON fields into manageable formats.</li>
            </ul>
        </li>
        <li>
            <strong>Data Loading:</strong>
            <ul>
                <li>Data is loaded into a <em>PostgreSQL</em> database with a custom schema (<code>zipco</code>).</li>
                <li>Uses <code>SQLAlchemy</code> to define data types and manage database interactions.</li>
            </ul>
        </li>
        <li>
            <strong>Query Execution:</strong>
            <ul>
                <li>Executes predefined SQL queries (<code>analysis.sql</code>) to generate insights:</li>
                <ul>
                    <li>Average sale price of properties.</li>
                    <li>Property count by state.</li>
                </ul>
                <li>Results are saved in JSON format for further analysis or visualization.</li>
            </ul>
        </li>
        <li>
            <strong>Automation with Windows Task Scheduler:</strong>
            <ul>
                <li>The ETL process is automated with a task that runs hourly.</li>
                <li>Scheduling details are provided in an XML configuration file (<code>etl_script.xml</code>).</li>
            </ul>
        </li>
        <li>
            <strong>Documentation and Modularity:</strong>
            <ul>
                <li>Clear modular structure for the ETL pipeline.</li>
                <li>Comprehensive handling of edge cases during data transformation and database loading.</li>
            </ul>
        </li>
    </ul>

   <h2>Files in the Repository</h2>
    <ul>
        <li>
            <strong><code>postgres_pipeline.py</code>:</strong>
            <p>
                The main Python script that implements the ETL process:
            </p>
            <ul>
                <li>Fetches data from the API.</li>
                <li>Transforms and cleans data.</li>
                <li>Loads data into the PostgreSQL database.</li>
                <li>Executes SQL queries and saves results.</li>
            </ul>
        </li>
        <li>
            <strong><code>analysis.sql</code>:</strong>
            <p>
                Contains SQL queries for analytical tasks:
            </p>
            <ul>
                <li>Calculate the average sale price of properties.</li>
                <li>Count the number of properties grouped by state.</li>
            </ul>
        </li>
        <li>
            <strong><code>etl_script.xml</code>:</strong>
            <p>
                Windows Task Scheduler configuration file to automate the ETL process:
            </p>
            <ul>
                <li>Runs the pipeline every hour.</li>
                <li>Logs task execution details.</li>
            </ul>
        </li>
        <li>
            <strong>Output Files:</strong>
            <ul>
                <li><em>CSV Files:</em> Intermediate tables saved as <code>fct_table.csv</code>, <code>dim_location.csv</code>, <code>dim_feature.csv</code>, and <code>dim_sales.csv</code>.</li>
                <li><em>JSON Files:</em> Query results saved as <code>average_price.json</code> and <code>state_counts.json</code>.</li>
            </ul>
        </li>
    </ul>

  <h2>Project Objectives</h2>
    <p>
        This project aims to provide hands-on experience in building and automating ETL pipelines. By working on this project, contributors will:
    </p>
    <ol>
        <li><strong>Gain Expertise in ETL Development:</strong> Learn how to design efficient workflows for ingesting, transforming, and loading large datasets.</li>
        <li><strong>Master PostgreSQL Database Management:</strong> Create and manage schemas, tables, and data types. Optimize SQL queries for real-time insights.</li>
        <li><strong>Develop Data Cleaning and Transformation Skills:</strong> Handle incomplete, inconsistent, or nested data structures. Apply pandas for data preprocessing.</li>
        <li><strong>Learn Workflow Automation:</strong> Use Windows Task Scheduler for periodic execution of ETL pipelines. Understand automation in production environments.</li>
        <li><strong>Enhance Problem-Solving and Analytical Skills:</strong> Derive actionable insights from real-world property data. Implement and document solutions to complex data challenges.</li>
        <li><strong>Build a Foundation for Data Engineering Roles:</strong> End-to-end ownership of a data engineering project. Develop skills in Python, SQL, database management, and automation.</li>
    </ol>

  <h2>How to Use the Repository</h2>
    <ol>
        <li><strong>Setup:</strong>
            <ul>
                <li>Install dependencies listed in <code>requirements.txt</code> (e.g., pandas, SQLAlchemy, psycopg2).</li>
                <li>Configure the PostgreSQL database with a user having write permissions.</li>
                <li>Place the API credentials (<code>x-rapidapi-key</code>) in <code>postgres_pipeline.py</code>.</li>
            </ul>
        </li>
        <li><strong>Run the Pipeline:</strong> Execute <code>postgres_pipeline.py</code> manually or use the provided Windows Task Scheduler configuration.</li>
        <li><strong>Analyze the Data:</strong> Modify and execute queries in <code>analysis.sql</code> for custom insights. Check output files (<code>average_price.json</code>, <code>state_counts.json</code>) for results.</li>
        <li><strong>Automate the Workflow:</strong> Import <code>etl_script.xml</code> into Windows Task Scheduler. Verify the task schedule and ensure proper execution.</li>
    </ol>
