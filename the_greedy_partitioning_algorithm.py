import numpy as np

# FILE_NAME = 'test_data.txt'
# FILE_NAME = 'test_data_2.txt'
FILE_NAME = 'ipums.txt'


def read_data():
    data_set = np.loadtxt(FILE_NAME)

    return data_set


def write_date(data, name="output.txt"):
    f = open(name, "w")
    f.write(data)
    f.close()


def median(numpArray):
    length = len(numpArray)
    if len(numpArray) % 2 == 0:
        return np.sort(numpArray)[len(numpArray)//2-1]
    return np.sort(numpArray)[len(numpArray)//2]


def frequency_set(data_set, dim):
    dimArray = data_set[:, dim]
    unique_elements, counts_elements = np.unique(dimArray, return_counts=True)
    set = np.asarray((unique_elements, counts_elements))

    return set


'''
qii:Quasi Identifiers Indexes

'''


def choose_dimentsion(dims_index, qii):

    return [*dims_index, qii[len(dims_index)]]


'''
qii:Quasi Identifiers Indexes

'''


def anonymize(data_set, qii, k=20, dims_index=[]):
    if not len(dims_index) != len(qii):
        return(get_sanitized_data(data_set, dims_index))
    dims_index = choose_dimentsion(dims_index, qii)
    fs = frequency_set(data_set, dims_index[-1])
    split_val = median(data_set[:, dims_index[-1]])
    if not allowed_cut(fs, split_val, k):
        return(get_sanitized_data(data_set, dims_index))
    lhs = np.array([])
    rhs = np.array([])

    (lhs, rhs) = split(data_set, data_set[:, dims_index[-1]] <= split_val)

    return anonymize(lhs, qii, k=k, dims_index=dims_index) + anonymize(rhs, qii, k=k, dims_index=dims_index)


def split(arr, cond):
    return [arr[cond], arr[~cond]]


'''
If ( allowable multidimensional cut for 𝑝𝑎𝑟𝑡𝑖𝑡𝑖𝑜𝑛)

'''


def allowed_cut(fs, split_val, k):
    lhs_size = -1
    rhs_size = -1
    for val_index in range(len(fs[0])):
        if fs[0][val_index] > split_val:
            lhs_size = np.sum(fs[1, :val_index])
            rhs_size = np.sum(fs[1, val_index:])
            break
    return lhs_size >= k and rhs_size >= k


'''
ec : Equivalence Class
dims_index : the indexes for the dimensions used to develop the equivalence class

'''


def get_sanitized_data(ec, dims_index):

    dims_interval = [[np.min(ec[:, dim]), np.max(ec[:, dim])]
                     for dim in dims_index]
    output = ''
    for row in ec:

        for attr_index in range(len(row)):
            if attr_index in dims_index:
                attr_index_in_dims_index = dims_index.index(attr_index)
                if dims_interval[attr_index_in_dims_index][0] == dims_interval[attr_index_in_dims_index][1]:
                    output += str(dims_interval[attr_index][1])+"\t"
                else:
                    output += "[{},{}]\t".format(*
                                                 dims_interval[attr_index_in_dims_index])
            else:
                output += str(row[attr_index])+"\t"
        output += "\n"

    return output


def get_summary(ec, dims_index):

    dims_interval = [[np.min(ec[:, dim]), np.max(ec[:, dim])]
                     for dim in dims_index]
    output = ''
    for row in ec:

        for attr_index in range(len(row)):
            if attr_index in dims_index:
                attr_index_in_dims_index = dims_index.index(attr_index)
                if dims_interval[attr_index_in_dims_index][0] == dims_interval[attr_index_in_dims_index][1]:
                    data.low = dims_interval[attr_index_in_dims_index][0]
                    data.highe = dims_interval[attr_index_in_dims_index][1]
                    output += str(dims_interval[attr_index][1])+"\t"
                else:
                    output += "[{},{}]\t".format(*
                                                 dims_interval[attr_index_in_dims_index])
            else:
                output += str(row[attr_index])+"\t"
        output += "\n"

    return output


if __name__ == "__main__":
    data = read_data()
    # add the indexes for the Quasi-identifiers
    qii = [0, 1, 2, 3, 4, 5, 6]
    s_data = anonymize(data, qii, k=100)
    write_date(s_data)
