## improcess [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

```python
pip install improcess
```

This tiny little python module is useful for creating multiple process of any function in seconds.

### Warning

if your tasks require to do more than 4 tasks to do in parallel, kindly don't use improcess as [imthread](https://github.com/imneonizer/imthread) is fast and reliable for huge parallelization using only single core. however while bench marking i have found that i was trying to do 1 million small tasks in parallel and imthread was not sufficient neither improcess because of limited number of cores. then i did a duo compilation of these two libraries to create 5 multi process with each 2,00, 000 threads and that took half the time than creating 1 million threads on single process alone, i tested it on google cloud those 1 million small tasks completed in 3 minutes, see the code in the last section.

#### Latest v1.0

A quick launch mode is added, just type `improcess.start(func_name, repeat=10)` and it will execute the given function given number of times in parallel. A standard way of measuring elapsed time is added as well. see examples below to understand how to use quick launch mode.

Other than that to keep a track on how many processes are been created in real time you can push in a new log method in your processing function so that whenever a new process is created you can see it. there are two methods of tracking them.

- just to print out the process number which is being created, use: `` improcess.console_log(output=True)``
- if you want to store it in some variable you can use: ``process_number = improcess.console_log()``
- in case some error occurs, the process will keep on running
- if you want to kill all the process use ``improcess.stop()`` inside your processing function while handling errors.
- Only down side is each process has their own memory space, but this doesn't matters as long as we are storing our output data at a particular place.

#### Problem Statement

