import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
#uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E704')
#uri = uri_helper.uri_from_env(default='usb://0')
uri = 'usb://0'
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
cflib.crtp.init_drivers(enable_debug_driver=False)

class TWR_ranging():
    def __init__(self):
        self.lg_twr = LogConfig(name='twr', period_in_ms=50)
        self.lg_twr.add_variable('ranging.distance0', 'float')
        self.lg_twr.add_variable('ranging.distance1', 'float')
        self.lg_twr.add_variable('ranging.distance2', 'float')
        self.lg_twr.data_received_cb.add_callback(self.twr_log)
        self.scf = SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache'))
        self.scf.open_link()
        self.scf.cf.log.add_config(self.lg_twr)
        self.lg_twr.start()
        self.ranging0 =None
        self.ranging1 =None
        self.ranging2 =None
    def stop(self):
        self.lg_twr.stop()
        
    def twr_log(self, timestamp, data, logconf):
        self.ranging0 = data['ranging.distance0']
        self.ranging1 = data['ranging.distance1']
        self.ranging2 = data['ranging.distance2'] 
        print('[%d][%s]: %s' % (timestamp, logconf, data))
        
    def get(self):
        if self.ranging0 != None:
            distance0 = self.ranging0
            distance1 = self.ranging1
            distance2 = self.ranging2
            return distance0, distance1, distance2
        else:
            return None, None, None
    	
        
     
        
        
      

if __name__ == '__main__':
    twr_ranging = TWR_ranging()
    #distance0, distance1, distance2 = twr_ranging.get()



