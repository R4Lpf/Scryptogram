#import language_tool_python 

# tool = language_tool_python.LanguageTools("en-US")
# text = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
# matches = tool.check(text)
# solution = language_tool_python.utils.correct(text, matches)

import string
import language_tool_python as lt

ALPHABET = string.ascii_uppercase #+ string.ascii_lowercase
alpha_dict= {}
reverse_alpha_dict =  {}
for i in range(0,26):
    reverse_alpha_dict[ALPHABET[i]] = i
    alpha_dict[i] = ALPHABET[i]


FIRSTCAND = [] # array of integers
CANDIDATELIST = [] #array of strings
COUNTER = -1

def modifyPuzzle(string):
    buffer = string.replace("-"," ").replace(".","").replace(",","")
    stringList = buffer.split(" ")
    buffer = ""
    hSet = set()
    for word in stringList:
        if word in hSet:
            continue
        else:
            hSet.add(word)
            buffer += word + " "
    return buffer[:-1]         

def convertToCanonicalForm(string):
    hMap = dict()
    ans = ""
    start = 0
    string = string.upper()
    for c in string:
        if c == " ":
            ans += " "
            continue
        else:
            if c not in hMap:
                hMap[c] = start
                start+=1
            ans += alpha_dict[hMap[c]]
    return ans

def isSame(map, newMap):
    return sorted(map) == sorted(newMap)

# =============================================================================
# No ciphertext letter may be mapped to more than one
# plaintext letter. For example, (X=A, X=B) is forbidden.
# A plaintext letter can only be mapped to once. E.g.,
# (X=A, Y=A) is forbidden.
# =============================================================================

"""
map è una lista di 26 lettere e ad ogni indice c'è una lettera se per esempio ad indice 0 c'è una M,
vuol dire che A nel cipher text equivale ad M nel plain text
[M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,A,B,C,D,E,F,G,H,I,J,K,L]
"""

def isConsistent(map, cipherWord, plainText): #this controls if the MAP is correct
    for i in range(len(cipherWord)):
        if plainText[i] not in map[reverse_alpha_dict[cipherWord[i]]]:
            return False
    return True
        
        
def printMappings(map):
    for i in range(26):
        print(alpha_dict[i] + "-->" + map[i])
        
def selfIntersection(map, string, hMap):
    t = len(string)-1
    
    while t!=0:
        boh = len(string)-t-1
        cipherWord = string[boh]
        print("######################################")
        print(cipherWord)
        print("######################################")
        newMap = [[]]*26
        candidateWords = CANDIDATELIST[boh]
        cipherLetter = [False] * 26
        i = FIRSTCAND[boh]
        g = []
        while candidateWords!=[] and i<len(candidateWords):
            buffer = candidateWords[i].upper()
            if isConsistent(map,cipherWord, buffer):
                for j in range(len(cipherWord)):
                    cipherLetter[reverse_alpha_dict[cipherWord[j]]] = True
# =============================================================================
#                     if buffer[j] not in newMap[reverse_alpha_dict[cipherWord[j]]]:
#                         print(alpha_dict[reverse_alpha_dict[cipherWord[j]]])
# =============================================================================
                    if buffer[j] not in g:
                        g.append(buffer[j])
                    #print(len(newMap[reverse_alpha_dict[cipherWord[j]]]))

            else:
                print(candidateWords[FIRSTCAND[boh]], candidateWords[i])
                candidateWords[FIRSTCAND[boh]],candidateWords[i] = candidateWords[i],candidateWords[FIRSTCAND[boh]]
                FIRSTCAND[boh]+=1
            i+=1
        for i in range(26):
            if cipherLetter[i]:
                newMap[i] = g
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(newMap,len(newMap))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        map = [newMap[k] for k in range(26) if cipherLetter[k]]
        t = t-1
    return map
        
def allCipherTextKnown(map):
    empty = [[]]*26
    for i in range(26):
        if len(map[i])>1:
            return False
    return True
    

def printSolution(string, map):
    ans = ""
    for c in string:
        try:
            ans += str(map[reverse_alpha_dict[c]])
        except:
            ans += " "
    print(ans)

