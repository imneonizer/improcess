## improcess [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

```python
pip install improcess
```

This tiny little python module is useful for creating multiple process of any function in seconds.

#### Latest v0.1.0

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

def my_func(i):
    process = improcess.console_log(output=True)
    try:
        time.sleep(5)
        return i*100
    except Exception as e:
        improcess.stop()
        

if __name__ == '__main__':
    multi_processing = improcess.multi_processing(my_func, max_process=10)
    raw_data = list(range(10))

    st = time.time()
    result = multi_processing.start(raw_data)
    et = round((time.time() - st),2)
    print(f'Result: {result}')
    print(f'Elapsed time: {et} sec')
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

#### Example 2

````python
import improcess
import time
import requests

#the function for processing data
def my_func(data):
    improcess.console_log(output=True)
    data = requests.get("http://httpbin.org/get")
    return data

if __name__ == '__main__':
    #building a imthreading object
    multi_processing = improcess.multi_processing(my_func, max_process=20)

    raw_data = list(range(1,21))

    st = time.time()
    
    #sending arguments for asynchronous multi processing
    processed_data = multi_processing.start(raw_data)

    #printing the synchronised received results
    print()
    #print('>> Input: {}'.format(raw_data))
    print('>> Result: {}'.format(processed_data))
    print('>> Elapsed time: {} sec'.format(round((time.time()-st),2)))
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
>> Elapsed time: 6.51 sec
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