"""
If you would like to change the name associated with an interlude, run this script as:

`python overwrite_interlude_perspective.py [chap_name] [perspective]`

EX:

`python overwrite_interlude_perspective.py "Let Slip 20.a" "Nomi"`

"""

import pickle
import sys

CHAP_NAME = None
PERSPECTIVE = None
if len(sys.argv)<3:
    with open('interlude_perspectives.pickle', 'rb') as file:
        INTERLUDE_PERSPECTIVES = pickle.load(file)

    print("{")
    for chap, perspec in INTERLUDE_PERSPECTIVES.items():
        print("    " + chap + "  :  " + perspec)
    print("}")

    raise("Error. Invalid number of arguments. Please read instructions in overwrite_interlude_perspective.py")
else:
    CHAP_NAME = sys.argv[1]
    PERSPECTIVE = sys.argv[2]

with open('interlude_perspectives.pickle', 'rb') as file:
    INTERLUDE_PERSPECTIVES = pickle.load(file)

INTERLUDE_PERSPECTIVES[CHAP_NAME] = PERSPECTIVE

print("{")
for chap, perspec in INTERLUDE_PERSPECTIVES.items():
  print("    " + chap + "  :  " + perspec)
print("}")

with open('interlude_perspectives.pickle', 'wb') as file:
    pickle.dump(INTERLUDE_PERSPECTIVES, file)
