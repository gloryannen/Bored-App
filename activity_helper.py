import random
from decimal import Decimal
from forms import ActivitySearchCriteria

class RandomProps:
    price = None
    participants = None
    type = list
    
def assignRandVariable(price, participants, type):
    valuesToReturn = RandomProps()
    # Round to 2 decimals points.
    # Bored API only accepts up to 2 decimal places. Min/Max values -> [0, 1]
    valuesToReturn.price = round(Decimal(price), 2)
    
    # participants = form.participants.data
    # Randomize participants if 3+ is selected in the form. 
    # Bored API has some activities for more than 3 people.
    if participants == 3:
        nums = ["3", "4", "5","8"]
        valuesToReturn.participants = random.choice(nums)
        print(valuesToReturn.participants, "PARTICIPANTS RANDOM ----------------------------------------------------")
    else:
        valuesToReturn.participants = participants  
        print(valuesToReturn.participants, "PARTICIPANTS 1,2 ----------------------------------------------------")
          
 
    # type = form.activityType.data
    # Randomize activity if multiple are selected.
    valuesToReturn.type= random.choice(type) 
    
    return valuesToReturn