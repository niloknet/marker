given_number = int(input('give me a number'))

# do Collatz sequence 
while given_number != 1:
    if given_number % 2 == 0:
        print('is even')
          given_number = given_number // 2
    else:
      print('is odd')
      given_number = given_number * 3 + 1
      print(given_number)
      