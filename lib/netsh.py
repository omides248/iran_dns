import re
import subprocess


class Netsh:

    # @classmethod
    # def set_dns_one_command(cls, interface=None, primary_dns=None, secondary_dns=None):
    #     if not interface:
    #         interface = cls.get_default_interface_name()
    #     command = f'netsh interface ipv4 set dnsservers name="{interface}" source=dhcp && ' \
    #               f'netsh interface ipv4 set dns name="{interface}" static {primary_dns} && ' \
    #               f'netsh interface ipv4 add dns name="{interface}" {secondary_dns} index=2'
    #
    #     proc = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @classmethod
    def set_dns(cls, interface=None, primary_dns=None, secondary_dns=None):

        if not interface:
            interface = cls.get_default_interface_name()

        if interface and primary_dns and secondary_dns:
            # cls.clear_dns()
            # os.system(f'netsh interface ipv4 set dns name="{interface}" static {primary_dns}')
            # os.system(f'netsh interface ipv4 add dns name="{interface}" {secondary_dns} index=2')
            subprocess.Popen(f'netsh interface ipv4 set dns name="{interface}" static {primary_dns}',
                             shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.Popen(f'netsh interface ipv4 add dns name="{interface}" {secondary_dns} index=2',
                             shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @classmethod
    def clear_dns(cls, interface=None):

        if not interface:
            interface = cls.get_default_interface_name()

        if interface:
            subprocess.Popen(f'netsh interface ipv4 set dnsservers name="{interface}" source=dhcp', shell=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @classmethod
    def get_primary_secondary_dns(cls, interface=None):
        primary_dns = ""
        secondary_dns = ""
        if not interface:
            interface = cls.get_default_interface_name()

        if interface:
            output = subprocess.Popen(f'netsh interface ipv4 show dnsservers name="{interface}"',
                                      stdout=subprocess.PIPE,
                                      encoding="utf-8",
                                      shell=True).stdout.read()
            v = cls.list_split(output, split_value="\n")
            if len(v) > 2:
                if v[2].startswith("Statically Configured DNS Servers:"):
                    _, primary_dns = cls.list_split(v[2], ":")
                    if primary_dns is None or primary_dns == "None":
                        primary_dns = ""
                    secondary_dns = v[3].strip()
                    if secondary_dns is None or secondary_dns == "None":
                        secondary_dns = ""

                    if secondary_dns.startswith("Register with which suffix:"):
                        secondary_dns = ""

        return primary_dns, secondary_dns

    @classmethod
    def get_default_interface_name(cls):
        try:
            output = subprocess.Popen('netsh interface ipv4 show addresses', stdout=subprocess.PIPE,
                                      shell=True, encoding="utf-8").stdout.read()
            interface_list = []
            interface_default_gateway_list = []
            items = output.split('\n\n')
            for i in items:
                i = i.strip()
                interface_i = i.split("\n")
                if len(interface_i) > 1:
                    interface_list.append(interface_i)

            for i in interface_list:
                interface_name = None
                default_gateway = None
                interface_metric = None
                for item in i:
                    if "Configuration for interface" in item:
                        interface_name = item.replace("Configuration for interface", "").replace("\"", "").strip()
                    elif "Default Gateway:" in item:
                        _, default_gateway = item.replace(" ", "").strip().split(":")

                    elif "InterfaceMetric:" in item:
                        _, interface_metric = item.replace(" ", "").strip().split(":")

                    if interface_name and default_gateway and interface_metric:
                        interface_default_gateway_list.append({"interface_name": interface_name,
                                                               "default_gateway": default_gateway,
                                                               "interface_metric": interface_metric})
            interface_default_gateway_list = sorted(interface_default_gateway_list, key=lambda d: d['interface_metric'],
                                                    reverse=True)
            if len(interface_default_gateway_list) > 0:
                return interface_default_gateway_list[0].get("interface_name")
            return ""
        except Exception as e:
            print(e)
            return ""

    @classmethod
    def get_all_interface_name(cls):
        interfaces_name = []
        try:
            output = subprocess.Popen('netsh interface show interface', stdout=subprocess.PIPE,
                                      encoding='Utf-8', shell=True).stdout.read()
            items = output.split('\n')
            for i in items[3:]:
                i = re.sub(r'\s\s+', '\t', i)
                if i:
                    interfaces_name.append(i.split('\t')[-1].strip())
            return sorted(interfaces_name, reverse=True)
        except Exception as e:
            print(e)
            return interfaces_name

    @classmethod
    def list_split(cls, string_separate=None, split_value=None):
        if string_separate and split_value:
            return list(map(str.strip, string_separate.split(split_value)))
        return []
