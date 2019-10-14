import multiprocessing
from random import randint, choice
from time import sleep

from dojo.client import Client
from dojo.queue import SimpleQueue

MAX_SLEEP_TIME = 15

commands = {
    'dequeue': [
        b'DEQUEUE'  
    ],
    'enqueue': [
        b'ENQUEUE smart-lavousier upload',
        b'ENQUEUE smart-lavousier train',
        b'ENQUEUE ingenuous-wozniak train',
        b'ENQUEUE smart-lavousier persist',
        b'ENQUEUE ingenuous-wozniak upload',
        b'ENQUEUE gentle-tesla train',
        b'ENQUEUE gentle-tesla remove',
        b'ENQUEUE ingenuous-wozniak persist'
    ]
}

def worker_enq():
    command = choice(commands.get('enqueue'))
    elapsed = randint(0, MAX_SLEEP_TIME)
    
    client = Client()
    sleep(elapsed)
    response = client.send_data(command)
    client.shutdown()
    print('>> ENQUEUED: ({})\tTook {}s'.format(
        command, elapsed))

def worker_deq():
    command = choice(commands.get('dequeue'))
    elapsed = randint(0, MAX_SLEEP_TIME)
    
    client = Client()
    sleep(elapsed)
    response = client.send_data(command)
    client.shutdown()
    print('<< DEQUEUED: ({})\tAfter {}s'.format(response[0], elapsed))
    
def run_async_requests(n=5):
    for i in range(n):
        fn = worker_enq if i % 2 == 0 else worker_deq
        process = multiprocessing.Process(
            name = 'worker_{}'.format(i),
            target=worker_enq,
        )
        try:
            process.start()
        except:
            process.terminate()
        # else:
        #     process.join()
        
    for i in range(n):
        process = multiprocessing.Process(
            name = 'worker_{}'.format(i),
            target=worker_deq,
        )
        try:
            process.start()
        except:
            process.terminate()
        # else:
        #     process.join()

if __name__ == '__main__':
    queue = SimpleQueue()
    run_async_requests(10)
    sleep(MAX_SLEEP_TIME + 1)
    # ensure that list is empty:
    assert not queue._deserialize_list()
    print('Success 😛')