from cloudshell.api.cloudshell_api import *

def cleanup():
    api = CloudShellAPISession('localhost', 'admin', 'a', 'Global')
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

cleanup()

