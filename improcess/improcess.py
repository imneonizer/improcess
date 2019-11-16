import multiprocessing

p_index = 0
class multi_processing():
    def __init__(self, processing_func, max_process=4):
        assert type(max_process) == int, 'max_process value should be a integer'
        assert max_process >0, 'max_process Cannot be less than 1'
        self.max_process = max_process
        self.process = processing_func

    def process_data(self, data):
        global p_index
        p_index = data[0]
        #print(f'I am number {data[0]}')

        try:
            success = True
            #processing data here
            processed_data = data[2](data[1])
        except Exception as e:
            processed_data = None
            if str(e) == 'stop_process':
                success = False
            else:
                print(e)
        finally:
            return (success, data[0], processed_data)

    def start(self, raw_data):

        if type(raw_data) == int:
            pseudo_infinity = raw_data
            process_count = raw_data
        else:
            pseudo_infinity = len(raw_data)
            process_count = len(raw_data)

        if process_count < self.max_process:
            self.max_process = process_count
        elif process_count > multiprocessing.cpu_count():
            self.max_process = multiprocessing.cpu_count()

        #number of process to create
        pool = multiprocessing.Pool(processes = process_count)

        args = []
        final_result = []
        #marking each process with a index id
        try:
            for i in range(1, pseudo_infinity+1):
                try:
                    index_data = raw_data[i-1]
                except Exception:
                    index_data = i

                args.append((i, index_data, self.process))

                if i%self.max_process == 0:
                    #starting processes
                    result = pool.map(self.process_data, args) #internal_processing_func, arguments_list
                    for x in result:
                        if not x[2] == None:
                            final_result = final_result + [x[2]]#temp_result
                            #temp_result.append(x[2])
                        else:
                            final_result = final_result + [None]
                            #temp_result.append(None)
                    args = [] #wiping temporary arguments list

                    for success in result:
                        if not success[0]:
                            raise Exception('force_stop')
        except Exception as e:
            if str(e) == 'force_stop':
                print('Exception: Stop All Process')
            else:
                print(e)

        #returning synchronized output
        return final_result

def console_log(output=False):
    global p_index
    data = p_index
    if output:
        print(f'>>> Creating Process {data}')
    return data
