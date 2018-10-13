# finding all factors for a given number
def find_factors(x): # define a function
  print ("The factors of ", x, " are: ")
  for i in range(1, x + 1):
    if x % i == 0:
      print(i)

def print_factors():
  # ask the user to input a number
  num = input("Enter a number to print its factors: ")
  if num >= 0: # check if the number is positive
    find_factors(num)
  elif num < 0: # if not, take the absolute value and find its factors
    numNew = abs(num)
    find_factors(numNew)
  else:
    print("Please enter a valid number.")
