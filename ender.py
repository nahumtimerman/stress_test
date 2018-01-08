from cloudshell.api.cloudshell_api import *

def cleanup():
    api = CloudShellAPISession('localhost', 'admin', 'admin', 'Global')
    active_reservations = api.GetCurrentReservations().Reservations
    for r in active_reservations:
       # if ('Performance' in r.Name):
          try:
             api.EndReservation(r.Id)
             print 'Ending ' + r.Id
          except:
             pass
          try:
             api.TerminateReservation(r.Id)
             print 'Killing ' + r.Id
          except Exception as e:
             print e

cleanup()

