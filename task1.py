import Numpy as np

FILE_NAME = 'test_data.txt'
# FILE_NAME = 'ipums.txt'

# class Person(Base):
#     age = Column(Integer)
#     gender = Column(Integer)
#     gender = Column(Integer)
#     marital = Column(Integer)
#     race_status = Column(Integer)
#     birth_place = Column(Integer)
#     language = Column(Integer)
#     occupation = Column(Integer)

data_set = np.array([])


def read_data():
    global data_set
    file = open(FILE_NAME, "r")
    # print(file.read())
    for line in file:
        data_set.append(line.rstrip('\n').split("\t"))
    file.close()


if __name__ == "__main__":
    read_data()
    print(data_set)
