# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 19:11:24 2019
@author: just4
"""

def CarSorted(fold):
    """
    Description:
    :fold:input,the answer.txt which the departing cars have been removed
          from the text.
    :StartTime:input,the current cars scheduling time
    :return:sorted CarId
    """
    with open(fold,'r') as file:
        result = []
        lines = file.readlines()[1:]
        for line in lines:
            line = line.strip('( )\n').split(',')
            for i in range(len(line)):
                line[i] = int(line[i])
#            if line[1] <= StartTime:
            result.append(line)
    result_return = sorted(result,key=lambda result:result[1])
    return [CarId[0] for CarId in result_return]