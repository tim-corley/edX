#!/usr/bin/env python3

# by placing the for loop within a function (main), we can call the square function from elsewhere without running the loop
def square(x):
    return x * x

def main():
    for i in range(10):
        print('{} squared is {}'.format(i, square(i)))

# if running this file, then execute main function
if __name__ == "__main__":
    main()
