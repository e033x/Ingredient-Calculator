import os, shutil, shelve

#'l': 1000, 'dl': 100, 'cl': 10, 'ml': 1, 'tsp': 5, 'tbsp': 15, 'fl.oz': 29.6, 'c': 240, 'pt': 473.2, 'qt': 946.3, 'gal': 3785.4

unitKeys = shelve.open('unitKeys')
if len(unitKeys) == 0:
    weightDef = {'kg': 1000, 'hg': 100, 'g': 1, 'mg': 0.1, 'oz': 28.3, 'lb': 453.6}
    volumeDef = {'l': 1000, 'dl': 100, 'cl': 10, 'ml': 1, 'tsp': 5, 'tbsp': 15, 
                 'fl.oz': 29.6, 'c': 240, 'pt': 473.2, 'qt': 946.3, 'gal': 3785.4}
    unitDecimalKey = {'kg': 2, 'hg': 1, 'g': 0, 'mg': 0, 'oz': 1, 'lb': 1, 
                      'l': 2, 'dl': 1, 'cl': 1, 'ml': 0, 'tsp': 1, 'tbsp': 1, 
                      'fl.oz': 1, 'c': 1, 'pt': 2, 'qt': 2, 'gal': 2}
    unitKeys['weightDef'] = weightDef
    unitKeys['volumeDef'] = volumeDef
    unitKeys['unitDecimalKey'] = unitDecimalKey
    unitKeys.close()
    print('Importing measurments')
else:
    unitKeys.close()
    print('Setup complete, welcome to this awesome program.')

#***********

def inputCleaner(cleaningObject):
    #for cleaning user input to match inputModifier keys in lib.txt
    stringList = list(cleaningObject)
    for i in range(0, len(stringList)):
        if stringList[i] == ' ':
            stringList[i] = ''
        else:
            continue
    outputString = "".join(stringList)
    return outputString.lower()

#***********

def libAdder(ingredientVar):
    lib = open('.\\lib.txt', 'a')
    newKey = inputCleaner(ingredientVar)
    while True:
        try:
            newValue = float(input('How many ml per gram?\n'))
            break
        except ValueError:
            print('***Please enter a number***')
            continue
    newEntry = newKey + ' ' + str(newValue)
    lib.write('\n' + newEntry)
    lib.close()
    return newKey
    
#***********

def manualLibAdder():
    lib = open('.\\lib.txt', 'a')
    newKey = inputCleaner(str(input('\nWhat is the name of the ingredient you want to add?\n')))
    while True:
        try:
            newValue = float(input('How many ml per gram?\n'))
            break
        except ValueError:
            print('***Please enter a number***\n')
            continue
    newEntry = newKey + ' ' + str(newValue)
    lib.write('\n' + newEntry)
    lib.close()
    return

#***********

def inputSelector():
    unitKeys = shelve.open('unitKeys')
    weightDef = unitKeys['weightDef']
    volumeDef = unitKeys['volumeDef']
    unitDecimalKey = unitKeys['unitDecimalKey']
    globalKeyControl = list(unitDecimalKey)
    weightKeyControl = list(weightDef)
    volumeKeyControl = list(volumeDef)
    modifierDef = {}
    
    with open('.\\lib.txt') as f:
        for line in f:
            (key, val) = line.split()
            modifierDef[key] = float(val)
    
    modifierKeyControl = list(modifierDef)
    
    
    print('\n' * 100)
    
    while True:
        inputKey = input('What is the unit?\n')
        if inputKey in globalKeyControl:
            break
        else:
            print('***That is not a recognized unit, please enter again***')
            continue

    while True:
        try:
            inputValue = float(input('What is the value?\n'))
            break
        except ValueError:
            print('***Please enter a number***\n')
            continue
    
    while True:
        outputKey = input('What do you want it converted to?\n')
        if outputKey in globalKeyControl:
            break
        else:
            print('***That is not a recognized unit, please enter again***\n')
            continue      
  
    if (inputKey in weightKeyControl and outputKey in volumeKeyControl) or (inputKey in volumeKeyControl and outputKey in weightKeyControl):
        ingredient = str(input('What is the ingredient you wish to convert?\n'))
        interModifier = inputCleaner(ingredient)
        if interModifier not in modifierKeyControl:
            print('\nThis ingredient does not currently exist in the library.')
            inputModifier = libAdder(interModifier)
            weightVolumeTransposer(inputKey, inputValue, inputModifier, outputKey)
        else:
            weightVolumeTransposer(inputKey, inputValue, interModifier, outputKey)
    
    else:
        simpleConverter(inputKey, inputValue, outputKey)


#***********

def weightVolumeTransposer(inputKey, inputValue, inputModifier, outputKey):
    unitKeys = shelve.open('unitKeys')
    modifierDef = {}
    weightDef = unitKeys['weightDef']
    volumeDef = unitKeys['volumeDef']
    unitDecimalKey = unitKeys['unitDecimalKey']
    weightKeyControl = list(weightDef)
    volumeKeyControl = list(volumeDef)  
    
    with open('.\\lib.txt') as f:
        for line in f:
            (key, val) = line.split()
            modifierDef[key] = float(val)
    
    if inputKey in weightKeyControl:
        interValue = inputValue * weightDef[inputKey]
        interValue = interValue * modifierDef[inputModifier]
        outputValue = interValue / volumeDef[outputKey]
        
        print('\n' * 100)
        print(str(inputValue) + ' ' + inputKey + ' of ' + inputModifier.title() + ' = ' + str(round(outputValue, unitDecimalKey[outputKey])) + ' ' + outputKey)
    
    elif inputKey in volumeKeyControl:
        interValue = inputValue * volumeDef[inputKey]
        interValue = interValue / modifierDef[inputModifier]
        outputValue = interValue / weightDef[outputKey]
        
        print('\n' * 100)
        print(str(inputValue) + ' ' + inputKey + ' of ' + inputModifier.title() + ' = ' + str(round(outputValue, unitDecimalKey[outputKey])) + ' ' + outputKey)
    
    else:
        print('\n' * 100)
        print('***Error***')


#*********

def simpleConverter(inputKey, inputValue, outputKey):
    unitKeys = shelve.open('unitKeys')
    weightDef = unitKeys['weightDef']
    volumeDef = unitKeys['volumeDef']
    unitDecimalKey = unitKeys['unitDecimalKey']
    globalKeyControl = list(unitDecimalKey)
    weightKeyControl = list(weightDef)
    volumeKeyControl = list(volumeDef)
    
    if inputKey in weightKeyControl and outputKey in weightKeyControl:
        interValue = inputValue * weightDef[inputKey]
        outputValue = interValue / weightDef[outputKey]
        
        print('\n' * 100)
        print(str(inputValue) + ' ' + inputKey + ' = ' + str(round(outputValue, unitDecimalKey[outputKey])) + ' ' + outputKey)
    
    else:
        interValue = inputValue * volumeDef[inputKey]
        outputValue = interValue / volumeDef[outputKey]
        
        print('\n' * 100)
        print(str(inputValue) + ' ' + inputKey + ' = ' + str(round(outputValue, unitDecimalKey[outputKey])) + ' ' + outputKey)


while True:
    query = input('\nPress any button to continue, Q to quit, N to add to library\n')
    if str(query.lower()) == 'q':
        break
    elif str(query.lower()) == 'n':
        manualLibAdder()
    else:
        inputSelector()