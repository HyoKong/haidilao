import numpy as np
import os
import logging
import pandas as pd
import altgraph.Graph


def read_txt(txt):
    """

    """
    with open(txt, 'r') as f:
        raw_total_list = f.readlines()
        # total_list = []
        if 'cross.txt' in txt:
            column = ['id', 'roadID1', 'roadID2', 'roadID3', 'roadID4']
        else:
            column = raw_total_list[0].strip('#').strip('\n').strip('(').strip(')').split(',')

        df = pd.DataFrame(columns=column)
        for each in raw_total_list[1:]:
            each_list = each.strip('\n').strip('(').strip(')').split(',')
            each_list = [int(i) for i in each_list]
            df.loc[len(df.index)] = each_list
            # total_list.append(each_list)

    return df


if __name__ == '__main__':
    read_txt('./SDK/SDK_python/CodeCraft-2019/config/car.txt')
