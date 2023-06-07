import ntplib
from datetime import datetime, timezone
from time import ctime


def sync_with_ntp(ntp_server):
    try:
        client = ntplib.NTPClient()
        response = client.request(ntp_server)
        response.offset
        delay = response.delay
        current_time = ctime(response.tx_time)
        print(f'Good {ntp_server}')
        #print(f'Current time {datetime.fromtimestamp(response.tx_time, timezone.utc)}')
        print(f'Delay {delay}')
    except Exception as e:
        print(f'Bad {str(e)}')
    return float(delay)

ntp_server = 'ntp7.ntp-servers.net'
sync_with_ntp(ntp_server)
