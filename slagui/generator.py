
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid


class AgreementParams(object):

    def __init__(self, templateid, consumerid, appid, moduleid,
                 expirationtime=None):
        self.templateid = templateid
        self.consumerid = consumerid
        self.appid = appid
        self.moduleid = moduleid

        self.expirationtime = expirationtime if expirationtime is not None \
            else AgreementParams._formatdate(datetime.now())

        self._check_param("templateid", templateid)
        self._check_param("consumerid", consumerid)
        self._check_param("appid", appid)
        self._check_param("moduleid", moduleid)

    def _check_param(self, variable, value):
        if value is None or value == "":
            raise ValueError("{} is empty".format(variable))

    @staticmethod
    def _formatdate(date_):
        # reset microseconds
        t = date_.replace(microsecond=0)
        t = t + relativedelta(years=1)
        return t.isoformat() + "+0000"


class AgreementGenerator(object):
    def __init__(self, template, parameters):
        """Generates an agreement from a template

        :param str template:
        :param generator.AgreementParams parameters:
        """
        self.template = template
        self.parameters = parameters

    def do(self):
        tpl = self.template
        params = self.parameters

        templateid_attr = 'wsag:TemplateId="{}"'.format(params.templateid)
        agreement_id = str(uuid.uuid4())
        agreementid_attr = 'wsag:AgreementId="{}"'.format(agreement_id)
        agreement = tpl\
            .replace("<wsag:Template ", "<wsag:Agreement ")\
            .replace(templateid_attr, agreementid_attr)\
            .replace("${application}", params.appid)\
            .replace("${consumer}", params.consumerid)\
            .replace("${templateid}", params.templateid)\
            .replace("${entity}", params.moduleid)\
            .replace("</wsag:Template>", "</wsag:Agreement>")
            #.replace("${expirationtime}", params.expirationtime)\

        return agreement, agreement_id