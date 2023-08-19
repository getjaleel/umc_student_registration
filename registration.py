import streamlit as st
import random
from datetime import datetime
import boto3

first_name = st.text_input("Enter First Name")
last_name = st.text_input("Enter Last Name")

phone = st.text_input("Enter Phone Number")
email = st.text_input("Enter Email Address")
payment_date = st.date_input("Payment Date")
sex = st.radio("Select Sex", options=["M", "F"])
payment_status = st.radio("Select Status",("Amount Paid","Exception"))
teachers_name = st.selectbox("Assign a teacher to student",('Inam Qatawi',' Safaa Albardawil'))
if payment_status == 'Amount Paid':
    amount_paid=st.text_input("Enter the amount")
else:
    st.write("Exception selected")

def generate_student_id(first_name, last_name, sex, phone, email, payment_date):
    first_initial = first_name[0].upper()
    last_initial = last_name[0].upper()
    current_year = datetime.now().year % 100
    random_num = random.randint(100, 999)
    student_id = f"{first_initial}{last_initial}{sex}{random_num}{current_year}"
    
    payment_datetime_str = f"{payment_date}"
    payment_datetime = datetime.strptime(payment_datetime_str, "%Y-%m-%d")
    epoch_time = int(payment_datetime.timestamp())
    
    
    return student_id, epoch_time

#payment_time = st.time_input("Payment Time")


name = (first_name + last_name)
course = st.selectbox("Select Course",('Juzz Amma','"Arabic Language (Arab kids) March 2023"','"Quran Group (Girls)"'))    
if payment_status == 'Amount Paid' and st.button("Register Student"):
    dynamodb = boto3.client('dynamodb', region_name='ap-southeast-2')
    # Define the DynamoDB table name
    
    student_id, epoch_time = generate_student_id(first_name,last_name,sex, phone, email, payment_date)
    st.write(f"Generated Student ID: {student_id}")
    st.write(f"Epoch Time: {epoch_time}")

    table_name = 'Student_Information'
    # Create a new item (row) for the student
    
    item = {
        'Student ID': {'S': student_id},
        'Name': {'S': name},
        'Sex': {'S': sex},
        'Course': {'S': course},
        'Amount paid':{'S':amount_paid},
        'Teachers Name':{'S':teachers_name}
    }
    # Put the item into the DynamoDB table
    dynamodb.put_item(TableName=table_name, Item=item)
    st.success('Student registered successfully!')
    st.write(f'Student ID: {student_id}')

elif payment_status == 'Exception' and st.button("Update"):
    dynamodb = boto3.client('dynamodb', region_name='ap-southeast-2')
    # Define the DynamoDB table name
    
    student_id, epoch_time = generate_student_id(first_name,last_name,sex, phone, email, payment_date)
    st.write(f"Generated Student ID: {student_id}")
    st.write(f"Epoch Time: {epoch_time}")

    table_name = 'Student_Information'
    # Create a new item (row) for the student
    
    item = {
        'Student ID': {'S': student_id},
        'Name': {'S': name},
        'Sex': {'S': sex},
        'Course': {'S': course},
        'Amount paid':{'S':'Excempted'},
        'Teachers Name':{'S':teachers_name}
    }
    # Put the item into the DynamoDB table
    dynamodb.put_item(TableName=table_name, Item=item)
    st.success('Student registered successfully!')
    st.write(f'Please note down the Student ID for reference: {student_id}')



# st.write("# Student ID Generator")