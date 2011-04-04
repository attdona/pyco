

unableToConnectHost =  "128.0.0.1"
loginSuccessfullHost = "127.0.0.1"
targetCommand = "uname -a"

# a host with wrong username/password
fakeLocalhost = {
             'name'    :'localhost', 
             'username':'netcube',
             'password':'netcube'
             }

localhost = {
             'name'    :'localhost', 
             'username':'netbox',
             'password':'netbox'
             }
cisco1  =   {
             'name'    :'163.162.155.61', 
             'username':'cisco',
             'password':'cisco'
             }            
             
asa1 = {
			 'name'    : '163.162.61.21',
			 'username': 'cisco',
			 'password': 'cisco'
}

hop1 = {
            'name'     : '163.162.155.60',
            'username' : 'pyco',
            'password' : 'pyco'
        }


hop2 = {
            'name'     : '163.162.155.90',
            'username' : 'netbox',
            'password' : 'netbox'
        }

# unknown host (ssh command generates No route to host)
hop3 = {
            'name'     : '163.162.155.91',
            'username' : 'netbox',
            'password' : 'netbox'
        }

