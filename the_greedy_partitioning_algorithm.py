import numpy as np

FILE_NAME = 'ipums.txt'
# Indexes of the Quasi Identifiers Indexes
dims_index = [0, 1, 2, 3, 4, 5, 6]
k = 9
sensitive_vlue_index = 7
ec_data = []


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
qii:Quasi Identifiers Index

'''


def choose_dimentsion(dims_index, qii):
    if len(dims_index)-1 == qii:
        return -1

    return 1+qii


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
qii:Quasi Identifiers Indexes

'''


def anonymize(data_set,  dims_index, k=10, qii=-1):

    # if not len(dims_index) != len(qii):
    #     return(get_sanitized_data(data_set, dims_index))

    qii = choose_dimentsion(dims_index, qii)
    fs = frequency_set(data_set, qii)
    split_val = median(data_set[:, qii])

    if qii == -1 or not allowed_cut(fs, split_val, k):
        return(get_sanitized_data(data_set, dims_index))

    lhs = np.array([])
    rhs = np.array([])

    (lhs, rhs) = split(data_set, data_set[:, qii] <= split_val)

    return anonymize(lhs, dims_index,  k=k, qii=qii) + anonymize(rhs, dims_index,  k=k, qii=qii)


def split(arr, cond):
    return [arr[cond], arr[~cond]]


'''
ec : Equivalence Class
dims_index : the indexes for the dimensions used to develop the equivalence class

'''


def get_sanitized_data(ec, dims_index):

    dims_interval = [[np.min(ec[:, dim]).astype(int), np.max(ec[:, dim]).astype(int)]
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
                output += str(row[attr_index].astype(int))+"\t"
        output += "\n"
    # call add_summary to add he EC information to be used in ILOSS
    add_summary(len(ec), dims_interval, len(
        np.unique(ec[:, sensitive_vlue_index])))
    return output


'''
this function adds the EC information to globle value ec_data

'''


# def add_summary(ec_length, dims_index, dims_interval, num_att):
#     global ec_data
#     data = {
#         'size': ec_length,
#         'att': []
#     }

#     data['size'] = ec_length
#     for attr_index in range(num_att):
#         if attr_index in dims_index:
#             attr_index_in_dims_index = dims_index.index(attr_index)
#             data['att'].append({
#                 'low': dims_interval[attr_index_in_dims_index][0],
#                 'up': dims_interval[attr_index_in_dims_index][1]

#             })
#         else:
#             data['att'].append({
#                 'low': dims_interval[attr_index_in_dims_index][0],
#                 'up': dims_interval[attr_index_in_dims_index][1]

#             })

#     ec_data.append(data)
def add_summary(ec_length, dims_interval, l_diverse):
    global ec_data
    data = {
        'size': ec_length,
        'att': dims_interval,
        'l_diverse': l_diverse
    }
    ec_data.append(data)


'''
g_attr: upper and lower values of the ith attribute

'''


def get_ec_info(dims_index):

    # get the cdm and size of the data set
    Cdm = 0

    # Dataser size
    size = 0
    for e in ec_data:
        Cdm += e['size']**2
        size += e['size']
    print('Cdm = ', Cdm)

    number_quasi_identifiers = len(dims_index)

    d_sum = 0
    g_attr = []
    for att_index in dims_index:
        g_attr.append([min([x['att'][att_index][0] for x in ec_data]),
                       max([x['att'][att_index][1] for x in ec_data])])

    min_diverse = size

    for ec in ec_data:

        if min_diverse > ec['l_diverse']:
            min_diverse = ec['l_diverse']

        for i, att in enumerate(ec["att"]):  # n
            d_sum += ((att[1]-att[0])*ec['size']/(g_attr[i][1]-g_attr[i][0]))
    iloss = d_sum/(size*number_quasi_identifiers)
    print('ILOSS = ', iloss)
    print('Utility = ', 1-iloss)
    print('l-diverse = ', min_diverse)


if __name__ == "__main__":
    data = read_data()
    # add the indexes for the Quasi-identifiers
    s_data = anonymize(data, dims_index=dims_index, k=k)
    write_date(s_data)

    get_ec_info(dims_index)
