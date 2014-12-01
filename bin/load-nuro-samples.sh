#
# Copyright 2014 Atos
# Contact: Atos <roman.sosa@atos.net>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

#
# Sample usage of REST facade.
#
# Usage: $0 <templateid> <appid> <entityid>
#   E.g.: $0 nuro-template b8fFlGVm EjmAYSpg
#
# Use env var SLA_DASHBOARD_URL to set dashboard root url
#
#
if [ "$0" != "bin/load-nuro-samples.sh" ]; then
    echo "Must be executed from project root"
    exit 1
fi

if [ $# -lt 3 ]; then
        echo "Usage: $0 <templateid> <appid> <entityid>"
        exit 1
fi

SLA_DASHBOARD_URL=${SLA_DASHBOARD_URL:-http://localhost:8000}

JSON="{\"templateid\": \"$1\", \"consumerid\": \"random-client\", \"appid\": \"$2\", \"moduleid\": \"$3\"}"

# generate and store agreement
curl -v "$SLA_DASHBOARD_URL/slagui/rest/agreements" -X POST -d"$JSON" -H"Content-type: application/json"

# start enforcement
curl -v "$SLA_DASHBOARD_URL/slagui/rest/enforcements/$2" -X PUT
