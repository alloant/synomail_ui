from synology_drive_api.utils import form_urlencoded


class CalendarMixin:

    def create_task(self, cal_id, summary):
        """
        :param task_id:
        get task status
        :return:
        """
        api_name = 'SYNO.Cal.Todo'
        endpoint = 'entry.cgi'
        data = {
            'cal_id': cal_id,
            'original_cal_id': cal_id,
            'summary': summary,
            'is_repeat_evt': False,
            'is_todo': True,
            'tz_id': 'null',
            'evt_notify_setting': [],
            'api': api_name,
            'method': 'create',
            'version': 1
        }
        urlencoded_data = form_urlencoded(data)
        resp = self.session.http_post(endpoint, data=urlencoded_data)
        return resp

    def create_task_2(self, user, summary):
        """
        :param task_id:
        get task status
        :return:
        """
        api_name = 'SYNO.Cal.Todo'
        endpoint = 'entry.cgi'
        params = {
            'cal_id': f"/{user}/home_todo",
            'original_cal_id': f"/{user}/home_todo",
            'summary': summary,
            'is_repeat_evt': False,
            'is_todo': True,
            'from_syno_app_url': [{"app":"SYNO.SDS.Chat.Application"}],
            'tz_id': 'null',
            'evt_notify_setting': [],
            'api': api_name,
            'method': 'create',
            'version': 1
        }
        urlencoded_data = form_urlencoded(params)
        resp = self.session.http_post(endpoint, data=urlencoded_data)
        #resp = self.session.http_get(endpoint,params=params)
        return resp

