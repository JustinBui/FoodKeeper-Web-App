import pandas as pd
import re

storageInfo = {
    "Pantry": [
        "Pantry_Min",
        "Pantry_Max",
        "Pantry_Metric",
        "Pantry_tips",
        "DOP_Pantry_Min",
        "DOP_Pantry_Max",
        "DOP_Pantry_Metric",
        "DOP_Pantry_tips",
        "Pantry_After_Opening_Min",
        "Pantry_After_Opening_Max",
        "Pantry_After_Opening_Metric"
    ],
    "Refrigerate": [
        'Refrigerate_Min',
        'Refrigerate_Max',
        'Refrigerate_Metric',
        'Refrigerate_tips',
        'DOP_Refrigerate_Min',
        'DOP_Refrigerate_Max',
        'DOP_Refrigerate_Metric',
        'DOP_Refrigerate_tips',
        'Refrigerate_After_Opening_Min',
        'Refrigerate_After_Opening_Max',
        'Refrigerate_After_Opening_Metric',
        'Refrigerate_After_Thawing_Min',
        'Refrigerate_After_Thawing_Max',
        'Refrigerate_After_Thawing_Metric'
    ],
    "Freeze" : [
        "Freeze_Min",
        "Freeze_Max",
        "Freeze_Metric",
        "Freeze_Tips",
        "DOP_Freeze_Min",
        "DOP_Freeze_Max",
        "DOP_Freeze_Metric",
        "DOP_Freeze_Tips"
    ]
}

# ================================================= Functions Made the Past (Eugene, Lyba) in food_item_info=================================================
df = pd.read_excel('FoodKeeper-Data.xls', sheet_name = 'Product')

def isNaN(string): return string != string

def foodNameFinder(key):
    for index  in range(len(df['Name'])-1):
        nameSearch = df['Name'].iloc[index]
        ifFound = key.lower().capitalize()
        if nameSearch == ifFound: return [index, nameSearch]

def foodNameFinder(key):
    for index  in range(len(df['Name'])-1):
        nameSearch = df['Name'].iloc[index]
        ifFound = key.lower().capitalize()
        if nameSearch == ifFound: return [index, nameSearch]

def getColumns(info, index):
    temp = []
    if storageInfo.get(info):
        for column in storageInfo[info]:
            if isNaN(df[column].iloc[index]) == False:
                temp.append(column)
    return temp

def entityFound(key):
    return True if foodNameFinder(key) != None else False

