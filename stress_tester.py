from Agents.BenchmarkAgent import BenchmarkAgent

import this

from executor import main

# mixed_scenario_enders_and_getters = {ReserverEnder: 30, ReserverSingleGetter: 20}
# reserve_get_status = {ReserverGetterOnlyStatus: 30}


# Create reservation, then end it
# main(ReserverEnder)

# Create reservation, then end it
# main(ReserverSingleGetter)

NUMBER_OF_BUILDS_MULTIPLE_EXECUTIONS = [33]

# create reservation, then have a loop that checks if status has changed every two seconds
for itera in NUMBER_OF_BUILDS_MULTIPLE_EXECUTIONS:
    reserve_benchmark_flow = {BenchmarkAgent: 5000}
    main(reserve_benchmark_flow,
        number_of_action_groups=1, number_of_actions_per_group=itera, sleep_between_groups=0,
        main_loop_iterations=3)