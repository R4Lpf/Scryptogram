

solution =     "people will not remember what you did for living, they will remember how you touched them with kindness and loving."
quote_string = "gjhgtj vqtt mhu sjfjfcjs vdiu xho kqk yhs tqwqmb, udjx vqtt sjfjfcjs dhv xho uhoedjk udjf vqud zqmkmjpp imk thwqmb"
print(solution)

"""
tips:
single letter words likely decrypt to A or I
vowel letters such as E often have high frequency counts.
letter groups following apostrophes are likely S, T, D, LL, RE 
keep in mind common words and suffixes line AND, THE, OF, IN, IS, IT, -ING, etc.
"""

alphabet = "abcdefghijklmnopqrstuvwxyz"
key =      "pkgrntxsm_bowufc_yidhlj_q_"
keyd = {}
print(len(solution))
print(len(quote_string))
for i in range(len(quote_string)):
    q = quote_string[i]
    s = solution[i]
    keyd[s] = q

print(sorted(keyd.items()))
