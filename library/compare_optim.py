"""We compare the different optimizations"""

from timeit import default_timer as timer
from typing import List

from library.setting_new import SettingNew
from optimization.initial_simplex import InitialSimplex
from optimization.nelder_mead_parameters import NelderMeadParameters
from optimization.opt_method import OptMethod
from optimization.optimize_new import OptimizeNew
from optimization.simul_anneal_param import SimulAnnealParam


def compare_optimization(setting: SettingNew,
                         opt_methods: List[OptMethod],
                         new=True,
                         print_x=False,
                         number_l=0) -> List[float]:
    """Measures time for different optimizations"""
    bound_list = []
    time_list = []

    for opt in opt_methods:
        start = timer()
        if opt == OptMethod.GRID_SEARCH:
            theta_bounds = [(0.1, 4.0)]

            bound_array = theta_bounds[:]
            for _i in range(1, number_l + 1):
                bound_array.append((0.9, 4.0))

            bound = OptimizeNew(
                setting_new=setting, new=new, print_x=print_x).grid_search_old(
                    bound_list=bound_array, delta=0.1)

        elif opt == OptMethod.PATTERN_SEARCH:
            theta_start = 0.5

            start_list = [theta_start] + [1.0] * number_l

            bound = OptimizeNew(
                setting_new=setting, new=new, print_x=print_x).pattern_search(
                    start_list=start_list, delta=3.0, delta_min=0.01)

        elif opt == OptMethod.NELDER_MEAD:
            nelder_mead_param = NelderMeadParameters()
            theta_start = 0.5

            start_list = [theta_start] + [1.0] * number_l
            start_simplex = InitialSimplex(parameters_to_optimize=number_l +
                                           1).gao_han(start_list=start_list)

            bound = OptimizeNew(
                setting_new=setting, new=new, print_x=print_x).nelder_mead_old(
                    simplex=start_simplex,
                    nelder_mead_param=nelder_mead_param,
                    sd_min=10**(-2))

        elif opt == OptMethod.SIMULATED_ANNEALING:
            simul_anneal_param = SimulAnnealParam()
            theta_start = 0.5

            start_list = [theta_start] + [1.0] * number_l

            bound = OptimizeNew(
                setting_new=setting, new=new,
                print_x=print_x).simulated_annealing(
                    start_list=start_list,
                    simul_anneal_param=simul_anneal_param)
        elif opt == OptMethod.BFGS:
            theta_start = 0.5

            start_list = [theta_start] + [1.0] * number_l

            bound = OptimizeNew(
                setting_new=setting, new=new,
                print_x=print_x).bfgs(start_list=start_list)

        else:
            raise NameError("Optimization parameter {0} is infeasible".format(
                opt.name))

        stop = timer()
        bound_list.append(bound)
        time_list.append(stop - start)

    print("time_list: ", time_list)
    print("bound_list: ")
    return bound_list


if __name__ == '__main__':
    from nc_operations.perform_metric import PerformMetric
    from nc_processes.arrival_distribution import ExponentialArrival
    from nc_processes.service_distribution import ConstantRate
    from single_server.single_server_perform import SingleServerPerform
    from fat_tree.fat_cross_perform import FatCrossPerform
    from library.perform_parameter import PerformParameter

    OUTPUT_TIME = PerformParameter(
        perform_metric=PerformMetric.OUTPUT, value=4)

    EXP_ARRIVAL = ExponentialArrival(lamb=4.4)
    CONST_RATE = ConstantRate(rate=0.24)

    SETTING1 = SingleServerPerform(
        arr=EXP_ARRIVAL, ser=CONST_RATE, perform_param=OUTPUT_TIME)
    OPT_METHODS = [
        OptMethod.GRID_SEARCH, OptMethod.PATTERN_SEARCH,
        OptMethod.SIMULATED_ANNEALING, OptMethod.BFGS
    ]

    print(
        compare_optimization(
            setting=SETTING1,
            opt_methods=OPT_METHODS,
            new=True,
            print_x=True,
            number_l=1))

    DELAY_PROB = PerformParameter(
        perform_metric=PerformMetric.DELAY_PROB, value=4)

    EXP_ARRIVAL1 = ExponentialArrival(lamb=11.0)
    EXP_ARRIVAL2 = ExponentialArrival(lamb=9.0)

    CONST_RATE1 = ConstantRate(rate=5.0)
    CONST_RATE2 = ConstantRate(rate=4.0)

    ARR_LIST = [EXP_ARRIVAL1, EXP_ARRIVAL2]
    SER_LIST = [CONST_RATE1, CONST_RATE2]

    SETTING2 = FatCrossPerform(
        arr_list=ARR_LIST, ser_list=SER_LIST, perform_param=DELAY_PROB)

    print(
        compare_optimization(
            setting=SETTING2,
            opt_methods=OPT_METHODS,
            new=True,
            print_x=True,
            number_l=1))
