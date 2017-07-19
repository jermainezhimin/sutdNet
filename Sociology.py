import pandas as pd
import numpy as np
import math

######################
#       NODES
######################

#Reading and initializing all required resources
survey = pd.read_csv("/Users/jermainezhimin/Desktop/Socio Project/survey.csv")
surveyHeaders = list(survey.columns.values)


#Basic nodes
basicDict = {}
basicDict['Names'] = [a.lstrip().rstrip() for a in survey['Name']]
basicDict['name.Pillar'] = [a.lstrip().rstrip() for a in survey['Pillar']]
basicDict['name.GLPALP'] = [a.lstrip().rstrip() for a in survey['GLP/ALP?']]
basicDict['name.Club'] = [a for a in survey['How many voluntary interest or sports groups are you a member of?']]
basicDict['name.Residential'] = [a for a in survey['Residential']]
'''
pd.DataFrame(basicDict).to_csv('nodes.csv',index=False)
'''

#Name
nameFHeaders = [surveyHeaders[i] for i in [1,       #Name
               5,9,13,17,21,25,29,33,37,41]]         #Freshmore
namePHeaders = [surveyHeaders[i] for i in [1,       #Name
               45,49,53,57,61,65,69,73,77,81]]      #Pillar

#Pillar
pillarFHeaders = [surveyHeaders[i] for i in [3,      #Name
                 6,10,14,18,22,26,30,34,38,42]]       #Freshmore
pillarPHeaders = [surveyHeaders[i] for i in [3,      #Name
                 46,50,54,58,62,66,70,74,78,82]]     #Pillar

#Sex
sexFHeaders = [surveyHeaders[i] for i in [2,      #Name
              7,11,15,19,23,27,31,35,39,43]]       #Freshmore
sexPHeaders = [surveyHeaders[i] for i in [2,      #Name
              47,51,55,59,63,67,71,75,79,83]]     #Pillar

#Class
classFHeaders = [surveyHeaders[i] for i in [4,      #Name
                8,12,16,20,24,28,32,36,40,44]]       #Freshmore
classPHeaders = [surveyHeaders[i] for i in [4,      #Name
                48,52,56,60,64,68,72,76,80,84]]     #Pillar

def nodeCompiler(fileName, nameHeaders, pillarHeaders, sexHeaders, classHeaders, survey):

    print "==================START======================"
    print "Creating nodelist " + fileName

    nodeDict = {}
    compiledNames = []
    compiledPillars = []
    compiledSex = []
    compiledClass = []
        
    #Compiling all names
    for a in nameHeaders:
        compiledNames = compiledNames + [b for b in survey[a]]

    #Stripping white spaces
    for a in compiledNames:
        if (type(a) != float):
            compiledNames[compiledNames.index(a)] = a.lstrip().rstrip()

    #Compiling all pillars
    for a in pillarHeaders:
        compiledPillars = compiledPillars + [b for b in survey[a]]

    #Compiling all sex
    for a in sexHeaders:
        compiledSex = compiledSex + [b for b in survey[a]]

    #Compiling all classes
    for a in classHeaders:
        compiledClass = compiledClass + [b for b in survey[a]]
        
    uniqueNames = []
    uniquePillars = []
    uniqueSex = []
    uniqueClass = []

    #Compiling unique names and pillars
    for a in compiledNames:
        if (not (a in uniqueNames)) and (type(a) != float):
            uniqueNames = uniqueNames + [a]
            uniquePillars = uniquePillars + [compiledPillars[compiledNames.index(a)]]
            uniqueSex = uniqueSex + [compiledSex[compiledNames.index(a)]]
            uniqueClass = uniqueClass + [compiledClass[compiledNames.index(a)]]

    print "Length of nodelist: " + str(len(uniqueNames))

    nodeDict['Names'] = uniqueNames 
    nodeDict['name.Pillar'] = uniquePillars
    nodeDict['name.Sex'] = uniqueSex
    nodeDict['name.Class'] = uniqueClass

    pd.DataFrame(nodeDict).to_csv(fileName,index=False)
    print "===================END=======================\n"
    return



######################
#       EDGES
######################

#Reading and initializing all required resources

edgePDict = {}
eNodeHeaders = 'Name'                                                       #Name
eFHeaders = [surveyHeaders[i] for i in [5,9,13,17,21,25,29,33,37,41]]        #Freshmore
ePHeaders = [surveyHeaders[i] for i in [45,49,53,57,61,65,69,73,77,81]]     #Pillar

