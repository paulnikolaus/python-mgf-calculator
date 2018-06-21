"""Hopy-by-hop for canonical tree"""

from typing import List

from library.perform_parameter import PerformParameter
from library.setting import Setting
from nc_operations.operations import Convolve, Leftover
from nc_operations.perform_metric import PerformMetric
from nc_operations.performance_bounds import Delay, DelayProb
from nc_operations.performance_bounds_discretized import (DelayDiscretized,
                                                          DelayProbDiscretized)
from nc_processes.arrival import Arrival
from nc_processes.arrival_distribution import ArrivalDistribution
from nc_processes.service import Service
from nc_processes.service_distribution import ServiceDistribution


class TandemSFA(Setting):
    """Canonical tandem with hop-by-hop analysis"""

    def __init__(self, arr_list: List[ArrivalDistribution],
                 ser_list: List[ServiceDistribution],
                 perform_param: PerformParameter) -> None:
        # The first element in the arrival list in dedicated to the foi
        if len(arr_list) is not (len(ser_list) + 1):
            raise ValueError(
                "number of arrivals {0} and servers {1} have to match".format(
                    len(arr_list), len(ser_list)))
        self.arr_list = arr_list
        self.ser_list = ser_list
        self.perform_param = perform_param

    def get_bound(self, theta: float) -> float:
        number_servers = len(self.ser_list)

        foi: Arrival = self.arr_list[0]

        leftover_service_list: List[Service] = [
            Leftover(arr=self.arr_list[i + 1], ser=self.ser_list[i])
            for i in range(number_servers)
        ]

        s_net: Service = leftover_service_list[0]
        for i in range(1, number_servers):
            s_net = Convolve(s_net, leftover_service_list[i])


