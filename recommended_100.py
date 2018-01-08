import json
import time

from Agents.BenchmarkWithoutEnd import BenchmarkWithoutEndAgent
from BackgroundServerMonitor import BackgroundServerMonitor
from executor import main


# grab cpu stats?

# mixed_scenario_enders_and_getters = {ReserverEnder: 30, ReserverSingleGetter: 20}
# reserve_get_status = {ReserverGetterOnlyStatus: 30}


# Create reservation, then end it
# main(ReserverEnder)

# Create reservation, then end it
# main(ReserverSingleGetter)


class PerformanceCombination:
    def __init__(self, sleep_between_groups, actions_per_group):
        self.sleep_between_groups = sleep_between_groups
        self.actions_per_group = actions_per_group


actions_per_group = [5, 10, 25, 33, 50]
sleep_between_groups = [0]
recommended = dict()

bests = [PerformanceCombination(0, 25), PerformanceCombination(0, 25), PerformanceCombination(30, 20), PerformanceCombination(15, 5)]

for sleep_between_group in sleep_between_groups:
    spg_result = dict()
    for apg in actions_per_group:
        start = time.time()
        reserve_benchmark_flow = {BenchmarkWithoutEndAgent: 5000}
        monitor = BackgroundServerMonitor()
        results = main(reserve_benchmark_flow, number_of_action_groups=100//apg,
                       number_of_actions_per_group=apg, sleep_between_groups=sleep_between_group, main_loop_iterations=5)
        monitor.stop()
        end = time.time()
        errors = results["total number of errors"]
        elapsed = end - start
        spg_result[apg] = {"duration": elapsed, "errors": errors,
                           "average_cpu_percent": monitor.cpu_percent,
                           "memory": monitor.memory}
    recommended[sleep_between_group] = spg_result
    with open('optimizer_{0}.json'.format(str(sleep_between_group)), 'w') as fp:
        json.dump(spg_result, fp)

# for best in bests:
#     spg_result = dict()
#     start = time.time()
#     reserve_benchmark_flow = {BenchmarkWithoutEndAgent: 5000}
#     monitor = BackgroundServerMonitor()
#     results = main(reserve_benchmark_flow, number_of_action_groups=100/best.actions_per_group,
#                    number_of_actions_per_group=best.actions_per_group, sleep_between_groups=best.sleep_between_groups,
#                    main_loop_iterations=5)
#     monitor.stop()
#     end = time.time()
#     errors = results["total number of errors"]
#     elapsed = end - start
#     spg_result[best.actions_per_group] = {"duration": elapsed, "errors": errors,
#                        "average_cpu_percent": monitor.cpu_percent,
#                        "memory": monitor.memory}
#     recommended[best.sleep_between_groups] = spg_result
#     with open('optimizer_{0}.json'.format(str(best.sleep_between_groups)), 'w') as fp:
#         json.dump(spg_result, fp)



# with open('optimizer.json', 'w') as fp:
#     json.dump(recommended, fp)

