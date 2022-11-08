import os
import pandas as pd


total = {"N Images": "# Total Images",
        "N Dog Images": "# Dog Images",
        "N Not Dog Images": "# Not-a-Dog Images"}
cnn_title = ["% Not-a-Dog Correct", "% Dogs Correct",
             "% Breeds Correct", "% Match Labels"]
cnn_models = ["vgg", "resnet", "alexnet"]
index_title = "CNN Model Architecture:"


results_file = [x for x in os.listdir() if x.split(".")[-1] == "txt" and x.split("_")[0] in cnn_models]


def read_files(file_collection):
    uploaded = {}
    
    for file in results_file:
        if "uploaded" in file:
            key = file.split("_")[0]

            with open(file, "r") as mod_res:
                value = mod_res.readlines()

            uploaded[key] = value
            
    return short_reads(clean_reading(uploaded))


def clean_reading(readings):
    clean = {}
    
    for k, v in readings.items():
        new_line = []
        
        for line in v:
            if line != "\n":
                new = line.replace("\n", "")
                new_line.append(new.strip())
        
        clean[k] = new_line
                
    return clean


def short_reads(reads):
    final = {}
    
    for key, value in reads.items():
        no = False
        res = []

        for line in value:
            if "*** Results Summary for" in line:   
                no = True

            if no:
                res.append(line)
                
        final[key] = res
        
    return final


def separate_readings(dicts):
    short_dicts = {k: v[1: 4] for k, v in dicts.items()}
    long_dicts = {k: v[5: 9] for k, v in dicts.items()}
    loc = list(dicts.keys())[0]
    short_results = {}
    long_results = {}
    
    for i in range(0, 3):
        sets = short_dicts[loc][i].split(":")
        index = sets[0].strip()
        value = int(sets[-1].strip())
        key = total[index]
        short_results[key] = value
        
        
    corrected_val = [[str(round(float(y), 1)) + "%" for y in x] for x in long_dicts.values()]
    val = list(zip(*list(corrected_val)))
    key = cnn_title
    
    for i in range(0, len(key)):
        long_results[key[i]] = val[i]
        
    final_res = pd.DataFrame(long_results, index = list(long_dicts.keys()))
    final_res.index.name = index_title
    
    print(pd.Series(short_results))
    print(final_res)
