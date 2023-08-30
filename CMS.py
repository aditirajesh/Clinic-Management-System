

import pandas as pd 
from datetime import datetime 
from datetime import date 
from typing import Iterator,Iterable 

class Med_Data(): #parent class 
    ''''Managing the main table'''


    def __init__(self,path):
        '''Constructor'''
        self.df = pd.read_csv(path).dropna()             #the dataframe 
        self.data = self.df.values.tolist()              #obtaining all the rows in the form of a list to do list based operations 
        self.size = len(self.data)
        self.columns = ["ID","Name","Type","DOE","Total","Used","Stock","Cost"]   #columns in the table 
        self.path = path  #storing the path of the csv file to make it easily accessible through other methods 


    def __len__(self):
        return self.size 
    
    def __save__(self,path):
        '''Saving the csv file'''
        self.df.to_csv(path,encoding = 'utf-8',index = False)     
    
    def __str__(self):
        '''Printing the table'''
        return self.df

    def __read__(self):
        '''Reading the csv file. this is mainly done so that the table changes gets constantly updated in the dataframe'''
        read_df = pd.read_csv(self.path).dropna()
        self.df = read_df 

    def __write__(self):
        '''Writing into the csv file'''
        new_df = pd.DataFrame(self.data,columns=self.columns)
        new_df.to_csv(self.path,index=False)

    def add(self,id,name,type,doe,used,stock,cost):
        '''Adding to the csv file'''
        for i in self.data:
            if id in i or name in i:
                if id in i:
                    return "ID present"

                else:
                    return "name present"

           
        row = [id,name,type,doe,used+stock,used,stock,cost]
        self.data.append(row)
        self.__write__()
        self.__read__()
        return "Addition complete"

    def table_list(self):
        return self.data

    def order(self,column):
        '''Ordering the table according to the column specified'''
        if column in self.columns:
            index = self.columns.index(column)    #this index value in the nested list is what is supposed to be changed 
            self.data.sort(key = lambda x: x[index]) 
            self.__write__()
            self.__read__()
            return self.__str__()

        else:
            return "Column does not exist"

    def update(self,med_id,column,new_value):
        '''Updating a particular value in the csv file based on ID'''
        count = 0   #kept to raise error if invalid id is entered 
        if column in ["ID","Name","Type","DOE","Used","Stock","Cost"]:
            index = self.columns.index(column)

            for i in self.data:
                if med_id in i and i[0] == med_id:
                    i[index] = new_value 

                    if column == "Used":
                        if new_value > i[4]:
                            return "Used Invalid"

                        else:
                            i[6] = i[4] - new_value 

                    elif column == "Stock":
                        if new_value > i[4]:
                            return "Stock Invalid"
                        else:
                            i[5] = i[4] - new_value  #amount used gets updated 

                    count += 1 
                    self.__write__()
                    self.__read__()
        
            if count == 1:
                return "Updation complete"
            else:
                return "Invalid ID"

        else:
            return "Column does not exist"

    def update_multi(self,med_id,total,used):
        '''Updating a particular value's total, used and stock amount'''
        counter = 0 
        for i in self.data:
            if med_id in i and i[0] == med_id:
                counter += 1 
                if used > total:
                    return "Used Invalid"

                else:
                    i[4] = total 
                    i[5] = used 
                    i[6] = total - used 
                    self.__write__()
                    self.__read__()

        if counter == 1:
            return "Updation complete"

        else:
            return "Invalid ID"

        
    def delete(self,med_id):
        '''Deleting a field based on Medicine ID'''
        count = 0 
        for i in self.data:
            if med_id in i and i.index(med_id) == 0:
                self.data.remove(i)
                self.__write__()
                self.__read__()
                count += 1 

        if count == 1:
            return "Deleted successfully"
        else:
            return "Invalid ID"

    def retrieve(self,row_num):
        '''Retrieving the row details based on the row_num specified'''
        if row_num < self.size:
            return self.data[row_num]

        else:
            return "Invalid row number"

    def low_stock(self):
        '''Prints rows that have dangerously low stock left'''
        low_stock_table = []
        index = self.columns.index("Stock")
        for i in self.data:
            if i[index] < 10:   #stock is lesser than 10, warning 
                low_stock_table.append(i)

        low_stock_df = pd.DataFrame(low_stock_table,columns=self.columns)
        return low_stock_df,low_stock_table

    def empty_stock(self):
        '''Prints rows that have no stock left'''
        no_stock = []
        index = self.columns.index("Stock")
        for i in self.data:
            if i[index] == 0:
                no_stock.append(i)

        no_stock_df = pd.DataFrame(no_stock,columns=self.columns)
        return no_stock_df,no_stock

    def reach_expiry(self):
        '''Prints the rows that are close to expiration date'''
        reach_expired = []
        index = self.columns.index("DOE")
        for i in self.data:
            sdate = i[index]
            ddate = datetime.strptime(sdate, "%d/%m/%Y").date()  #yyyy-mm-dd
            today = date.today() #2022-08-18
            if (ddate - today).days < 30:   #30 days before expiration date
                reach_expired.append(i)

        reach_expired_df = pd.DataFrame(reach_expired,columns=self.columns)
        return reach_expired_df,reach_expired 

    def expired(self):
        '''Prints information of all medicines that are expired'''
        expired = []
        index = self.columns.index("DOE")
        for i in self.data:
            sdate = i[index] 
            ddate = datetime.strptime(sdate,"%d/%m/%Y").date()
            today = date.today()

            if today >= ddate:   #medicine is expired 
                expired.append(i)

        expired_df = pd.DataFrame(expired,columns=self.columns)
        return expired_df,expired
        
    def clear(self):
        '''Clearing the entire table - csv file'''
        self.table.clear()

