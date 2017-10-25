import pickle

def read_pickle_file(path):
    data_list = []
    with open(path, 'rb') as readFile:
        item_count = pickle.load(readFile)
        for _ in range(item_count):
            data = pickle.load(readFile)
            data_list.append(data)
    return data_list

def write_pickle_file(path, data_list):
    with open(path, 'wb') as writeFile:
        pickle.dump(len(data_list), writeFile)
        for i in range(len(data_list)):
            pickle.dump(data_list[i], writeFile)