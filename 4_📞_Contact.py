from os import uname_result
import streamlit as st
import pandas as pd
from importlib.machinery import SourceFileLoader
import smtplib
CMS = SourceFileLoader("CMS","/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/CMS.py").load_module()
df_medicine = CMS.Med_Data("/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/med.csv")
df_bandages = CMS.Med_Data("/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/bandages.csv")



class Clients:

    def __init__(self,name,email):
        self.name = name 
        self.email = email 

    def receive(self,mes):
        smtp_session = smtplib.SMTP('smtp.gmail.com', 587) #enabling the smtp session 
        smtp_session.starttls()  #start tls for security 
        smtp_session.login('customerhelp.ssncms@gmail.com','aditipass2004*')
        message = mes 
        smtp_session('customerhelp.ssncms@gmail.com',self.email,message)
        smtp_session.quit()
        

class Developer:
    '''singleton pattern is also implemented here to ensure only one developer object is present '''
    s_instance = None 

    def __init__(self):
        self.subscribers = []

    def __new__(cls):
        if cls.s_instance is None:
            cls.s_instance = super(Developer,cls).__new__(cls)

        return cls.s_instance 

    def register(self, obj):
        if type(self) == Clients:
            self.subscribers.append(obj)

    def unregister(self,obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def dispatch(self):
        '''medicines low on stock '''
        low_medicine = List_Iterable(df_medicine.low_stock()[1])
        low_bandages = List_Iterable(df_bandages.low_stock()[1])
        
        '''medicines out of stock'''
        no_medicine = List_Iterable(df_medicine.empty_stock()[1])
        no_bandages = List_Iterable(df_bandages.empty_stock()[1])
        
        '''medicines expired'''
        expired_medicine = List_Iterable(df_medicine.expired()[1])
        expired_bandages = List_Iterable(df_medicine.expired()[1])
        
        '''medicines close to expiry'''
        expiry_medicine = List_Iterable(df_medicine.reach_expiry()[1])
        expiry_bandages = List_Iterable(df_bandages.reach_expiry()[1])

        for subscriber in self.subscribers:

            for med in low_medicine:
                message = '{} is low in stock'.format(med)
                subscriber.receive(message)

            for band in low_bandages:
                message = '{} medical equipment is low in stock'.format(band)
                subscriber.receive(message)

            for med in no_medicine:
                message = '{} is out of stock'.format(med)
                subscriber.receive(message)

            for band in low_bandages:
                message = '{} medical equipment is out of stock'.format(band)
                subscriber.receive(message)

            for med in expired_medicine:
                message = '{} is expired'.format(band)
                subscriber.receive(message)

            for band in expired_bandages:
                message = '{} medical equipment is expired'.format(band)
                subscriber.receive(message)

            for med in expiry_medicine:
                message = '{} is close to expiry'.format(med)
                subscriber.receive(message)

            for band in expiry_bandages:
                message = '{} medical equipment is close to expiry'.format(band)
                subscriber.receive(message)





class List_Iterable:
    def __init__(self,l):
        self.iterable_list = l 


    def __iter__(self):
        return List_Iterator(self.iterable_list)

class List_Iterator:

    def __init__(self,l):
        self.iterator_list = l 
        self.index = 0 

    def __next__(self):
        if self.index < len(self.iterator_list):
            name = self.iterator_list[self.index][1]
            self.index += 1
            return name 

        else:
            raise StopIteration





def page_designs():
    st.markdown(
        r"""
        # Contact :phone:"""
    )
    st.markdown("---")

page_designs()





def mail_contact():
    st.caption("        ")
    st.caption("If you have any queries, submit them below")

    st.subheader("Contact through mail :mailbox:")
    contact_form = '''
    <form action="https://formsubmit.co/customerhelp.ssncms@gmail.com" method="POST">
        <input type="text" name="name" placeholder = "Your name" required>
        <textarea name="message" placeholder="What issue are you facing?"></textarea>
        <button type="submit">Send</button>
        <input type="hidden" name="_captcha" value="false">
    </form>
    '''

    st.markdown(contact_form,unsafe_allow_html = True)


mail_contact()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/style/style.css")

def receive_notifications():
    st.caption("  \n\n\n\n\n\n")
    st.subheader("Receive notifications! :stopwatch:")
    st.caption("If you want to receive notifications about expired and out of stock medicines, fill in the information below:")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input('Enter your name ')

    with col2:
        email = st.text_input('Enter email id')

    customer = Clients(name,email)
    developer = Developer()
    developer.register(customer)
    developer.dispatch() #sending notifications the minute the person is subscribed 

receive_notifications()

def phone_contact():
    st.caption("  \n\n\n\n\n\n")
    st.subheader("Contact through phone :phone:")
    col1,col2 = st.columns(2)
    with col1:
        st.write("Contact number  1: 7010821856")
        st.write("Contact number  2: 9092093093")

    with col2:
        st.write("Name: Aditi Rajesh")
        st.write("Name: Arjun Bharath")

    st.caption("Thank you for using SSN CMS!")

phone_contact()

