# Q1a
# imports
import json

def accessible(filename, output):
    '''
    Reads .json file, returns contents, and writes to 1a.out all accessible stations
    @param myParam1: str
    @return: None
    '''
    output = open(output,'w')
  
    # Reads .json file and retrieves contents
    with open(filename, "r") as myfile:
        content = json.load(myfile)
        
        # Var that keeps track of first term, applicable in formatting .json file
        start = 1  
    
        # Checks for accessibility for each station
        for station in content["Nodes"]:
            if station["Accessible"] == True:
                # If first term
                if start == 1:
                    # Write to .json file
                    output.write(station["Name"])
                    start = 0
                else:                    
                    # Write to .json file
                    output.write(", "+station["Name"])


# Driver Code
if __name__ == "__main__":
    accessible("1a.json", "1a.out")