from exported import CakeExportedTransactions

CSV_FILE = "/mnt/Data/pCloudDocs/Finanz/Crypto/DefiCake/2022-12-12_15-41-52_Cake.csv"


def main():
    exported = CakeExportedTransactions(CSV_FILE)
    print(exported.ingoing.head(20))
    print(exported.outgoing.head(20))


if __name__ == '__main__':
    main()
