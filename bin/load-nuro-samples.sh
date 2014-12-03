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
# Usage: $0 <templateid> <consumerid> <appid> <entityid>
#   E.g.: 
#       $0 nuro-template random-client b8fFlGVm EjmAYSpg
#       $0 nuro-template-cloud nuro b8fFlGVm EjmAYSpg
#
# Use env var SLA_DASHBOARD_URL to set dashboard root url
#
#
if [ "$0" != "bin/load-nuro-samples.sh" ]; then
    echo "Must be executed from project root"
    exit 1
fi

if [ $# -lt 4 ]; then
        echo "Usage: $0 <templateid> <consumerid> <appid> <entityid>"
        exit 1
fi

function get_json_attr() {
    local result

    JSON=$1
    ATTR=$2
    result=$(echo "$JSON" | python -c "import json,sys;obj=json.load(sys.stdin); print obj['$ATTR'];")
    echo "$result"
}

function do_agreement() {
    # $1: templateid
    # $2: consumerid
    # $3: appid
    # $4: moduleid

    JSON="{\"templateid\": \"$1\", \"consumerid\": \"$2\", \"appid\": \"$3\", \"moduleid\": \"$4\"}"

    # generate and store agreement
    out=$(curl "$SLA_DASHBOARD_URL/slagui/rest/agreements" -X POST -d"$JSON" -H"Content-type: application/json")

    agreement_id=$(get_json_attr "$out" "id")
    # start enforcement
    curl "$SLA_DASHBOARD_URL/slagui/rest/enforcements/$agreement_id" -X PUT
}

SLA_DASHBOARD_URL=${SLA_DASHBOARD_URL:-http://localhost:8000}

do_agreement "$1" "$2" "$3" "$4"
