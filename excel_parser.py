import os
import xlrd
from datetime import datetime
from pprint import pprint
import unittest
import json


# 1. EXCEL PARSING - TEST#1

class MyExcelParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.labels = ["Quote Number", "Ship To", "Date", "Name",
                       "LineNumber", "PartNumber", "Description", "Item Type", "Price"]

    def load_file(self):
        self.wb = xlrd.open_workbook(self.file_path)
        self.sheet = self.wb.sheet_by_index(0)
        self.nrows = self.sheet.nrows
        self.ncols = self.sheet.ncols
        self.__parse_data()

    def __parse_data(self):
        result = {}
        for row in range(self.nrows):
            for col in range(self.ncols):
                val = self.sheet.cell_value(row, col)
                # look ahead for the adjacent column number
                next_col = col+1 if col < self.ncols-1 else col
                # find the value in th adjacent not blank column
                next_val = self.sheet.cell_value(row, next_col)

                if val:  # to check for blank rows

                    # to handle Quote Number, Ship to, Date
                    if val in self.labels[0:2] and next_val not in self.labels:
                        result[val] = next_val if next_val != '' else 'Data Not Present'

                    # to handle date and convert to the format as requested
                    elif val == self.labels[2] and next_val not in self.labels:
                        # self.wb.datemode default workbook mode is 0 i.e. mm/dd/yyyy
                        next_val_dt = datetime(
                            *xlrd.xldate_as_tuple(next_val, self.wb.datemode)).strftime("%Y-%m-%d")
                        result[val] = next_val_dt if next_val_dt != '' else 'Data Not Present'

                    # to handle name field
                    elif type(val) == str and val.startswith(self.labels[3]):
                        result[self.labels[3]] = val.split(':')[-1]

                    # to get the item fields
                    elif val == self.labels[4]:
                        result['Items'] = [
                            item for item in self.__parse_item_data(row, col) if item]

        self.__build_output(result)

    '''
        method to parse the items row by row as per the input excel
    '''

    def __parse_item_data(self, rnum, cnum):
        items = []
        item_labels = []  # to create the label array based on the header column names
        for row in range(rnum, self.nrows):
            tmp_item = {}
            for col in range(self.ncols):
                val = self.sheet.cell_value(row, col)
                if col < cnum:  # running the loop for the columns prioir to item header
                    if val and str(val).startswith('-'*10):
                        return items  # exit when atleast 10 dashes are encountered
                    continue  # skipping the part below to run for the column before where LineNumber starts
                if val:
                    # to check if the current row contains the header cols
                    if val in self.labels:
                        item_labels.append(val)
                    else:
                        # add to dictionary the corresponding value based on the position
                        tmp_item[item_labels[col-cnum]] = val
            items.append(tmp_item)
        return items

    def __build_output(self, out_data):
        response = {}
        print_labels = ['Quote Number', 'Date', 'Items',
                        'LineNumber', 'PartNumber', 'Description', 'Price']
        for key, value in out_data.items():
            if key in print_labels:
                if key == 'Quote Number':  # modify the key value as per the sample ooutput
                    response['Quote'] = value
                else:
                    if type(value) == list:  # loop through the items if found
                        response.setdefault('Items', [])
                        for v1 in value:
                            tmp_item = {}
                            for key1, value1 in v1.items():
                                if key1 in print_labels:
                                    tmp_item[key1] = value1
                            response['Items'].append(tmp_item)
                    else:
                        response[key] = value

        self.__print_debug_data(response, 'output json', format='json')
        return response

    def __print_debug_data(self, data, message=None, format=None):
        print('-'*100)
        print(message)
        if format and format == 'json':
            # pretty printing the dictionary to screen
            print(json.dumps(data, indent=3))
        else:
            if type(data) == dict:
                for d in data:
                    if type(data[d]) == list:
                        for l in data[d]:
                            self.__print_debug_data(l, str(d))
                    else:
                        print(d, ':', data[d])
            else:
                print(data)
        print('\n')


class TestExcelParser(unittest.TestCase):

    def test_parsed_data(self):
        path = os.path.join(os.getcwd(), 'ToParse_Python .xlsx')
        parser = MyExcelParser(path)
        self.assertTrue(parser.load_file,
                        "Expected true ")


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'ToParse_Python .xlsx')
    parser = MyExcelParser(path)
    parser.load_file()
    # unittest.main()
