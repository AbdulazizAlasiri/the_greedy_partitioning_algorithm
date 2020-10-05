import numpy as np

# FILE_NAME = 'test_data.txt'
FILE_NAME = 'ipums.txt'


def read_data():
    data_set = np.loadtxt(FILE_NAME, usecols=range(0, 8), dtype=np.int16)

    return data_set


def linkage_attack(dataset, table):

    for person in table:
        print("\nSarching for {}'s data... ".format(person[0]))
        findings = []
        for row in dataset:

            match = True
            for index in range(len(row)):
                if person[index + 1] is None:
                    continue
                match = person[index+1] == row[index]
                # print(person[index +
                #              1], "and  ", row[index])
                if not match:
                    break

            if match:

                row_found = row.tolist()
                findings.append(row_found)

        if len(findings):
            print("Age\tGender\tMarital\tRace\tBplace\tLang\tOccup\tIncome")
            for f in findings:
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7]))
        else:
            print("No match with {} information found ".format(person[0]))


if __name__ == "__main__":
    data = read_data()

    # whitout he gendar
    table1 = [
        ["Ahmed", 28, None, None, None, 110, None, None, None, ],
        ["Fatma", 44, None, None, None, 4, None, None, None, ],
        ["Ali", 17, None, None, None, 199, None, None, None],
        ["Abeer", 34, None, None, None, 260, None, None, None],
        ["Muhamad", 40, None, None, None, 15, None, None, None]]

    # whith he gendar
    table2 = [
        ["Ahmed", 28, 1, None, None, 110, None, None, None, ],
        ["Fatma", 44, 2, None, None, 4, None, None, None, ],
        ["Ali", 17, 1, None, None, 199, None, None, None],
        ["Abeer", 34, 2, None, None, 260, None, None, None],
        ["Muhamad", 40, 1, None, None, 15, None, None, None]]
    linkage_attack(data, table2)
