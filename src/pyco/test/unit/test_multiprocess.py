'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import logging
from pyco.device import device

#from IPython.parallel import Client
from multiprocessing import Pool

from pyco import log
from utils import setface


TELNET_PORT = 7777

# create logger
log = log.getLogger("test")


def cioscoios_show_ip_local_pool(host):
    out = host.send("show ip local pool")
    return out


def command(host):
    try:
        print("----> [%s]" % host.driver)
        if (host.driver.name == "ciscoios"):
            return cioscoios_show_ip_local_pool(host)
        elif(host.driver.name == 'juniper'):
            print("Thommy lets happen!")
        else:
            print("unknown device type %s" % host.driver)
    except Exception:
        #print("%s: interrogazione fallita, vedere file di log per i dettagli" % host.name)
        #traceback.print_exc(file=sys.stdout)
        logging.exception("interrogazione fallita")
    finally:
        pass


class Test(unittest.TestCase):
    
    #@unittest.skip("skipping")
    def testMulti(self):
        log.debug("testMulti ...")
        setface("ciscoios")
        
        h = device('telnet://%s:%s@%s:%d/ciscoios' % 
                   ('obi-wan-kenobi', 'secret', 'localhost',TELNET_PORT))
        h.maxWait = 2
        
        #p = Client()[:]
        
        hosts = [h] * 10
        
        with Pool(5) as p:
            results = p.map(command, hosts)
            self.assertEqual(len(results), 10, "expected 10 command outputs")
            self.assertNotIn(None, results, "some commands failed unexpectely")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()