def edgeCompiler(fileName, eNodeHeaders, eHeaders, survey):

    print "==================START======================"
    print "Creating edgelist " + fileName

    edgeDict = {}
    fromNames = []
    toNames = []
    
    #Compiling all edges and tidying string
    for a in survey[eNodeHeaders]:
        for b in eHeaders:
            if (type(list(survey[b])[list(survey[eNodeHeaders]).index(a)]) != float):
                fromNames = fromNames + [a]
                toNames = toNames + [list(survey[b])[list(survey[eNodeHeaders]).index(a)]]

    for a in fromNames:
        fromNames[fromNames.index(a)] = a.lstrip().rstrip()

    for a in toNames:
        toNames[toNames.index(a)] = a.lstrip().rstrip()
        
    #Checking the loops and ensuring one direction only
    delIndex = []
    for a in range(0,len(fromNames)):
        test = [fromNames[a],toNames[a]]
        for b in range(0,len(fromNames)):
            if (a<b):
                check = [fromNames[b],toNames[b]]
                if sorted(test) == sorted(check):
                    delIndex = [a] + delIndex

    delIndex = list(set(delIndex))
    delIndex = sorted(delIndex,reverse=True)

    for a in delIndex:
        del fromNames[a]
        del toNames[a]
    
    print "Length of edgelist: " + str(len(fromNames))

    edgeDict['From'] = fromNames
    edgeDict['To'] = toNames

    pd.DataFrame(edgeDict).to_csv(fileName,index=False)

    print "===================END=======================\n"
    return

def dupRemover(fileName, dupCsv, basicDict):

    fromList = []
    toList = []
    
    edgeDup = dict(pd.read_csv(dupCsv))

    for a in range(0,len(edgeDup['From'])):
        if (edgeDup['From'][a] in basicDict['Names']) and (edgeDup['To'][a] in basicDict['Names']):
            fromList.append(edgeDup['From'][a])
            toList.append(edgeDup['To'][a])

    edgeDup['From'] = fromList
    edgeDup['To'] = toList
    
    pd.DataFrame(edgeDup).to_csv(fileName,index=False)
                
######################
#   FUNCTION CALLS
######################

nodeCompiler("nodeF.csv",nameFHeaders,pillarFHeaders,sexFHeaders,classFHeaders,survey)
nodeCompiler("nodeP.csv",namePHeaders,pillarPHeaders,sexPHeaders,classPHeaders,survey)
edgeCompiler("edgeF.csv", eNodeHeaders, eFHeaders, survey)
edgeCompiler("edgeP.csv", eNodeHeaders, ePHeaders, survey)
dupRemover("edgesF.csv", "/Users/jermainezhimin/Desktop/Socio Project/edgeF.csv", basicDict)
dupRemover("edgesP.csv", "/Users/jermainezhimin/Desktop/Socio Project/edgeP.csv", basicDict)

######################
#   RELATION CALLS
######################

edgeF = pd.read_csv("/Users/jermainezhimin/Desktop/Socio Project/edgesF.csv")
edgeP = pd.read_csv("/Users/jermainezhimin/Desktop/Socio Project/edgesP.csv")
eFHeaders = ['GLP/ALP?','How many voluntary interest or sports groups are you a member of?','Residential'] #GLP and ALP Values

def statCalculator(fileName, bStat, basicNode, eStat, types, edgeList, survey):

    basicNode[bStat + 'Stat' + types] = []

    #Initializing Variables
    for a in basicNode['Names']:

        #Begin counting of friends and similar friends
        checkStat = basicDict[bStat][basicNode['Names'].index(a)]
        fri = 0.0
        simFri = 0.0

        #Check link start 'from' end 'to'
        for b in range(0,len(edgeList['From'])):
            if a==edgeList['From'][b]:
                if edgeList['To'][b] in basicDict['Names']:
                    fri += 1.0
                    if checkStat== basicNode[bStat][basicDict['Names'].index(edgeList['To'][b])]:
                        simFri +=1.0

        for c in range(0,len(edgeList['To'])):
            if a==edgeList['To'][c]:
                if edgeList['From'][c] in basicDict['Names']:
                    fri += 1.0
                    if checkStat== basicNode[bStat][basicDict['Names'].index(edgeList['From'][c])]:
                       simFri +=1.0

        #Checking percentage
        if fri !=0:
            fri = float(simFri / fri)
            basicNode[bStat + 'Stat' + types].append(fri)

        else:
            basicNode[bStat + 'Stat' + types].append(fri)
            
    print "Calculated stats for " + bStat + " given " + types  
    pd.DataFrame(basicNode).to_csv(fileName,index=False)

'''
statCalculator('nodes.csv', 'name.Club', basicDict, 'How many voluntary interest or sports groups are you a member of?', 'F', edgeF, survey)
statCalculator('nodes.csv', 'name.Club', basicDict, 'How many voluntary interest or sports groups are you a member of?', 'P', edgeP, survey)
statCalculator('nodes.csv', 'name.GLPALP', basicDict, 'GLP/ALP?', 'F', edgeF, survey)
statCalculator('nodes.csv', 'name.GLPALP', basicDict, 'GLP/ALP?', 'P', edgeP, survey)
statCalculator('nodes.csv', 'name.Residential', basicDict, 'Residential', 'F', edgeF, survey)
statCalculator('nodes.csv', 'name.Residential', basicDict, 'Residential', 'P', edgeP, survey)
'''
