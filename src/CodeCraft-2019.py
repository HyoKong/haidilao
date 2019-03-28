from utils import *
from altgraph import Graph, GraphAlgo
import logging
import sys
import pdb

logging.basicConfig(level=logging.DEBUG,
                    filename='./logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]
    # car_path = '../config/car.txt'
    # road_path = '../config/road.txt'
    # cross_path = '../config/cross.txt'
    # answer_path = '../config/answer.txt'

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    opts = {}
    opts['car_txt_path'] = car_path
    opts['cross_txt_path'] = cross_path
    opts['road_txt_path'] = road_path

    car_df = read_txt(car_path)
    cross_df = read_txt(cross_path)
    road_df = read_txt(road_path)

    # pdb.set_trace()
    car_df = car_df.sort_values(by=['speed', 'planTime'], ascending=False).sort_values(by=['planTime'])
    car_df = car_df.reset_index(drop=True)
    num = 15

    # edges = [(head , tail , weight) , ... ,]
    edges = []
    for i in range(len(road_df.index)):
        head = road_df.loc[i, 'from']
        tail = road_df.loc[i, 'to']
        # graph weight
        time = road_df.loc[i, 'length'] / (road_df.loc[i, 'speed'] * road_df.loc[i, 'channel'])
        edges.append((head, tail, time))

        if road_df.loc[i, 'isDuplex'] == 1:
            edges.append((tail, head, time))
    graph = Graph.Graph()
    for head, tail, weight in edges:
        graph.add_edge(head, tail, weight)

    total_path = []
    for i in range(len(car_df.index)):
        car_id = car_df.loc[i, 'id']
        car_df.loc[i, 'planTime'] = i // num + 1

        start = car_df.loc[i, 'from']
        stop = car_df.loc[i, 'to']
        dot_path = GraphAlgo.shortest_path(graph, start, stop)
        road_path = []
        for j in range(len(dot_path) - 1):
            road_id = road_df[((road_df.loc[:, 'from'] == dot_path[j]) & (road_df.to == dot_path[j + 1])) | (
                        (road_df.loc[:, 'from'] == dot_path[j + 1]) & (road_df.to == dot_path[j]))]['id'].values[0]
            road_path.append(road_id)
        road_path.insert(0, i // num + 1)
        road_path.insert(0, car_id)
        total_path.append(road_path)

    # to write output file
    with open(answer_path, 'w') as f:
        for each_car in total_path:
            f.write('(')
            for each in each_car[:-1]:
                f.write(str(each))
                f.write(',')
            f.write(str(each_car[-1]))
            f.write(')')
            f.write('\n')


if __name__ == "__main__":
    main()
