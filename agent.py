import logging
from time import sleep, time
import random

from cloudshell.api.cloudshell_api import CloudShellAPISession, UpdateTopologyRequirementsInputsRequest

# from breaker import host, users, password, domain, topology, duts, global_input


class Agent(object):
    RESERVATION_DETAILS_BASE_SLEEP = 3

    def __init__(self, duts, global_inputs):
        self.random = random.Random()
        self.global_inputs =global_inputs
        self.duts = duts
        self.reservations = []

    class __metaclass__(type):
        def __iter__(self):
            for attr in dir(Agent):
                if not attr.startswith("__"):
                    yield attr

    def worker(self, num, statistics):
        """thread worker function"""
        logging.debug('Worker {0}: {1} started'.format(self.__class__.__name__, num))
        self.doing_stuff(num, statistics)
        logging.debug('Worker {0}: {1} ended'.format(self.__class__.__name__, num))
        return

    def doing_stuff(self, num, statistics):
        pass

    def reserve_topology(self, api, topology, num, statistics):
        input_requirements = []
        input_requirements.append(UpdateTopologyRequirementsInputsRequest('UUT1', 'Serial Number', self.duts[0], 'Attributes'))
        now = time()
        logging.debug('Topology begin reserved ' + str(now))
        try:
            out = api.CreateImmediateTopologyReservation(reservationName='Performance',
                                                         owner='admin',
                                                         durationInMinutes='60',
                                                         notifyOnStart=True,
                                                         notifyOnEnd=True,
                                                         notificationMinutesBeforeEnd='15',
                                                         topologyFullPath=topology,
                                                         globalInputs=self.global_inputs,
                                                         requirementsInputs=input_requirements)
            self.reservations.append(out.Reservation)

        except Exception as e:
            thread_num = 'Thread ' + str(num)
            statistics.error = thread_num
            print e.message
            return None

        after = time()
        elapsed = after - now
        statistics.duration = elapsed

        logging.debug('Topology begin reserved ' + str(after))
        logging.debug('Elapsed ' + str(elapsed))

        if not out and not out.reservation:
            logging.debug('Failed to reserve')

        return statistics

    def end_my_reservations(self, api, num, statistics):
        try:
            for reservation in self.reservations:
                api.EndReservation(reservation.Id)
        except Exception as e:
            thread_num = 'Thread ' + str(num)
            statistics.error = thread_num
            print e.message
            return

    def check_reservation_status(self, api, num, statistics):
        if len(self.reservations) == 0:
            return

        reservation_id = self.reservations[0].Id
        try:
            status = api.GetReservationDetails(reservation_id)

            tries = 0
            while tries < 10 and status == api.GetReservationDetails(reservation_id):
                self._random_sleep(self.RESERVATION_DETAILS_BASE_SLEEP)
                tries += 1
        except Exception as e:
            thread_num = 'Thread ' + str(num)
            statistics.error = thread_num
            print e.message
            return

    def check_only_reservation_status(self, api, num, statistics):
        if len(self.reservations) == 0:
            return

        reservation_id = self.reservations[0].Id
        try:
            status = api.GetReservationStatus(reservation_id).ReservationSlimStatus.ProvisionigStatus

            tries = 0
            max_tries = random.randint(3, 10)
            while tries < max_tries \
                    and status == api.GetReservationStatus(reservation_id).ReservationSlimStatus.ProvisionigStatus:
                sleep(self.RESERVATION_DETAILS_BASE_SLEEP)
                tries += 1
        except Exception as e:
            thread_num = 'Thread ' + str(num)
            statistics.error = thread_num
            print e.message
            return

    def single_get_reservation(self, api, num, statistics):
        if len(self.reservations) == 0:
            return

        reservation_id = self.reservations[0].Id
        try:
            status = api.GetReservationDetails(reservation_id)

        except Exception as e:
            thread_num = 'Thread ' + str(num)
            statistics.error = thread_num
            print e.message
            return

    def _random_sleep(self, sleep_time):
        some_element_of_chance = self.random.randint(10, 100) / 100
        sleep(some_element_of_chance * sleep_time)

    def random_sleep(self):
        sleep_time = self.random.randint(0, 1)
        self._random_sleep(sleep_time)


