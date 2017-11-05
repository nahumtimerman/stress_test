import threading
import time
import logging
from cloudshell.api.cloudshell_api import *
import json
import argparse

parser = argparse.ArgumentParser()

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s', )

NUMBER_OF_BUILDS = 15
MAIN_LOOP = 5

users = ['admin' for i in xrange(NUMBER_OF_BUILDS)]
domain = ['SSP SJC' for i in xrange(NUMBER_OF_BUILDS)]
duts = ['[Any]' for i in xrange(NUMBER_OF_BUILDS)]
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

def worker(num, statistics):
    """thread worker function"""
    logging.debug('Worker: %s started' % num)
    api = CloudShellAPISession(host, users[0], password, domain[0])
    GetReserveEndCycle(api, topology, num, statistics)
    logging.debug('Worker: %s ended' % num)
    return


def GetReserveEndCycle(api, topology, num,statistics):
    reservation = ReserveTopology(api, topology, num, statistics)
    if not reservation:
        logging.debug('Failed to reserve')

    return statistics


def ReserveTopology(api, topology, num, statistics):
    input_requirements = []
    input_requirements.append(UpdateTopologyRequirementsInputsRequest('UUT1', 'Serial Number', duts[0], 'Attributes'))
    now = time.time()
    logging.debug('Topology begin reserved ' + str(now))
    try:
        out = api.CreateImmediateTopologyReservation(reservationName='Performance',
                                                     owner='admin',
                                                     durationInMinutes='60',
                                                     notifyOnStart=True,
                                                     notifyOnEnd=True,
                                                     notificationMinutesBeforeEnd='15',
                                                     topologyFullPath=topology,
                                                     globalInputs=global_input,
                                                     requirementsInputs=input_requirements)
    except Exception as e:
        thread_num = 'Thread ' + str(num)
        statistics.error = thread_num
        print e.message
        return None

    after = time.time()
    elapsed = after - now
    statistics.duration = elapsed

    logging.debug('Topology begin reserved ' + str(after))
    logging.debug('Elapsed ' + str(elapsed))

    return out.Reservation


def mean(l):
    a = sum(l) / float(len(l))
    return a


def cleanup():
    api = CloudShellAPISession(host, 'admin', password, 'Global')
    active_reservations = api.GetCurrentReservations('admin').Reservations
    for r in active_reservations:
        if ('Performance_' in r.Name):
            try:
                api.EndReservation(r.Id)
            except:
                pass
            try:
                api.TerminateReservation(r.Id)
            except:
                pass


def main():
    api = CloudShellAPISession(host, 'admin', password, 'Global')
    active_reservations = api.GetCurrentReservations('').Reservations
    logging.debug('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nStarting test\n~~~~~~~~~~~~~~~~~~~~~~~')
    logging.debug('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{0}\n~~~~~~~~~~~~~~~~~~~~~~~'.format(len(active_reservations)))

    results["number of threads"] = NUMBER_OF_BUILDS
    results["main loop"] = MAIN_LOOP

    main_loop_stats =[]

    for j in xrange(MAIN_LOOP):
        logging.debug('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nLoop {0}\n~~~~~~~~~~~~~~~~~~~~~~~'.format(j))
        main_loop_start = time.time()
        threads = []

        errors_in_iteration = []
        iteration_stats = []

        for i in range(NUMBER_OF_BUILDS):
            thread_stats = Statistics()
            t = threading.Thread(target=worker, args=(i, thread_stats))
            threads.append(t)
            t.start()
            iteration_stats.append(thread_stats)
            main_loop_stats.append(thread_stats)

        [t.join() for t in threads]

        logging.debug('~~~~~ Iteration {0} Average ~~~~~'.format(j))
        logging.debug('{0} of threads'.format(NUMBER_OF_BUILDS))
        iteration_durations = [stat.duration for stat in iteration_stats]
        iteration_errors = [stat.error for stat in iteration_stats if stat.error]
        avg_duration_iteration_result = str(mean(iteration_durations))
        errors_in_iteration_result = len(iteration_errors)

        main_loop_end = time.time()
        main_loop_elapsed = main_loop_end - main_loop_start

        results["Iteration {0}".format(j)] = {
            "average_duration": avg_duration_iteration_result,
            "errors_in_iteration": errors_in_iteration_result,
            "durations": iteration_durations,
            "total_iteration_duration": str(main_loop_elapsed)
        }

        logging.debug('average duration of iteration {0}'.format(avg_duration_iteration_result))
        logging.debug(
            '{0} errors in iteration'.format(errors_in_iteration_result))
        for o in xrange(5):
            try:
                cleanup()
                break
            except Exception as e:
                print e
        del average_reserve_duration_inside_iteration[:]
        del errors_in_iteration[:]



    logging.debug('####### TOTAL AVERAGE ######')
    logging.debug('{0} of threads'.format(NUMBER_OF_BUILDS))
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

    with open('{0}.json'.format('number_of_builds_' + str(NUMBER_OF_BUILDS)), 'w') as fp:
        json.dump(results, fp)

number_of_iterations = [10, 15, 30, 50, 100]
for itera in number_of_iterations:
    NUMBER_OF_BUILDS = itera
    main()
