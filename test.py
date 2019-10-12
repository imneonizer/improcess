import improcess
import random
import time

names = ['April', 'May']

#the function for processing data
def my_func(data):
    improcess.console_log(output=True)
    name = random.choice(names)
    time.sleep(1)
    return f'{name} says, Hello World!'

if __name__=="__main__":
    processed_data = improcess.start(my_func, repeat=4)

    print(processed_data)
    improcess.elapsed(output=True)
