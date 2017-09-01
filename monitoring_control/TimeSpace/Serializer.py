import traceback
from django.views.generic import View
from TimeSpace.models import Host


class ClientHandler(View):

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.client_configs = {
            "services": {}
        }

    def fetch_configs(self):
        try:
            try:
                host_obj = Host.objects.get(ip_addr=self.client_ip)
                template_list = list(host_obj.templates.select_related())
                host_group_obj = host_obj.host_groups.select_related()
                print(host_group_obj)
                template_list.extend([template for template in host_group_obj])
                for template in template_list:
                    for service in template.services.select_related():
                        self.client_configs['services'][service.name] = [service.plugin_name, service.interval]
            except Exception as e:
                print(u"没有这个客户端!")
        except:
            traceback.print_exc()
        return self.client_configs