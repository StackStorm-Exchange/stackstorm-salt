import json
from requests import Session

from lib.base import SaltAction


class SaltLocal(SaltAction):
    __explicit__ = [
        'cmdmod',
        'event',
        'file',
        'grains',
        'pillar',
        'pkg',
        'saltcloudmod',
        'schedule',
        'service',
        'state',
        'status'
    ]

    def run(self, module, target, tgt_type, args, **kwargs):
        self.verify_ssl = self.config.get('verify_ssl', True)
        '''
        CLI Examples:

            st2 run salt.local module=test.ping matches='web*'
            st2 run salt.local module=test.ping tgt_type=grain target='os:Ubuntu'
        '''

        # ChatOps alias and newer ST2 versions set default args=[]
        # This breaks test.ping & test.version

        if module not in ['test.ping', 'test.version']:
            self.generate_package('local',
                                  cmd=module,
                                  target=target,
                                  tgt_type=tgt_type,
                                  args=args,
                                  data=kwargs)
        else:
            self.generate_package('local',
                                  cmd=module,
                                  target=target,
                                  tgt_type=tgt_type,
                                  args=None,
                                  data=kwargs)

        request = self.generate_request()
        self.logger.info('[salt] Request generated')
        request.prepare_body(json.dumps(self.data), None)
        self.logger.info('[salt] Preparing to send')
        resp = Session().send(request, verify=self.verify_ssl)
        return resp.json()
