import random

def  math_test(i,point_number):
    for  x in range(i):
        j = round(random.uniform(0,50),point_number)
        k = round(random.uniform(0,50),point_number)
        test = round(j + k,point_number)


        print(j,k,test)


if __name__ == '__main__':
    #math_test(10,None)
    math_test(50,2)