- Let say  for example, we have a ``list`` of numbers from `1 to 10` and all we wanted to do is `multiply every number by 1000` but the  challenge is ``it takes 5 sec`` for multiplying a single number by 1000 from the list, I know its an arbitrary condition, but we can create it with ``time.sleep(5)`` function.
- Basically it can be used with GPU's where you can leverage the powers of multi cores to do task in parallel.
- Or you want to make a web request million times, without waiting for the server to respond you to make the next request in those cases threading is a solution but since running multiple threads on one single process cannot leverage the full power of processors so in those case we can use this library to create 4 process and with those process we can create 1000 threads using [imthread](https://github.com/imneonizer/imthread)  at once.

#### Working

So what this module does is, at the time of object initialization it takes in the function which is used for processing data and max number of processes which can be created at once, when running in multi cores of CPU/GPU, and as input it takes a list of arguments for which multiple processes will be created.

------

#### Example 1

```python
import improcess
import time

def my_func(data):
    process = improcess.console_log(output=True)
    time.sleep(5)
    return data*100

#list of input data for processing
raw_data = [1,2,3,4,5,6,7,8,9,10]

if __name__ == '__main__':
    result = improcess.start(my_func, repeat=10, max_process=10)
    print(f'Result: {result}')
    print(f'>>> Elapsed time: {improcess.elapsed()} sec')
```

#### output

```python
>>> Creating Process 1
>>> Creating Process 2
>>> Creating Process 3
>>> Creating Process 4
>>> Creating Process 5
>>> Creating Process 6
>>> Creating Process 7
>>> Creating Process 8
>>> Creating Process 9
>>> Creating Process 10
Result: [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
Elapsed time: 5.53 sec
```

Now you can clearly see, if we do it without multi processing it would have taken around ``50 Seconds`` for processing the data while doing the task one by one and waiting for ``5 Sec`` after running the function each time. but since we are doing it with multiprocessing it will take only ``5 Seconds``  for processing the same task with different data, in their individual process.

**one thing to take care is:** always execute the improcess.start() as

````
if __name__ == "__main__":
	improcess.start()
````

It is essential to prevent improcess from creating its own duplicate process.

#### Example 2

````python
import improcess
import requests

#the function for processing data
def my_func(data):
    improcess.console_log(output=True)
    data = requests.get("http://httpbin.org/get")
    return data

if __name__ == '__main__':
    #sending arguments for asynchronous multi processing
    processed_data = improcess.start(my_func, repeat=20, max_process=20)

    #printing the synchronised received results
    print(f'>> Result: {processed_data}')

    improcess.elapsed(output=True)
````

#### output

````python
>>> Creating Process 1
>>> Creating Process 2
>>> Creating Process 3
>>> Creating Process 4
>>> Creating Process 5
>>> Creating Process 6
>>> Creating Process 7
>>> Creating Process 8
>>> Creating Process 9
>>> Creating Process 10
>>> Creating Process 11
>>> Creating Process 12
>>> Creating Process 13
>>> Creating Process 14
>>> Creating Process 15
>>> Creating Process 16
>>> Creating Process 17
>>> Creating Process 18
>>> Creating Process 19
>>> Creating Process 20

>> Result: [<Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>]
>>> Elapsed time: 5.92 sec
````

In this example we didn't used `time.sleep()` instead we make a request to the webserver and it took ``0.5 seconds`` to get the result back so we did it 20 times with multi processing and were able to receive the results in less time in a synchronous order.

> Lets try to do it without multiprocessing and see how it affects the processing time.

we can specify that at once how many process should be created so lets change the input parameter as ``max_process = 1`  while creating the [improcess](https://github.com/imneonizer/improcess) object, this way it will only create one process at a time and will wait until the previous process has finished properly.

#### output

````python
.
.
.
>> Elapsed time: 10.19 sec
````

It is clear that every request to the server was taking approx. ``0.5 seconds`` so while making one request at a time it took ``10.19 seconds`` as expected.

Though Expected Elapsed time is little bit slow in comparison to [imthread](https://github.com/imneonizer/imthread) library because in multi process each process have their own individual console and memory space. but both of these libraries can be used in conjunction to achieve ultra fast processing, instance we can create 4 individual processes and with every process we can call create 1000 threads. so it will be lot faster than using only [imthread](https://github.com/imneonizer/imthread) individually or [improcess](https://github.com/imneonizer/improcess) individually.

### Example 3

Quick Launch mode, a new feature is added where you can directly use improcess to pass in the repetitive function, input data for those functions and how many threads you want it to create at a time. other than that if you just want it to repeat the function without any inputs you can do that too.

### output

````python
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
````

we kept a time gap of 1 sec inside the function still it repeated the task 4 times in same time. since it can access the global variables we can assign certain tasks that don't need different inputs every time.

#### Handling errors and killing all process

So, by default if any error occurs the processes will keep on running, in case if you want to ignore some errors but if you want to kill all the process at once you can use ``improcess.stop()`` while handling errors.

```python
#the function for processing data
def my_func(data):
    process_number = improcess.console_log(output=True)
    try:
        data = requests.get("http://httpbin.org/get")
        return data
    except Exception as e:
        print(e) #printing other errors
        #killing all active process
        improcess.stop() #use to kill all process
```

if you don't use ``improcess.stop()`` function then the processes will keep on running and filling ``None`` in place of returned data. if you used the ``improcess.stop()`` it will kill all active processes immediately and will return the data that were processed by your function so far.

#### Similar Module

Also if your process are I/O bound you can use a similar library [imthread](https://github.com/imneonizer/imthread) which runs inside only one process and create multiple threads, and advantage of using multi threads over multi process is that you can share your memory space in between other threads.

#### Balanced use of improcess and imthread

I tride to do this awesome fun experiment with both the libraries and the take away is try to use imthread as much as you can and once its limits are reached use improcess to boost its capabilities by spawing a new process. we are going to encrypt a piece of text with different password for a million time. i used [imcrypt](https://github.com/imneonizer/imcrypt), an awesome library for any kind of file encryption in python. For the experiment below please install required libraries:

````python
pip install imthread
pip install improcess
pip install imcrypt
````

**Here's the source code**
````python
import imcrypt
from imcrypt.imcrypt import ImCrypt
import time
import imthread
import improcess
import random

text = 'hello world'

def my_func_p(data):
    def my_func_t(data):
        original = text
        key = ImCrypt.generate_unique_key(0)
        encrypted = imcrypt.encrypt(original, key=key)
        return encrypted, key, original

    processed_data = imthread.start(my_func_t, repeat=total_threads, max_threads=10000)
    return processed_data

total_threads = 50000
total_process = 20
if __name__ == '__main__':
    processed_data = improcess.start(my_func_p, repeat=total_process, max_process=4)
    for data_p in processed_data:
        for data in data_p:
            encrypted, key, original = data[0], data[1], data[2]
            print(f"Encrypted: '{encrypted}' Key: '{key}' Original: '{original}'")

    print(f"Elapsed: {improcess.elapsed()} sec for {total_threads*total_process} Encryption")
````

#### Output
````
Elapsed: 120.67 sec for 1000000 Encryption
````
so, it took 2 minutes to encrypt a text with different passwords 1 million times. I know it sound too good to be true but its real now you can try to do the same stuff with using imthread only and see the time difference it will take 4 times of 2 minutes.
