import xlrd

class towns:
    def __init__(self):
        self.book = xlrd.open_workbook('Random Shops.xlsx')
        self.townInfo = self.book.sheet_by_name('Town Sheet') #the sheet with the overall info of the town
        self.shopNames = self.book.sheet_by_name('ShopNames')
        self.randomTreasures = self.book.sheet_by_index(1)
        self.shops = {}
        for row in range(9, 19):
            self.shops[self.townInfo.cell(row, 0).value] = []
            for col in range(1,8):
                self.shops[self.townInfo.cell(row, 0).value].append(self.townInfo.cell(row, col).value)

        """Sorry in advance, very bad hard code coming right up"""
        self.shops['Innkeep'].append(self.townInfo.cell(1, 1).value + ' ' + self.townInfo.cell(1, 2).value+ ' ')
        self.shops['Alchemist'].append(self.townInfo.cell(2, 1).value + ' ' + self.townInfo.cell(2, 2).value+ ' ')
        self.shops['Blacksmith'].append(self.townInfo.cell(3, 1).value + ' ' + self.townInfo.cell(3, 2).value+ ' ')
        self.shops['Jeweler'].append(self.townInfo.cell(4, 1).value + ' ' + self.townInfo.cell(4, 2).value+ ' ')
        self.shops['Enchanter'].append(self.townInfo.cell(5, 1).value + ' ' + self.townInfo.cell(5, 2).value+ ' ')
        self.shops['Magic Weps'].append(self.townInfo.cell(6, 1).value + ' ' + self.townInfo.cell(6, 2).value+ ' ')
        self.shops['General Store'].append('')
        self.shops['Guard Captain'].append('')
        self.shops['Holy Person'].append('')
        self.shops['Townmaster'].append('')
        stock = {}

        for j in range(6):
            stock[self.townInfo.cell(2 + j, 9).value] = self.townInfo.cell(2 + j, 10).value
        self.shops['Blacksmith'].append(stock)
        stock = {}

        for j in range(6):
            stock[self.townInfo.cell(2 + j, 12).value] = self.townInfo.cell(2 + j, 13).value
        self.shops['Jeweler'].append(stock)
        stock = {}

        for j in range(12):
            stock[self.townInfo.cell(15 + j, 9).value] = self.townInfo.cell(15 + j, 10).value
        self.shops['Alchemist'].append(stock)
        stock = {}

        for j in range(6):
            stock[self.townInfo.cell(2 + j, 15).value] = self.townInfo.cell(2 + j, 16).value
        self.shops['Enchanter'].append(stock)
        stock = {}

        for j in range(6):
            stock[self.townInfo.cell(15 + j, 9).value] = self.townInfo.cell(15 + j, 10).value
        self.shops['Magic Weps'].append(stock)
        stock = {}
        #print(self.shops['Blacksmith'][8])

    def viewAllShops(self):
        stuff = 'Inhabitants:\n'
        for shops in self.shops:
            stuff+=(f"{shops}: {self.shops[shops][7]}run by {self.shops[shops][0]} {self.shops[shops][1]}, a {self.shops[shops][4]} {self.shops[shops][3]} {self.shops[shops][2]}. Traits: {self.shops[shops][5]}, {self.shops[shops][6]}\n")

        return stuff

    def viewStocks(self, shop):
        stuff = ''
        for items in self.shops[shop][8]:
            stuff+= (str(items) + ': ' + str(self.shops[shop][8][items]) + '\n')
        return stuff

if __name__ == "__main__":
    town = towns()
    town.viewStocks('Enchanter')

town = towns()