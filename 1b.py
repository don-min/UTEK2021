# Q1b
# imports 
import json
import collections
import itertools

def read_file(filename):
    '''
    Reads .json file and returns contents
    @param myParam1: str
    @return: dict
    '''
    with open(filename, "r") as myfile:
        content = json.load(myfile)
    return content  


def accessible(content):
    '''
    Returns accessibility ratio given path nodes
    @param myParam1: list
    @return: float
    '''
    # Stores accessible stations
    output = []

    # Check for accessibility
    for station in content:
        if station["Accessible"] == True:
            output.append(station["Name"])

    # Computes ratio
    return len(output)/len(content)


def run(filename, outfile, k=3):
    '''
    Computes top k accessible paths give .json file contents and writes to 1b.out with outputs
    @param myParam1: dict
    @return: dict
    '''
    data = read_file(filename)

    output = open(outfile, 'w')
    output.seek(0)

    # Var that keeps track of first term, applicable in formatting json file
    start = 1

    # Parses data into {PathName: Accessibility Ratio}
    path_dict = {}
    [val_list] = data.values()
    for i in range(0, len(val_list)):
        path_dict[val_list[i]["PathName"]] = accessible(val_list[i]["Nodes"])

    # Sorts dictionary in reverse order
    order_dict = {k: v for k, v in sorted(path_dict.items(), key=lambda item: item[1], reverse=True)}

    # Extracts top k accessible paths
    k_accessible = collections.OrderedDict(itertools.islice(order_dict.items(), k))

    # Writes results to outfile
    for path in k_accessible:
        if start == 1:
            output.write(path)
            start = 0
        else:
            output.write(", " + path)
    return order_dict


# Driver Code
if __name__ == "__main__":
    run("1b.json", "1b.out", k=3)
    