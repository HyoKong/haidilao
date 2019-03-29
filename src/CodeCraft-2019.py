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

def build_graph(road_df):
    # edges = [(head , tail , weight) , ... ,]
    edges = []
    for i in range(len(road_df.index)):
        head = road_df.loc[i, 'from']
        tail = road_df.loc[i, 'to']
        # graph weight
        time = road_df.loc[i, 'length'] * ((road_df.loc[i,'car_num']+1)) / (road_df.loc[i, 'speed'] * road_df.loc[i, 'channel'])
        edges.append((head, tail, time))

        if road_df.loc[i, 'isDuplex'] == 1:
            edges.append((tail, head, time))
    graph = Graph.Graph()
    for head, tail, weight in edges:
        graph.add_edge(head, tail, weight)
    return graph

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
    # cross_df = read_txt(cross_path)
    road_df = read_txt(road_path)
    # 用于记录当前道路车辆数目
    road_df['car_num'] = 0
    # pdb.set_trace()
    car_df = car_df.sort_values(by=['speed', 'planTime'], ascending=False).sort_values(by=['planTime'])
    car_df = car_df.reset_index(drop=True)
    
    # 用于记录当前车辆所在道路及位置
    car_df['current_road'] = None
    car_df['current_loc'] = None
    


    total_path = []
    # 已发车车辆行车路线
    total_path_dict = {}
    count = 0  # 总发车数量
    num = 10  # 每次发车数量

    # for i in range(len(car_df.index)):
    # while not total_path_dict: # 车没有全部到站
    # pdb.set_trace()
    while len(car_df.index)-1 >= count:        # 没有排到最后一辆车
        # del total_path_dict['init']
        
        for i in range(count,min(count+num,len(car_df.index))):
            car_id = car_df.loc[i, 'id']
            
            car_df.loc[i, 'planTime'] = i // num + 1
    
            start = car_df.loc[i, 'from']
            stop = car_df.loc[i, 'to']
            
            graph = build_graph(road_df)
            dot_path = GraphAlgo.shortest_path(graph, start, stop)
            road_path = []
            
            for j in range(len(dot_path) - 1):
                road_id = road_df[((road_df.loc[:, 'from'] == dot_path[j]) & (road_df.to == dot_path[j + 1])) | (
                            (road_df.loc[:, 'from'] == dot_path[j + 1]) & (road_df.to == dot_path[j]))]['id'].values[0]
                road_path.append(road_id)
            # total_path_dict[str(car_id)] = road_path

            
            road_path.insert(0, i // num + 1)
            road_path.insert(0, car_id)
            total_path.append(road_path)
            # print(car_id)
            total_path_dict.update({str(car_id): road_path[2:]})  # 存入已经规划好行车路线的所有车的路径，若车到站，则删除
        update_car_num(road_df, car_df, total_path_dict)
        count += num
        

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

# 更新每条道路上车辆数量，将其写入dataframe中
def update_car_num(road_df,car_df,total_path_dict):
    """
    :param road_df:
    :param car_df:
    :param count:当前已发车数量
    :param total_path_dict: 已发车车辆行车路线
    """
    delete_car_list = []
    for car, road_list in total_path_dict.items():
        # 更新car_df中的current_road和current_loc
        car_id = int(car)
        
        # pdb.set_trace()
        car_series = car_df[car_df['id'].isin([car_id])]
        
        if car_series.loc[:,'current_road'].values == None:             # 该车刚刚发车
            car_series.loc[:,'current_road'] = road_list[0]
            road_series = road_df[road_df['id'].isin([road_list[0]])]
            speed = min(car_series.loc[:,'speed'].values,road_series.loc[:,'speed'].values)
            car_series.loc[:,'current_loc'] = speed
            car_df[car_df['id'].isin([car_id])] = car_series
        else:                                                           # 该车已经走了一段路了
            current_road = car_series.loc[:,'current_road'].values[0]
            current_loc = car_series.loc[:,'current_loc'].values[0]
            road_series = road_df[road_df['id'].isin([current_road])]
            road_length = road_series.loc[:,'length'].values
            speed = min(car_series.loc[:, 'speed'].values, road_series.loc[:, 'speed'].values)

            # 判断是否是最后一条路
            if road_list.index(current_road) < len(road_list) - 1:      # 不是最后一条路
                next_road = road_list[road_list.index(current_road) + 1]
                next_road_series = road_df[road_df['id'].isin([next_road])]
                next_speed = min(car_series.loc[:, 'speed'].values, next_road_series.loc[:, 'speed'].values)
                # 判断是否通过路口
                if road_length-current_loc >= speed:  # 不能跑出该路
                    next_loc = speed+current_loc
                    car_series.loc[:,'current_loc'] = next_loc
                elif road_length-current_loc>=next_speed:
                    car_series.loc[:, 'current_loc'] = road_length
                else:
                    next_road = road_list[road_list.index(current_road)+1]
                    car_series.loc[:,'current_road'] = next_road
                    car_series.loc[:, 'current_loc'] = next_speed - road_length + current_loc
                car_df[car_df['id'].isin([car_id])] = car_series
                
            else:           # 是最后一条路
                if road_length-current_loc >= speed:  # 不能跑出该路
                    next_loc = speed+current_loc
                    car_series.loc[:,'current_loc'] = next_loc
                else:               # 到站
                    car_series.loc[:, 'current_loc'] = None
                    car_series.loc[:,'current_road'] = None
                    delete_car_list.append(car)
                    
    for each in delete_car_list:
        del total_path_dict[each]
                    
    # 更新road_df中的car_num:
    num_series = car_df['current_road'].value_counts()

    for each_road in num_series.index:
        # pdb.set_trace()
        road_series = road_df[road_df['id'].isin([each_road])]
        road_series.loc[:,'car_num'] = num_series[each_road].tolist()
    # return road_df
    
if __name__ == "__main__":
    main()
