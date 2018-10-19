from threading import Thread
from time import sleep
from random import uniform
from random import randint

emulations = [
    {
        'floors': [z for z in range(randint(1, 10))],
        'path': {
            'tag': i,
            'coordinates': [
                {'x': a * i, 'y': a * i} for a in range(randint(5, 25))
            ]
        }
    }
    for i in range(1, 10)
]


class WorkersController:
    __workers = set()
    __active_tags = {}
    __paths = []
    __used_tags = set()
    __tags_path_node = {}
    __tags_path_length = {}
    __tags_path = {}
    __tags_floor_sequence = {}

    def __init__(self, emulations):
        for emulation in emulations:
            for floor_number in emulation['floors']:
                self.__workers.add(floor_number)
            self.__paths.append(emulation)
            self.__tags_path_node[emulation['path']['tag']] = \
                len(emulation['path']['coordinates']) - 1
            self.__tags_path_length[emulation['path']['tag']] = \
                len(emulation['path']['coordinates'])
            self.__tags_path[emulation['path']['tag']] = \
                emulation['path']['coordinates']
            self.__tags_floor_sequence[emulation['path']['tag']] = \
                emulation['floors']

    def emulate(self):
        for worker in self.__workers:
            session_tags = [p for p in self.__paths if
                            worker in p['floors']]
            threaded_worker = Thread(
                target=self.__emulator,
                args=(session_tags, worker),
                name='worker_{}'.format(worker)
            )
            threaded_worker.start()

    def __emulator(self, session_tags, worker):
        path_steps = 2500
        self.__active_tags[worker] = \
            [tag['path']['tag'] for tag in session_tags
             if tag['path']['tag'] not in self.__used_tags]
        for used_tag in self.__active_tags[worker]:
            self.__used_tags.add(used_tag)
        while path_steps > 0:
            path_steps -= 1
            for tag in self.__active_tags[worker]:
                node = self.__tags_path_node[tag]
                # coordinates = self.__tags_path[tag][node]
                # print('worker {}, tag: {}, coordinates: {}'
                #       .format(worker, tag, coordinates))
                if node is not 0:
                    self.__tags_path_node[tag] -= 1
                else:
                    self.__tags_path_node[tag] = \
                        self.__tags_path_length[tag] - 1
                    self.__allocate_tag_to_next_worker(tag, worker)
            if len(self.__active_tags[worker]) > 0:
                print('WORKER {} TAGS: {}'
                      .format(worker, self.__active_tags[worker]))
            nap_t = uniform(.1, .5)  # napping for random time
            sleep(nap_t)

    def __allocate_tag_to_next_worker(self, tag, previous_worker):
        i = self.__tags_floor_sequence[tag].index(previous_worker)
        worker = None
        if i == len(self.__tags_floor_sequence[tag]) - 1:
            worker = self.__tags_floor_sequence[tag][0]
        else:
            worker = self.__tags_floor_sequence[tag][i + 1]
        self.__active_tags[previous_worker].remove(tag)
        self.__active_tags[worker].append(tag)


if __name__ == '__main__':
    for emulation in emulations:
        floors = emulation['floors']
        tag = emulation['path']['tag']
        path_len = len(emulation['path']['coordinates'])
        print(f'emulations to run on floors for tag:'
              f' {tag}: {floors} for path length: {path_len}')
    sleep(5)
    workers_controller = WorkersController(emulations)
    workers_controller.emulate()
