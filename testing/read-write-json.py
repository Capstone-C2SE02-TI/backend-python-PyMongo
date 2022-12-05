
import json
 
# Data to be written
dictionary = {
    "investorERC20Balance" : {
        100 : 50
    }
}
 
# Serializing json
json_object = json.dumps(dictionary, indent=4)
 
# Writing to sample.json
with open("../craw/max-worker-statistic.json", "w") as outfile:
    outfile.write(json_object)