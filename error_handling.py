try:
    name = input('Enter your full name')
    age = input('Enter your current age')
    print (f"You are {name} and your age is {age} years.")
except TypeError:
    print("Please be seriousand enter correct type")
except ValueError:
    print("Please be serious and enter the correct value")
except ZeroDivisionError:
    print("Please be serious and correct the zero division error")
