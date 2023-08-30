'''LIST OF MODULES'''
import streamlit as st 
from importlib.machinery import SourceFileLoader
from datetime import date 
from datetime import datetime 
import pandas as pd 

CMS = SourceFileLoader("CMS","/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/CMS.py").load_module()
df_medicine = CMS.Med_Data("/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/med.csv") #table 
df_bandages = CMS.Med_Data("/Users/aditirajesh/Desktop/program_files/python/python_2sem/CMS_project/bandages.csv")

def page_designs():
    st.markdown(
        r"""
        # EDIT  :hammer:
        """
    )
    st.caption("The data can be edited with ease without accessing the main file.")
page_designs()

option1 = st.selectbox("Select Table",["Medicines","Medical Devices"])

if option1 == "Medicines":
    table = df_medicine 

else:
    table = df_bandages 

option = st.radio("Select",("Update","Add","Delete","Search","Sort"))
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)  #making the radio button appear sideways 
st.markdown("---")


def table_operations(option):

    if option == "Add":
        def add():

            col1,col2,col3 = st.columns(3)

            with col1:
                id = st.number_input("ID",step=1)
                name = st.text_input("Name")
                cost = st.number_input("Cost",step=1)

            with col2:
                type = st.text_input("Type")
                doe_date = st.date_input("Date of Expiry")
                doe = doe_date.strftime("%d/%m/%Y") #formatting to add into table 

            with col3:
                stock = st.number_input("Stock (Amount left)",step=1)
                used = st.number_input("Amount Used ",step=1)


            if st.button("Add"):

                if doe_date <= date.today():
                    st.error("Invalid Date")

                elif stock <= 0:
                    st.error("Invalid Stock")

                elif used < 0:
                    st.error("Invalid Amount Used")

                elif cost <= 0:
                    st.error("Invalid Cost")

                elif id <= 0:
                    st.error("Invalid ID")

                else:
                    add_table = table.add(id,name,type,doe,used,stock,cost)
                    if add_table == "ID present":
                        st.error("ID already present in the table")

                    elif add_table == "Name present":
                        st.error("Name already present in the table")

                    else:
                        st.success("Addition complete!")

        add()

    elif option == "Update":
        def update():
            id = st.number_input("Enter ID",step=1)
            column_name = st.selectbox("Enter column name you want to change",["ID","Name","Type","DOE","Total","Used","Stock","Cost"])
            
            if column_name in ["Name","Type"]:
                new_value = st.text_input("Enter new value")

            elif column_name in ["ID","Stock","Cost","Used","Total"]:
                new_value = st.number_input("Enter new value",step=1)
                if column_name == "Total":
                    used_input = st.number_input("Enter amount used:",step=1,min_value=0,max_value=new_value)

            elif column_name == "DOE":
                date_value = st.date_input("Enter new date") 
                new_value = date_value.strftime("%d/%m/%Y")


            if st.button("Update"):
               
                if column_name == "DOE" and date.today() >= date_value:
                    st.error("Product expired. Please re-enter date value.")

               
                elif column_name in ["Stock","Cost","Total","Used"] and new_value < 0:
                        st.error("Enter positive integers only.")
                
            
                else:

                    if column_name == "Total":
                        update_table = table.update_multi(id,new_value,used_input)

                    else:
                        update_table = table.update(id,column_name,new_value)
                        
                if update_table == "Stock Invalid":
                    st.error("Stock cannot be greater than the total amount purchased")

                elif update_table == "Used Invalid":
                    st.error("Used amount cannot be greater than total")

                elif update_table == "Invalid ID":
                    st.error("Invalid ID")

                else:
                    st.success("Updation successful!")

        update()


    elif option == "Delete":
        def delete():
            id = st.number_input("Enter ID to delete",step=1)
            if st.button("Delete"):

                del_table = table.delete(id)

                if del_table == "Deleted successfully":
                    st.success("Deletion successful.")

                else:
                    st.error("Invalid ID")

        delete()
                    

    elif option == "Search":
        def search():
            column_name = st.selectbox("Search by:",["Name","ID"])
            search = []
            counter = 0 
            if column_name == "ID":
                val_input = st.number_input("Enter ID:",step=1)
                index = table.columns.index("ID")
                
            else:
                val_input = st.text_input("Enter Name:")
                index = table.columns.index("Name")
        
            for i in table.data:
                if val_input in i and i.index(val_input) == index:
                    counter += 1 
                    search.append(i)

                else:
                    continue 

            if st.button("Search"):
                if counter == 0:
                    st.error("No product found.")

                else:
                    search_df = pd.DataFrame(search,columns=table.columns)
                    st.table(search_df)

        search()


    elif option == "Sort":
        def sort():
            types = []
            for i in table.data:
                if i[2] in types:
                    continue 
                else:
                    types.append(i[2])

            val_name = st.selectbox("Choose Type",types)
            index = table.columns.index("Type")
            counter = 0 
            sort_l = []
            for i in table.data:
                if val_name in i and i.index(val_name) == index:
                    counter += 1 
                    sort_l.append(i)


                else:
                    continue 

            if st.button("Sort"):
                if counter == 0:
                    st.error("No such type exists.")

                else:
                    sort_df = pd.DataFrame(sort_l,columns=table.columns)
                    st.table(sort_df)

        sort()

table_operations(option)

def sidebar_operations():
    with st.sidebar:
        st.title("Restock")
        option = st.selectbox("Select Table:",["Medicines","Medical Equipment"])
        if option == "Medicines":
            table = df_medicine

        else:
            table = df_bandages

        name = st.text_input("Name of Product")
        total = st.number_input("Enter Restock amount",step=1)
        counter = 0 
        row = None 

        for i in table.data:
            if i[1] == name:
                counter += 1 
                row = i 

            else:
                continue

        if st.button("Restock"): 

            if counter == 1:
                table.update_multi(row[0],total,0)
                st.success("Restock successful")

            else:
                if name == "":
                    pass 
                else:
                    st.error("Medicine not found in Inventory")

sidebar_operations()




        
            






            

    

