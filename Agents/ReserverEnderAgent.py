from time import sleep

from cloudshell.api.cloudshell_api import CloudShellAPISession

from agent import Agent


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


