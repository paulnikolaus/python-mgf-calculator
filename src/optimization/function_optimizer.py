"""Simple Optimizer"""

from math import inf
from typing import List

import numpy as np
import scipy.optimize

from nc_arrivals.arrival_distribution import ArrivalDistribution
from nc_server.constant_rate_server import ConstantRateServer
from utils.exceptions import ParameterOutOfBounds
from utils.perform_parameter import PerformParameter


def optimizer_st(fun: callable,
                 s: int,
                 t: int,
                 arr_list: List[ArrivalDistribution],
                 ser_list: List[ConstantRateServer],
                 number_param: int,
                 ranges: list,
                 print_x=False) -> float:
    def helper_fun(param_list: [float, float]) -> float:
        # if len(param_list) != number_param:
        #     raise ValueError(
        #         f"Number of parameters {len(param_list)} is wrong")

        if number_param == 1:
            try:
                return fun(theta=param_list[0],
                           s=s,
                           t=t,
                           arr_list=arr_list,
                           ser_list=ser_list)
            except (FloatingPointError, ParameterOutOfBounds, OverflowError):
                return inf

        elif number_param == 2:
            try:
                return fun(theta=param_list[0],
                           s=s,
                           t=t,
                           arr_list=arr_list,
                           ser_list=ser_list,
                           p=param_list[1])
            except (FloatingPointError, ParameterOutOfBounds, OverflowError):
                return inf

        else:
            raise NotImplementedError(f"This number of parameters ="
                                      f" {number_param} is not implemented")

    # np.seterr("raise")
    np.seterr("warn")

    grid_res = scipy.optimize.brute(func=helper_fun,
                                    ranges=ranges,
                                    full_output=True)

    if print_x:
        print("grid search optimal x: ", grid_res[0].tolist())

    return grid_res[1]


def optimizer_perform(fun: callable,
                      arr_list: List[ArrivalDistribution],
                      ser_list: List[ConstantRateServer],
                      perform_param: PerformParameter,
                      number_param: int,
                      ranges: list,
                      print_x=False) -> float:
    def helper_fun(param_list: [float, float]) -> float:
        # if len(param_list) != number_param:
        #     raise ValueError(
        #         f"Number of parameters {len(param_list)} is wrong")

        if number_param == 1:
            try:
                return fun(theta=param_list[0],
                           perform_param=perform_param,
                           arr_list=arr_list,
                           ser_list=ser_list)
            except (FloatingPointError, OverflowError, ParameterOutOfBounds,
                    ValueError):
                return inf

        elif number_param == 2:
            try:
                return fun(theta=param_list[0],
                           perform_param=perform_param,
                           arr_list=arr_list,
                           ser_list=ser_list,
                           p=param_list[1])
            except (FloatingPointError, OverflowError, ParameterOutOfBounds,
                    ValueError):
                return inf

        elif number_param > 2:
            try:
                return fun(theta=param_list[0],
                           perform_param=perform_param,
                           arr_list=arr_list,
                           ser_list=ser_list,
                           p_list=param_list[1:])
            except (FloatingPointError, OverflowError, ParameterOutOfBounds,
                    ValueError):
                return inf

        else:
            raise NotImplementedError(f"This number of parameters ="
                                      f" {number_param} is not implemented")

    # np.seterr("raise")
    np.seterr("warn")

    grid_res = scipy.optimize.brute(func=helper_fun,
                                    ranges=ranges,
                                    full_output=True)

    if print_x:
        print("grid search optimal x: ", grid_res[0].tolist())

    return grid_res[1]