def solveRecursive(inputString, map, string, hMap, selectedWord):
    
    if allCipherTextKnown(map):
        printSolution(inputString, map)
    
    candidateWords = []
    tmp = [[]] * 26
    while not isSame(tmp,map):
        for i in range(26):
            tmp[i] = map[i]
        selfIntersection(map,string,hMap)
    
    FIRSTCANDtmp = [-1]*len(FIRSTCAND)
    for j in range(len(FIRSTCAND)):
        FIRSTCANDtmp[j] = FIRSTCAND[j]
    i = FIRSTCAND[selectedWord]
    while i<len(CANDIDATELIST[selectedWord]):
        candidateWords.append(CANDIDATELIST[selectedWord][i])
        i+=1
    hasChild = False
    for i in range(len(candidateWords)):
        plainWord = candidateWords[i].lower()
        cipherWord = string[selectedWord]
        if isConsistent(map, cipherWord, plainWord):
            for k in range(26):
                tmp[k] = map[k]
            checker = [False]*26
            for j in range(len(cipherWord)):
                if not checker[cipherWord[j]]:
                    checker[cipherWord[j]] = True
                    hSet = []
                    hSet.append(plainWord[j])
                    tmp[cipherWord[j]] = hSet
            solveRecursive(inputString, tmp, string, hMap, selectedWord+1)
            hasChild = True    
        
        for j in range(len(FIRSTCAND)):
            FIRSTCAND[j] = FIRSTCANDtmp[j]
    if not hasChild:
        print("Partial Solution: " + str(FIRSTCAND[selectedWord]) + " " + str(len(CANDIDATELIST[selectedWord])))
                    
def planner(map):
    global COUNTER
    COUNTER +=1
    return COUNTER




cipherText = "MUG NGJ KIX CGCXSL LG CGCXSL FP QJPL K PLGIN."
plain = "Who you are moment to moment is just a story."
hMap = dict()
with open("usa.txt", "r") as file1:
    language = file1.read().splitlines()

for word in language:
    canonical = convertToCanonicalForm(word)
    if canonical in hMap:
        hMap[canonical].append(word)
    else:
        tmp = []
        tmp.append(word)
        hMap[canonical] = tmp
file1.close()

cipherInputted = modifyPuzzle(cipherText).split(" ")   
print(cipherInputted)

print("_____________________________________________________")
print("HMAP:")
print(hMap)
print("_____________________________________________________")
CANDIDATELIST = [""]*len(cipherInputted)
can = []
for i in range(len(cipherInputted)):
    can.append(convertToCanonicalForm(cipherInputted[i]))
    CANDIDATELIST[i] = hMap[convertToCanonicalForm(cipherInputted[i])]
    
print(CANDIDATELIST)

    
map = [[]]*26

for i in range(26):
    if map[i] == [] and alpha_dict[i] in cipherText:
        map[i] = [letter for letter in string.ascii_uppercase]
    elif alpha_dict[i] not in cipherText:
        map[i] = []
print("---------------------------------------------")
print("map:")
print(map)
print("---------------------------------------------")
FIRSTCAND = [0]*len(cipherInputted)

solveRecursive(cipherText, map, cipherInputted, hMap, 0)

for i in range(len(cipherInputted)):
    try:
        print(cipherInputted[i] + " " + CANDIDATELIST[i][FIRSTCAND[i]] + " " + str(FIRSTCAND[i]))
    except:
        print(cipherInputted[i] + " " )


          
# =============================================================================
# =============================================================================
# # import language_tool_python as lt
# # s = "A sentence with a error in the Hitchhiker’s Guide tot he Galaxy"
# # tool = lt.LanguageTool("en-US")
# # is_bad_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
# # matches = tool.check(s)
# # matches = [rule for rule in matches if not is_bad_rule(rule)]
# # lt.utils.correct(s, matches)
# =============================================================================
# 
# =============================================================================
# =============================================================================
# import stanza
# """
# @inproceedings{qi2020stanza,
#     title={Stanza: A {Python} Natural Language Processing Toolkit for Many Human Languages},
#     author={Qi, Peng and Zhang, Yuhao and Zhang, Yuhui and Bolton, Jason and Manning, Christopher D.},
#     booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations",
#     year={2020}
# }
# """
# =============================================================================

#print(set(r))


