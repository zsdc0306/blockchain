import time

tb0=1509740483L;

def gettime_ntp(addr='time.nist.gov'):
    # http://code.activestate.com/recipes/117211-simple-very-sntp-client/
    import socket
    import struct
    import sys
    import time
    TIME1970 = 2208988800L      # Thanks to F.Lundh
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = '\x1b' + 47 * '\0'
    client.sendto( data, (addr, 123))
    data, address = client.recvfrom( 1024 )
    if data:
        t = struct.unpack( '!12I', data )[10]
        t -= TIME1970
        return time.ctime(t),t


#get current time anc calculate the block that needs to produce at the given time
def whoseturn(no_of_producers):
    timeslot = 3;  # AFTER 3 Seconds change producer
    currtime=gettime_ntp()[1]
    totalslots= (currtime-tb0)/timeslot;
    #print producers[totalslots%no_of_producers],currtime
    return totalslots % no_of_producers

print gettime_ntp()