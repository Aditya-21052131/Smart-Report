from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from jinja2 import Template

# Create engine and session
engine = create_engine('sqlite:///health_reports.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Define base model
Base = declarative_base()

# Define models for lab reports and health test packages
class LabReport(Base):
    __tablename__ = 'lab_reports'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    test_name = Column(String)
    result = Column(Float)

class HealthTestPackage(Base):
    __tablename__ = 'health_test_packages'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    package_name = Column(String)
    # Add more columns as needed

# Create tables
Base.metadata.create_all(engine)

# Sample data
lab_data = [
    {'patient_id': 1, 'test_name': 'CBC', 'result': 12.5},
    {'patient_id': 2, 'test_name': 'Lipid Profile', 'result': 150},
    # Add more sample data as needed
]

# Ingest data into database
for data in lab_data:
    lab_report = LabReport(**data)
    session.add(lab_report)
session.commit()

# Process data
def process_lab_data():
    data = session.query(LabReport).all()
    processed_data = {report.test_name: report.result for report in data}
    return processed_data

# Generate visualization
def generate_bar_chart(data):
    plt.bar(data.keys(), data.values())
    plt.xlabel('Test Name')
    plt.ylabel('Result')
    plt.title('Lab Test Results')
    plt.show()

# Generate report template
def generate_report_template(patient_name, data):
    template = Template("""
    <html>
    <head><title>{{ patient_name }}'s Lab Report</title></head>
    <body>
    <h1>{{ patient_name }}'s Lab Report</h1>
    <p>Report Data:</p>
    <ul>
    {% for key, value in data.items() %}
    <li>{{ key }}: {{ value }}</li>
    {% endfor %}
    </ul>
    </body>
    </html>
    """)
    return template.render(patient_name=patient_name, data=data)

# Example usage
processed_data = process_lab_data()
generate_bar_chart(processed_data)
report_template = generate_report_template("John Doe", processed_data)
print(report_template)
