from nslookup import Nslookup

import sys, json, pprint, time, random, logging, os, datetime













class nsCheck(object):



    def __init__(self):

        self.app_name = 'checker_api'

        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.my_path = os.path.join(self.BASE_DIR, 'exec')

        self.log_dir = "/var/log/django/{}/".format(self.app_name)

        os.system("mkdir -p /var/log/django/{} 2> /dev/null".format(self.app_name))





    def loggingFile(self, log_debug=None, log_info=None, log_warning=None, log_error=None, log_critical=None):

        # logdir = os.path.join(self.my_path, 'logs/')

        logdir = self.log_dir

        os.popen("find {0} -type f -name '*.log' -mtime +40 -exec rm {1} \;".format(logdir, '{}'))

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

        logging.basicConfig(

            filename='{}{}-{}.log'.format(logdir, self.app_name, datetime.datetime.now().strftime("%Y-%m-%d-%H")),

            format=LOG_FORMAT, level=logging.DEBUG)

        logger = logging.getLogger()

        if log_debug:

            logger.debug(str(log_debug))

        if log_info:

            logger.info(str(log_info))

        if log_warning:

            logger.warning(str(log_warning))

        if log_error:

            logger.error(str(log_error))

        if log_critical:

            logger.critical(str(log_critical))





        """docstring for nsCheck"""

    def get_info(self,domains):

        # dns_server = ["180.76.76.76", "114.114.114.119", "114.114.114.114", "114.114.115.115", "114.114.114.110", "114.114.115.110", "202.46.34.76", "202.46.32.187", "202.46.34.75", "223.5.5.5", "223.6.6.6", "202.46.34.74"]

        dns_server = ["180.76.76.76"]

        count = 0

        self.loggingFile(log_debug="{}".format("#####" * 20))

        self.loggingFile(log_debug="API Check for domain {}".format(domains),

                         log_info=str("Nameserver = {}".format(dns_server)))

        while count <= 100 :

            rancho = [random.choice(dns_server)]

            # time.sleep(3)

            dns_query = Nslookup(dns_servers=rancho)

            ips_record = dns_query.dns_lookup(domains)

            ip = ips_record.answer

            data = {

                    'ip': ip,

                    'nameserver': rancho

            }

            print(str(len(ip)) + " my length")

            print(data)

            time.sleep(3)

            if len(ip) == 0:

                count  = count + 1

                self.loggingFile(log_debug="{}".format("#####" * 20))

                self.loggingFile(log_debug="TRY: {} | API Check NO VALUE for domain {}".format(count, domains), log_warning=str("IP is {} | Nameserver is  {}".format(ip, rancho)))

                print(str(count) + " my count")

            else:

                data = {

                        'ip': ip,

                        'nameserver': rancho

                }

                print(str(count) + " my count")

                print(data)

                self.loggingFile(log_debug="{}".format("#####" * 20))

                self.loggingFile(log_debug="TRY: {} | API Check OK for domain {}".format(count, domains), log_info=str("data = {}".format(data)))

                return data

        return data







if __name__== "__main__":

        domains = 'jiab888.net'

        g = nsCheck()

        print(g.get_info(domains))


