'''

@author: frank
'''
import sys, os, os.path
import cephagent
from zstacklib.utils import log
from zstacklib.utils import linux
import zstacklib.utils.iptables as iptables

pidfile = '/var/run/zstack/ceph-backupstorage-agent.pid'
log.configure_log('/var/log/zstack/ceph-backupstorage-agent.log')
logger = log.get_logger(__name__)

def prepare_pid_dir(path):
    pdir = os.path.dirname(path)
    if not os.path.isdir(pdir):
        os.makedirs(pdir)
    
def main():
    usage = 'usage: python -c "from cephbackupstorage import cdaemon; cdaemon.main()" start|stop|restart'
    if len(sys.argv) != 2 or not sys.argv[1] in ['start', 'stop', 'restart']:
        print usage
        sys.exit(1)
    
    global pidfile
    prepare_pid_dir(pidfile)

    try:
        iptc = iptables.from_iptables_save()
        iptc.add_rule('-A INPUT -p tcp -m tcp --dport 7761 -j ACCEPT')
        iptc.iptable_restore()

        cmd = sys.argv[1]
        agentdaemon = cephagent.CephDaemon(pidfile)
        if cmd == 'start':
            logger.debug('zstack-ceph-backupstorage starts')
            agentdaemon.start()
        elif cmd == 'stop':
            logger.debug('zstack-ceph-backupstorage stops')
            agentdaemon.stop()
        elif cmd == 'restart':
            logger.debug('zstack-ceph-backupstorage restarts')
            agentdaemon.restart()
        sys.exit(0)    
    except Exception:
        logger.warning(linux.get_exception_stacktrace())
        sys.exit(1)
    
    
if __name__ == '__main__':
    main()