class ReserverGetter(Agent):
    def __init__(self, host, username, password, domain, topology):
        global_input = []
        duts = ['[Any]']
        super(ReserverGetter, self).__init__(duts, global_input)
        self.topology = topology
        self.domain = domain
        self.password = password
        self.host = host
        self.username = username

    def doing_stuff(self, num, statistics):
        self.random_sleep()
        api = CloudShellAPISession(self.host, self.username, self.password, self.domain)
        # self.random_sleep()
        self.reserve_topology(api, self.topology, num, statistics)
        # self.random_sleep()
        self.check_reservation_status(api, num, statistics)
        # self.random_sleep()
        # self.end_my_reservations(api, num, statistics)

class ReserverGetterOnlyStatus(Agent):
    def __init__(self, host, username, password, domain, topology):
        global_input = []
        duts = ['[Any]']
        super(ReserverGetterOnlyStatus, self).__init__(duts, global_input)
        self.topology = topology
        self.domain = domain
        self.password = password
        self.host = host
        self.username = username

    def doing_stuff(self, num, statistics):
        self.random_sleep()
        api = CloudShellAPISession(self.host, self.username, self.password, self.domain)
        # self.random_sleep()
        self.reserve_topology(api, self.topology, num, statistics)
        sleep(5)
        self.check_only_reservation_status(api, num, statistics)
        # self.random_sleep()
        # self.end_my_reservations(api, num, statistics)


class BenchmarkAgent(Agent):
    def __init__(self, host, username, password, domain, topology):
        global_input = []
        duts = ['[Any]']
        super(BenchmarkAgent, self).__init__(duts, global_input)
        self.topology = topology
        self.domain = domain
        self.password = password
        self.host = host
        self.username = username

    def doing_stuff(self, num, statistics):
        self.random_sleep()
        api = CloudShellAPISession(self.host, self.username, self.password, self.domain)
        self.reserve_topology(api, self.topology, num, statistics)
        self.single_get_reservation(api, num, statistics)
        self.check_only_reservation_status(api, num, statistics)
        self.end_my_reservations(api, num, statistics)

class ReserverSingleGetter(Agent):
    def __init__(self, host, username, password, domain, topology):
        global_input = []
        duts = ['[Any]']
        super(ReserverSingleGetter, self).__init__(duts, global_input)
        self.topology = topology
        self.domain = domain
        self.password = password
        self.host = host
        self.username = username

    def doing_stuff(self, num, statistics):
        self.random_sleep()
        api = CloudShellAPISession(self.host, self.username, self.password, self.domain)
        self.reserve_topology(api, self.topology, num, statistics)
        self.random_sleep()
        self.single_get_reservation(api, num, statistics)


class ReserverEnder(Agent):
    def __init__(self, host, username, password, domain, topology):
        global_input = []
        duts = ['[Any]']
        super(ReserverEnder, self).__init__(duts, global_input)
        self.topology = topology
        self.domain = domain
        self.password = password
        self.host = host
        self.username = username

    def doing_stuff(self, num, statistics):
        self.random_sleep()
        api = CloudShellAPISession(self.host, self.username, self.password, self.domain)
        # self.random_sleep()
        self.reserve_topology(api, self.topology, num, statistics)
        # self.random_sleep()
        sleep(3)
        # self.check_reservation_status(api, num, statistics)
        # self.random_sleep()
        self.end_my_reservations(api, num, statistics)


# agentTypesToNumberOfAgentsToCreate = {ReserverEnder: 25, ReserverSingleGetter: 25}


class AgentFactory(object):
    def __init__(self, agentTypesToNumberOfAgentsToCreate, host, username, password, domain, topology):
        self.domain = domain
        self.password = password
        self.username = username
        self.topology = topology
        self.host = host
        self.agentTypesToNumberOfAgentsToCreate = agentTypesToNumberOfAgentsToCreate
        self.types = [key for key in agentTypesToNumberOfAgentsToCreate]
        self.totalToCreate = sum([value for key, value in agentTypesToNumberOfAgentsToCreate.iteritems()])

    def get_agent(self):
        if self.totalToCreate == 0:
            return Agent()
        type = random.choice(self.types)
        while(self.agentTypesToNumberOfAgentsToCreate and self.agentTypesToNumberOfAgentsToCreate[type]==0):
            self.agentTypesToNumberOfAgentsToCreate.pop(type, None)
            self.types.pop(type)
            type = random.choice(self.types)
        self.agentTypesToNumberOfAgentsToCreate[type] -= 1
        return type(self.host, self.username, self.password, self.domain, self.topology)



