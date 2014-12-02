
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from slagui.generator import AgreementGenerator
from slagui.generator import AgreementParams
from slaclient import restclient

factory = restclient.Factory(settings.SLA_MANAGER_URL)


@api_view(['POST'])
def agreements(request):
    """Simple generation of an agreement from a template.

    The request body is a json document like:
    { "templateid": $id, "consumer": $consumer,
      "appid": $appid, "moduleid": $moduleid }

    , where:
       $id is the TemplateId of an existing template,
       $consumer is the desired agreement client,
       $appid is the brooklyn application id,
       $moduleid is the php module brooklyn id.

    This implementation needs an existing template with the following
    constraints (see slagui/testing/template-generator.xml for an example):
    * it has an AgreementId attribute in root element with the following
      value: ${application}
    * the string ${consumer} is substituted by $consumer
    * the string ${templateid} is substituted by $id
    * the string ${application} is substituted by $appid
    * the string ${entity} is substituted by $moduleid
    """
    if request.method == "POST":
        #expected input:
        # { "templateid": $id, "consumer": $consumer,
        #   "appid": $appid, "moduleid": $moduleid }
        try:
            params = _parse_input(request.body)
        except ValueError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                content_type="text/plain",
                data=e.message
            )

        templateclient = factory.templates()
        template, response = templateclient.getbyid(params.templateid)
        rawtemplate = response.text

        generator = AgreementGenerator(rawtemplate, params)
        rawagreement, agreement_id = generator.do()

        agreementclient = factory.agreements()
        agreementclient.create(rawagreement)

        result = dict(id=agreement_id)
        return Response(data=result, content_type="text/plain")
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
def enforcements(request, agreement_id):
        jobsclient = factory.enforcements()
        r = jobsclient.start(agreement_id)
        return Response(data=r.text, content_type="text/plain")


def _parse_input(jsondata):
    """Parse jsondata into a dict. Raise ValueError if any field is lacking"""
    d = json.loads(jsondata)
    return AgreementParams(
        templateid=d.get("templateid"),
        consumerid=d.get("consumerid"),
        appid=d.get("appid"),
        moduleid=d.get("moduleid")
    )


