from pkg_resources import resource_filename, resource_string, iter_entry_points #@UnresolvedImport

from pyco.device import loadConfiguration

cfgFile = resource_filename('pyco.test.mock', 'pyco-mock.cfg')
loadConfiguration(cfgFile)