def foodStorage(foodName, information):
    tempString = ''
    foundFood = foodNameFinder(foodName)
    
    # If the foodName entity is not found, the function returns 'No tip to give!'
    if entityFound(foodName):
        index = foundFood[0]
        foodName = foundFood[1]
    else: return ['No Tip to give!']
    
    # -------------------- Assuming food storage is found --------------------
    info = information.lower().capitalize()
    tempCol = getColumns(info, index)
    all_info = []
    
    for col in tempCol:
        tempString = ''
        if "Metric" in col:
            if "DOP" not in col:
                if isNaN(df[info + "_Metric"].iloc[index]) == False and df[info + "_Metric"].iloc[index] not in ['Days', 'Weeks', 'Months', 'Years']: tempString = f'{info.capitalize()} is {df[info + "_Metric"].iloc[index]}'
            if 'DOP' in col:
                if isNaN(df["DOP_" + info + "_Metric"].iloc[index]) == False and df["DOP_" + info + "_Metric"].iloc[index] not in ['Days', 'Weeks', 'Months', 'Years']: tempString = f'{info.capitalize()} is {df["DOP_" + info + "_Metric"].iloc[index]}'
            if 'After' in col and info == "Refrigerate":
                if isNaN(df[info + "_After_Thawing_Metric"].iloc[index]) == False and df[info + "_After_Thawing_Metric"].iloc[index] not in ['Days', 'Weeks', 'Months', 'Years']: tempString = f'{info.capitalize()} is {df[info + "_After_Thawing_Metric"].iloc[index]}'
                if isNaN(df[info + "_After_Opening_Metric"].iloc[index]) == False and df[info + "_After_Opening_Metric"].iloc[index] not in ['Days', 'Weeks', 'Months', 'Years']: tempString = f'{info.capitalize()} is {df[info + "_After_Opening_Metric"].iloc[index]}'
        if "DOP" in col and "Min" in col:
            min = df['DOP_' + info + '_Min'].iloc[index]
            max = df['DOP_' + info + '_Max'].iloc[index]
            if isNaN(min) == False and isNaN(max) == False:
                if min == max: tempString = f'The Date of Perish for {foodName} is {int(min)} {df["DOP_" + info + "_Metric"].iloc[index]}'
                else: tempString = f'The Date of Perish for {foodName} is from {int(min)} to {int(max)} {df["DOP_" + info + "_Metric"].iloc[index]}'
        if "Min" in col and "DOP" not in col:
            min = df[info + '_Min'].iloc[index]
            max = df[info + '_Max'].iloc[index]
            if isNaN(min) == False and isNaN(max) == False:
                if min == max: tempString = f'{foodName.capitalize()} can be stored in the {info} for {int(min)} {df[info + "_Metric"].iloc[index]}'
                else: tempString = f'{foodName.capitalize()} can be stored in the {info} for {int(min)} to {int(max)} {df[info + "_Metric"].iloc[index]}'
        if "After" in col and "Min" in col  and info == "Refrigerate":
            if "Thawing" in col:
                min = df[info + '_After_Thawing_Min'].iloc[index]
                max = df[info + '_After_Thawing_Max'].iloc[index]
                if isNaN(min) == False and isNaN(max) == False:
                    if min == max: tempString = f'{foodName.capitalize()} can be stored after thawing in the {info} for {int(min)} {df[info + "_After_Thawing_Metric"].iloc[index]}'
                    else: tempString = f'{foodName.capitalize()} can be stored after thawing in the {info} for {int(min)} to {int(max)} {df[info + "_After_Thawing_Metric"].iloc[index]}'
            else:
                min = df[info + '_After_Opening_Min'].iloc[index]
                max = df[info + '_After_Opening_Max'].iloc[index]
                if isNaN(min) == False and isNaN(max) == False:
                    if min == max: tempString = f'{foodName.capitalize()} can be stored after opened in the {info} for {int(min)} {df[info + "_After_Opening_Metric"].iloc[index]}'
                    else: tempString = f'{foodName.capitalize()} can be stored after opened in the {info} for {int(min)} to {int(max)} {df[info + "_After_Opening_Metric"].iloc[index]}'
        if "tips" in col or "Tips" in col:
            if "Freeze" in col:
                if "DOP" in col: tempString += f'A tip about {foodName} the Date of Perish is {df["DOP_" + info + "_Tips"].iloc[index]}'
                else: tempString = f'A tip about {foodName} is that {df[info + "_Tips"].iloc[index]}'
            else:
                if "DOP" in col: tempString += f'A {foodName} tip about the Date of Perish is {df["DOP_" + info + "_tips"].iloc[index]}'
                else: tempString = f'A tip about {foodName} is that {df[info + "_tips"].iloc[index]}'
    
        if tempString != '': all_info.append(tempString)                   
    return all_info if len(all_info) else ['No Tip to give!']


# ====================== NLP Functionalities ======================
def preProcess(tweet):
    #Converts a tweet to lowercase, replaces anyusername w/ <USERNAME> and URLS with <URL>
    tweet = tweet.lower()
    tweet = re.sub('@[a-zA-z0-9]*', '', tweet)              # <USERNAME>
    tweet = re.sub('http[a-zA-z0-9./:]*', '', tweet)       # <URL>
    tweet = re.sub('[.,-,!,",?]*', '', tweet)

    # Utilize for instragram posts, remove hashtag for food-related posts
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub('&amp;', 'and', tweet)
    #print(tweet)
    return tweet