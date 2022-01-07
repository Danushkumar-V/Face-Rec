import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""ATTEDENCE MONITORING SYSTEM"""

	st.title("ATTENDANCE MONITORING SYSTEM ")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		st.header("INTRODUCTION:")
		st.write("Taking attendance during lectures will reduce the time of lecture hour.To avoid these losses, we are about to use automatic process which is based on image processing.In this novel approach, we are using face detection & face recognition system. This face detection differentiates faces from non-faces and is therefore essential for accurate attendance.we have developed a system for video based face detection and recognition for surveillance. ")
		st.header("APPLICATION OF FACIAL RECOGNITION:")	
		st.write("I.Access control")
		st.write("II.Security")
		st.write("III.Surveillance")
		st.write("IV.Time & Attendance")
		

		
	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["ATTENDANCE","STUDENT DATABASE"])
				if task == "ATTENDANCE":
					st.subheader("ATTENDANCE")
					df=pd.read_csv("Attendance_data/csv_2.csv")
					#st.download_button( label="Download data as CSV",data=,file_name='Attendance.csv', mime='text/csv')
					#df.reset_index(inplace = True, drop = True)
					#roll=df.sort_values("Roll_No",axis=0).reset_index()
					#display_count = st.selectbox('Select the Roll Number',roll)
					st.table(df)
					#roll=df.sort_values("Roll_No",axis=0).reset_index(inplace=True)
					#start_time = st.slider("What is the date",value=datetime(2021, 1, 1, 9, 30),format="MM/DD/YY - hh:mm")
					#display_count = st.selectbox('Select the Roll Number',roll)
	 				#st.table(df)

				elif task == "STUDENT DATABASE":
					st.subheader("STUDENT DATABASE")
					sf=pd.read_csv("Frontend/dataofad.csv")
					st.table(sf)
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()