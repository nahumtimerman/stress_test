import json
import logging
import threading
import time

from Agents.ReserverEnderAgent import ReserverEnder
from cloudshell.api.cloudshell_api import *

from Agents.agent import AgentFactory

# BREAKER runs several batches, that start staggered i.e. run 10, then wait a bit then run another 10,
# then wait a bit then run another 10

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s', )

NUMBER_OF_BUILDS_MULTIPLE_EXECUTIONS = [1]
# NUMBER_OF_BUILDS = 15  # default
MAIN_LOOP = 1

users = ['admin']
domain = ['SSP SJC']
duts = ['[Any]']
topology = 'SSP SJC topologies/Topo 1 KP 2017-05-31 [SSP SJC]'
global_input = []
password = 'admin'
average_reserve_duration = []
average_reserve_duration_inside_iteration = []
errors_in_iteration = []
errors_in_entire_run = []
results = dict()
lockling = threading.Lock()
host = 'localhost'


class Statistics:
    def __init__(self):
        self.error = None
        self.duration = 0


def mean(l):
    a = sum(l) / float(len(l))
    return a


def cleanup():
    api = CloudShellAPISession(host, 'admin', password, 'Global')
    active_reservations = api.GetCurrentReservations('admin').Reservations
    for r in active_reservations:
        if ('Performance' in r.Name):
            try:
                api.EndReservation(r.Id)
            except:
                pass
            try:
                api.TerminateReservation(r.Id)
            except:
                pass


def main(requested_types_to_number_of_threads, number_of_action_groups=3, number_of_actions_per_group=10,
         sleep_between_groups=10, main_loop_iterations=1):
    api = CloudShellAPISession(host, 'admin', password, 'Global')
    MAIN_LOOP = main_loop_iterations
    active_reservations = api.GetCurrentReservations('').Reservations
    logging.debug('Starting test')
    logging.debug('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{0}\n~~~~~~~~~~~~~~~~~~~~~~~'.format(len(active_reservations)))

    number_of_builds = number_of_action_groups * number_of_actions_per_group
    results["number of threads"] = number_of_builds
    results["main loop"] = MAIN_LOOP

    main_loop_stats = []
    for j in xrange(MAIN_LOOP):
        af = AgentFactory(requested_types_to_number_of_threads, host, users[0], password, domain[0], topology)
        logging.debug('Loop {0}'.format(j))
        main_loop_start = time.time()
        threads = []
        errors_in_iteration = []
        iteration_stats = []

        for k in xrange(number_of_action_groups):
            for i in range(number_of_actions_per_group):
                agent = af.get_agent()
                thread_stats = Statistics()
                t = threading.Thread(target=agent.worker, args=(i, thread_stats))
                threads.append(t)
                t.start()
                iteration_stats.append(thread_stats)
                main_loop_stats.append(thread_stats)
            time.sleep(sleep_between_groups)

        [t.join() for t in threads]

        total_threads = number_of_action_groups * number_of_actions_per_group
        log_iteration_results(iteration_stats, j, main_loop_start, total_threads, number_of_builds)
        cleanup_iteration(errors_in_iteration)

    log_total_results(main_loop_stats, number_of_builds)


def log_total_results(main_loop_stats, number_of_builds):
    logging.debug('####### TOTAL AVERAGE ######')
    logging.debug('{0} of threads'.format(number_of_builds))
    logging.debug('{0} main loop iterations'.format(MAIN_LOOP))
    total_durations = [stat.duration for stat in main_loop_stats]
    total_errors = [stat.error for stat in main_loop_stats if stat.error]
    total_avg_duration_result = str(mean(total_durations))
    total_errors_result = len(total_errors)
    results["total average duration"] = total_avg_duration_result
    results["total number of errors"] = total_errors_result
    logging.debug('average duration of total {0}'.format(total_avg_duration_result))
    logging.debug(
        '{0} errors in entire run'.format(total_errors_result))
    logging.debug(results)
    with open('{0}.json'.format('breaker_number_of_builds_' + str(number_of_builds)), 'w') as fp:
        json.dump(results, fp)


def log_iteration_results(iteration_stats, j, main_loop_start, total_threads, number_of_builds):
    main_loop_end = time.time()
    main_loop_elapsed = main_loop_end - main_loop_start
    logging.debug('~~~~~ Iteration {0} Average ~~~~~'.format(j))
    logging.debug('{0} of threads'.format(number_of_builds))
    logging.debug('Iteration duration: {0}'.format(main_loop_elapsed))
    iteration_durations = [stat.duration for stat in iteration_stats]
    iteration_errors = [stat.error for stat in iteration_stats if stat.error]
    avg_duration_iteration_result = str(mean(iteration_durations))
    errors_in_iteration_result = len(iteration_errors)
    results["Iteration {0}".format(j)] = {
        "average_duration": avg_duration_iteration_result,
        "errors_in_iteration": errors_in_iteration_result,
        "durations": iteration_durations,
        "total_iteration_duration": str(main_loop_elapsed),
        "total threads": total_threads
    }
    logging.debug('average duration of iteration {0}'.format(avg_duration_iteration_result))
    logging.debug('{0} errors in iteration'.format(errors_in_iteration_result))


def cleanup_iteration(errors_in_iteration):
    for o in xrange(5):
        try:
            cleanup()
            break
        except Exception as e:
            print e
    del average_reserve_duration_inside_iteration[:]
    del errors_in_iteration[:]

if __name__=='__main__':
    for itera in NUMBER_OF_BUILDS_MULTIPLE_EXECUTIONS:
        NUMBER_OF_BUILDS = itera
        main(ReserverEnder)
