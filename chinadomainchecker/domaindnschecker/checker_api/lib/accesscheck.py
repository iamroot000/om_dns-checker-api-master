import requests, time, os, ipaddress, subprocess

class CheckDomain():
    def _resolveip(self, mydomain):
        out_list = []
        _domain = mydomain.replace('https://', '').replace('http://', '').strip()
        _dns = "180.76.76.76"
        _out = os.popen("nslookup {} {}".format(_domain, _dns))
        for i in _out.read().split('\n'):
            if len(i) != 0:
                out_list.append(i)

        try:
            nsnum = -1
            myip = ipaddress.ip_address(unicode(out_list[nsnum].split('Address:')[-1].strip()))
            while True:
                if len(str(myip).split(':')) > 1:
                    nsnum = nsnum - 2
                    myip = ipaddress.ip_address(unicode(out_list[nsnum].split('Address:')[-1].strip()))
                    print("IP is {} = Lookup is ipv6 = Element number {}".format(myip,nsnum))
                else:
                    print("IP is {} = Lookup is ipv4 = Element number {}".format(myip,nsnum))
                    return myip
        except Exception as e:
            return None


    def domcheck(self, domain):
        try:
            _result = requests.get(domain, timeout=15, allow_redirects=False)
            print("Domain {} is ACCESSIBLE.".format(domain))
            return {"dom_status": 0}
        except Exception as e:
            print("Domain {} is INACCESSIBLE. ERROR: {}".format(domain, str(e)))
            for i in range(0,3):
                time.sleep(10)
                try:
                    _result = requests.get(domain, timeout=15, allow_redirects=False)
                    print("try {}: Domain {} is ACCESSIBLE.".format(int(i + 1), domain))
                    return {"dom_status": 0}
                except Exception as e:
                    url = domain
                    _nsresult = self._resolveip(url)
                    if _nsresult == None or _nsresult == "None":
                        print("{} try ========= {}".format(i, str("Unable to resolve IP of {}".format(url))))
                    else:
                        args = ["curl", "--resolve",
                                "{}:443:{}".format(url.replace('https://', '').replace('http://', '').strip(),
                                                   _nsresult), "-I", url, "--max-time", "15"]
                        child = subprocess.Popen(args, stdout=subprocess.PIPE)
                        streamdata = child.communicate()[0]
                        rc = child.returncode
                        if int(rc) != 0:
                            print(args)
                            print("{} try ========= Cant connect to {} using curl".format(i, url))
                        else:
                            print(args)
                            print("{} try ========= Connected to {} using curl".format(i, url))
                            return {"dom_status": 0}
                    print("try {}: Domain {} is INACCESSIBLE. ERROR: {}".format(int(i + 1), domain, str(e)))
            return {"dom_status": 1}



if __name__ == '__main__':
    # print(CheckDomain().domcheck('https://baidu.com'))
    print(CheckDomain().domcheck('https://kingbally.com'))
    #print(CheckDomain().domcheck('https://dl.365kqzs.cn'))


