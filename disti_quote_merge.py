import os
import unittest


class QuoteMerge:
    def __init__(self, bom, disti):
        self.bom_list = bom
        self.disti_list = disti
        self.bom_disti_lbl_keys = {"bom_pn": "BoM PN", "bom_qty": "BoM Qty",
                                   "dsti_pn": "Disti PN", "dsti_qty": "Disti Qty", "err_flg": "Error Flag"}
        self.bom_disti_list = []

    def merge_data(self):
        # approach used for this problem is
        # loop through all bom items
        # check against the aggregated disti list
        # if part number matches then look for the respective quantity in disti list
        # if the quantity is more than bom quantity , then split it
        # and assign the remainder back to disti list

        self.__print_debug_data(self.bom_list, 'original bom_list')
        self.__print_debug_data(self.disti_list, 'original disti_list')

        for bom in self.bom_list:
            print('bom', bom)
            # creating dummy dict to be filled over in the subsequent steps
            bom_disti = {"bom_pn": "", "bom_qty": "",
                         "dsti_pn": "", "dsti_qty": "", "err_flg": ""}
            bom_partno = bom['Part Number']
            bom_qty = bom['Quantity']
            bom_disti["bom_pn"] = bom_partno
            bom_disti["bom_qty"] = bom_qty

            for disti in self.disti_list:
                # initialising error flag to default X
                bom_disti["err_flg"] = "X"
                disti_partno = disti['Part Number']
                disti_qty = disti['Quantity']
                disti['__matched'] = False

                # when the part number of bom matches with that of disti
                if bom_partno == disti_partno:
                    # if there are any disti quantities left
                    # negative or 0 quantity means we have used up all the disti parts quantities
                    if disti_qty > 0:
                        # get the remaining quantities
                        remainder = disti_qty - bom_qty
                        disti["Quantity"] = remainder
                        bom_disti["dsti_pn"] = disti_partno
                        # if remainder is >=0 i.e. there are additional quantities then assign the value equal to bom quantity
                        # else we are short on quantity so assign the original disti quantity itself
                        bom_disti["dsti_qty"] = bom_qty if remainder >= 0 else disti_qty
                        # update the error flag to blank if the bom qty matches disti qty
                        bom_disti['err_flg'] = "" if bom_disti["bom_qty"] == bom_disti["dsti_qty"] else "X"
                    # we want to break the loop since we dont want it to iterate to other parts once part is matched
                    break

            self.bom_disti_list.append(bom_disti)

        # add the remaining disti items which were not present in the bom list
        for disti in self.disti_list:
            bom_disti = {"bom_pn": "", "bom_qty": "",
                         "dsti_pn": "", "dsti_qty": "", "err_flg": ""}
            bom_disti["err_flg"] = "X"
            disti_partno = disti['Part Number']
            disti_qty = disti['Quantity']

            # add the items only if there is any remaining quantity available
            if disti['Quantity'] > 0:
                bom_disti["dsti_pn"] = disti_partno
                bom_disti["dsti_qty"] = disti_qty
                self.bom_disti_list.append(bom_disti)

        # debug printing the unformatted output list
        self.__print_debug_data(self.bom_disti_list,
                                'final output bom_disti_list')
        self.__print_to_console()

        return self.bom_disti_list

    def __print_to_console(self):
        headers = []
        rows = []
        for bom_disti in self.bom_disti_list:
            # create header rows from the key cols
            headers += list(bom_disti.keys()) if not headers else []

            # create rows with left justified and fixed string length for display
            rows.append(' '.join([str(val).ljust(10)
                        for val in bom_disti.values()]))

        print(' '.join([self.bom_disti_lbl_keys[h].ljust(10)
              for h in headers]))
        [print(r) for r in rows]

    def __print_debug_data(self, data, message=None):
        print('-'*100)
        print(message)

        if type(data) == list:
            for d in data:
                print(d)
        else:
            print(data)
        print('\n')


class TestQuoteMerge(unittest.TestCase):
    def test_merged_data(self):
        bom_list = [
            {"Part Number": "ABC", "Quantity": 2},
            {"Part Number": "XYZ", "Quantity": 1},
            {"Part Number": "IJK", "Quantity": 1},
            {"Part Number": "ABC", "Quantity": 1},
            {"Part Number": "IJK", "Quantity": 1},
            {"Part Number": "XYZ", "Quantity": 2},
            {"Part Number": "DEF", "Quantity": 2}
        ]

        disti_list = [
            {"Part Number": "XYZ", "Quantity": 2},
            {"Part Number": "GEF", "Quantity": 2},
            {"Part Number": "ABC", "Quantity": 4},
            {"Part Number": "IJK", "Quantity": 2},
        ]

        output_log = [{'bom_pn': 'ABC', 'bom_qty': 2, 'dsti_pn': 'ABC', 'dsti_qty': 2, 'err_flg': ''},
                      {'bom_pn': 'XYZ', 'bom_qty': 1, 'dsti_pn': 'XYZ', 'dsti_qty': 1, 'err_flg': ''}, {'bom_pn': 'IJK', 'bom_qty': 1, 'dsti_pn': 'IJK',
                                                                                                        'dsti_qty': 1, 'err_flg': ''}, {'bom_pn': 'ABC', 'bom_qty': 1, 'dsti_pn': 'ABC', 'dsti_qty': 1, 'err_flg': ''},
                      {'bom_pn': 'IJK', 'bom_qty': 1, 'dsti_pn': 'IJK',
                       'dsti_qty': 1, 'err_flg': ''},
                      {'bom_pn': 'XYZ', 'bom_qty': 2, 'dsti_pn': 'XYZ',
                       'dsti_qty': 1, 'err_flg': 'X'},
                      {'bom_pn': 'DEF', 'bom_qty': 2, 'dsti_pn': '',
                       'dsti_qty': '', 'err_flg': 'X'},
                      {'bom_pn': '', 'bom_qty': '', 'dsti_pn': 'GEF',
                       'dsti_qty': 2, 'err_flg': 'X'},
                      {'bom_pn': '', 'bom_qty': '', 'dsti_pn': 'ABC', 'dsti_qty': 1, 'err_flg': 'X'}]
        simulator = QuoteMerge(bom_list, disti_list)

        output = simulator.merge_data()
        self.assertCountEqual(output, output_log,
                              "Expected the output should match the log data ")


if __name__ == '__main__':
    unittest.main()
    # bom_list = [
    #     {"Part Number": "ABC", "Quantity": 2},
    #     {"Part Number": "XYZ", "Quantity": 1},
    #     {"Part Number": "IJK", "Quantity": 1},
    #     {"Part Number": "ABC", "Quantity": 1},
    #     {"Part Number": "IJK", "Quantity": 1},
    #     {"Part Number": "XYZ", "Quantity": 2},
    #     {"Part Number": "DEF", "Quantity": 2}
    # ]

    # disti_list = [
    #     {"Part Number": "XYZ", "Quantity": 2},
    #     {"Part Number": "GEF", "Quantity": 2},
    #     {"Part Number": "ABC", "Quantity": 4},
    #     {"Part Number": "IJK", "Quantity": 2},
    # ]
    # simulator = QuoteMerge(bom_list, disti_list)
    # simulator.merge_data()
