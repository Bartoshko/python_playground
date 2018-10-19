from multiprocessing import Process, Pipe
from time import sleep

# slower child
parent_t, child_t = .2, .3
# slower parent
# parent_t, child_t = .3, .2

some_x_value = 0


def f(conn):
    a = 0
    while a < 100:
        # print(f' x global value: {some_x_value}')
        sleep(parent_t)
        a += 1
        print(f'actual {a}')
        conn.send(a)
    conn.close()


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    run_forever = True
    while run_forever:
        some_x_value += 1
        # print(f'main thread x global value {some_x_value}')
        sleep(child_t)
        data_from_conn = parent_conn.recv()
        if parent_conn.recv() > 50:
            run_forever = False
        print(f'received {data_from_conn}')
    p.join()
    print('this is the end')
