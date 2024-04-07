import salt.cloud

from st2common.runners.base_action import Action


class SaltInstaller(Action):
    def run(self, name, provider, instance_id):
        client = salt.cloud.CloudClient("/etc/salt/cloud")
        ret = client.create(names=[name], provider=provider, instance_id=instance_id)
        return ret
