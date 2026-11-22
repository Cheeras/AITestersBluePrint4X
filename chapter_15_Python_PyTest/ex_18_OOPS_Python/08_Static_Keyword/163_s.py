class ExcelReader:
    @staticmethod
    def readExcelFile():
        print("Reading from Excel")

class MYSQLDBConnction:
    @staticmethod
    def readMySQLFile():
        print("Readinf from MySQL")

class TC1:
    def runTC(self):
        ExcelReader.readExcelFile()
        MYSQLDBConnction.readMySQLFile()
        print("Hiii")

tc1 = TC1()
tc2 = TC1()


tc1.runTC()
tc2.runTC()