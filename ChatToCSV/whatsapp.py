import os
import numpy as np
import pandas as pd
import regex as re


class WhatsAppChatToCSV:

    def __init__(self, input_filename, output_filename="output", path=os.getcwd(), return_df = False):
        """
        input:
            input_filename  : Whatsapp exported chat
            output_filename : name for csv file to be saved
            path            : Path in which the files are located
        """

        self.input_filename = input_filename
        self.output_filename = output_filename
        self.path = path
        self.return_df = return_df
        self.messages = []
        self.users = []
        self.dates = []
        self.times = []

    def addPointerToEachLine(self):

        """
        Puts a pointer after each date to seperate each message
        """
        dates = re.findall(
            r"[0-9]{1,4}[\_|\-|\/|\|][0-9]{1,2}[\_|\-|\/|\|][0-9]{1,4}[,]", self.data)
        for i in set(dates):
            self.data = self.data.replace(i, '<*+*>'+i)
        self.data = self.data.split('<*+*>')

        return None

    def seperatelyExtractContent(self):

        """
        Extracts user, message, date and time
        """

        messages = []
        dates = []
        times = []
        users = []
        for i in range(len(self.data)):
            if len(self.data[i]) != 0 and self.data[i]:
                dates.append(
                    self.data[i][:self.data[i].find('-')-1].split(',')[0])
                times.append(
                    self.data[i][:self.data[i].find('-')-1].split(',')[1])
                temp = self.data[i][self.data[i].find('-')+1:]
                users.append(temp[:temp.find(':')])
                messages.append(temp[temp.find(':')+1:])

        self.messages = messages
        self.users = users
        self.dates = dates
        self.times = times

        return None

    def removeUnwantedRows(self):

        """
        Removes rows with media omitted or deleted messages
        """

        rows_to_remove = []
        for i in range(len(self.dataframe)):
            if self.dataframe.values[i][2].strip('\n') == self.dataframe.values[i][3].strip('\n') or '<Media omitted>' in self.dataframe.values[i][3] or 'This message was deleted' in self.dataframe.values[i][3]:
                rows_to_remove.append(i)
        self.dataframe = self.dataframe.drop(
            rows_to_remove, axis=0).reset_index(drop=True)

        return None

    def buildCSV(self):

        """
        Builds the final csv
        """

        with open(self.path+'/'+self.input_filename) as file:
            self.data = file.read()

        self.addPointerToEachLine()
        self.seperatelyExtractContent()
        finalOutput = {'Date': self.dates, 'Time': self.times,
                       'User': self.users, 'Message': self.messages}
        self.dataframe = pd.DataFrame(finalOutput)
        self.removeUnwantedRows()
        self.dataframe.to_csv(self.output_filename+".csv",index=False)

        if self.return_df:
            return self.dataframe