# =============================================================================
# class DictionaryLookUp:
#     def __init__(self):
#         self.firstcand = list(int())
#         self.candidateList = list(str())
#         self.counter = -1
# 
#     def modifyPuzzle(self, string) -> str():
#         stringBuffer = ""
#         for c in string:
#             if c == "-":
#                 stringBuffer += " "
#             elif c == " ":
#                 stringBuffer += " "
#             elif c in ALPHABET:
#                 stringBuffer += c
#         s = stringBuffer.split(" ")
#         stringBuffer = ""
# 
#         hSet = set()
# 
#         for i in s:
#             if i in hSet:
#                 continue
#             else:
#                 hSet.add(i)
#                 stringBuffer += i + " "
#         return stringBuffer[:-1]
# 
# 
#     def convertToCanonicalForm(self,string) -> str():
#         hMap = dict()
#         ans = ""
#         start = 0
#         for c in string:
#             if c not in hMap:
#                 hMap[c] = alpha_dict[start]
#                 start+=1
#             if c in hMap:
#                 ans += c
#         return ans
#     
#     def isSame(map: set(), newMap: set()) -> bool(): ## praticamente inutile ## prima erano dict() invece di set()
#         return map == newMap
# # =============================================================================
# #         for i in range(26):
# #             for z in map[i]:
# #                 if z in newMap[i]:
# #                     continue
# #                 else:
# #                     return False
# #         return True
# # =============================================================================
# 
#     def isConsistent(self, map: dict(), cipherText: str(), plainText: str()) -> bool():
#         for i in range(len(cipherText)):
#             if plainText[i] not in map[reverse_alpha_dict[cipherText[i]]]:
#                 return False
#         return True
#     
#     def printMappings(self, map: dict()):
#         for i in range(26):
#             c = "A"
#             print(alpha_dict[reverse_alpha_dict[c]+i])
#             for z in map[i]:
#                 print(z + " ")
#             print("-----------------------------------------")
#     
#     def selfInterseciton(map: dict(), string: str(), hMap: dict()) -> dict():
#         pass
# 
# 
# =============================================================================
#GIT HUB substitution_cipher_solver DictionaryLookUp


# =============================================================================
# solution =     "people will not remember what you did for living, they will remember how you touched them with kindness and loving."
# quote_string = "gjhgtj vqtt mhu sjfjfcjs vdiu xho kqk yhs tqwqmb, udjx vqtt sjfjfcjs dhv xho uhoedjk udjf vqud zqmkmjpp imk thwqmb"
# print(solution)
# 
# """
# tips:
# single letter words likely decrypt to A or I
# vowel letters such as E often have high frequency counts.
# letter groups following apostrophes are likely S, T, D, LL, RE 
# keep in mind common words and suffixes line AND, THE, OF, IN, IS, IT, -ING, etc.
# """
# 
# alphabet = "abcdefghijklmnopqrstuvwxyz"
# key =      "pkgrntxsm_bowufc_yidhlj_q_"
# keyd = {}
# print(len(solution))
# print(len(quote_string))
# for i in range(len(quote_string)):
#     q = quote_string[i]
#     s = solution[i]
#     keyd[s] = q
# 
# print(sorted(keyd.items()))
# 
# =============================================================================

"""
I read the paper made by Edwin Olson on Robust Dictionary Attack of Short Simple Substitution Ciphers. 05-10-2007
- No ciphertext letter may be mapped to more than one plaintext letter. For example, (X=A, X=B) is forbidden
- A plaintext letter can only be mapped to once. E.g., (X=A, Y=A) is forbidden.
A node in the tree substitutes a single letter rather than a whole word.


Algorithm 1 Solve(Map)
    for all X in {A, B, C, ..., Z} do:
        if (UserProvidedClue(X)) then:
            Map(X) = {UserClue(X)}
        else:
            Map(X) = {A, B, C, ..., Z}
    SolveRecursive(Map)

Algorithm 2 SolveRecursive(Map)
    if AllCipherTextKnown() then: #this is when we are at the bottom of the three
        ReportFullSolution(Map)
        return
    C = PlannerSelectUnknownLetterOrWord()
    has_child = False
    Map = SelfIntersection(Map)
    for all P in Candidates(C) do:
        if (IsConsistent(Map, C, P)) then:
            NewMap = AddMappings(Map, C, P)
            SolveRecursive(NewMap)
            has_child = True
    if (has_child = false) then:
        ReportPartialSolution(Map)
    return

Algorithm 3 SelfIntersection(Map)
    {Initialize Map to full sets}
    repeat
        for all C in CiphertextWords do
            {Initialize NewMap to empty sets}
            for all X in Candidates(C) do:
                NewMap(X) = {}
            for all P in Candidates(C) do:
                if (IsConsistent(Map, C, P)) then:
                    NewMap = AddMappings(NewMap, C, P)
            Map = Intersect(Map, NewMap)
    unitl no redutions performed
    return Map

"""
