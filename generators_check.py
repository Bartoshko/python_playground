from time import sleep

def firstn(n):
    num = 0
    while num < n:
        sleep(0.001)
        print(num)
        yield num
        num += 1 

sum_of_first_n = sum(firstn(1000))
for i in firstn(10):
    sleep(1)
    print(i)

print(sum_of_first_n)
