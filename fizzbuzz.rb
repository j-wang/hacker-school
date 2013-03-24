# fizzbuzz.rb
# written by James Wang

# Write a program that prints out the numbers 1 to 100 (inclusive).
# If the number is divisible by 3, print Fizz instead of the number. If it's
# divisible by 5, print Buzz. If it's divisible by both 3 and 5, print
# FizzBuzz.

(1..100).each {|x| puts "#{'Fizz' if (x%3).zero?}" +
                        "#{'Buzz' if (x%5).zero?}" +
                        "#{x if !(x%5).zero? && !(x%3).zero?}"}
