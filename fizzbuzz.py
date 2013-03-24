# fizzbuzz.py
# written by James Wang

# Write a program that prints out the numbers 1 to 100 (inclusive).
# If the number is divisible by 3, print Fizz instead of the number. If it's
# divisible by 5, print Buzz. If it's divisible by both 3 and 5, print
# FizzBuzz.

def fizzbuzz (maximum):
    for x in range(1, maximum + 1):
        if x % 3 == 0 and x % 5 == 0: yield "FizzBuzz"
        elif x % 3 == 0: yield "Fizz"
        elif x % 5 == 0: yield "Buzz"
        else: yield x

for x in fizzbuzz(100): print (x)













