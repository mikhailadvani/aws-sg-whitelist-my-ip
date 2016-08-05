import sys
import json
from boto.ec2 import EC2Connection

group_name = sys.argv[1]
vpc_id = sys.argv[2]

ec2_connection = EC2Connection()

def jsonify_security_group_rules(rules):
    jsonified_rules = []
    for rule in rules:
        jsonified_rule = {}
        jsonified_rule['proto'] = rule.ip_protocol
        jsonified_rule['from_port'] = rule.from_port
        jsonified_rule['to_port'] = rule.to_port
        for grant in rule.grants:
            sg_rule = jsonified_rule
            if 'sg' in str(grant):
                sg_rule['group_name'] = str(grant)
            else:
                sg_rule['cidr_ip'] = str(grant)
            jsonified_rules.append(sg_rule)
    return jsonified_rules

def get_security_group_facts():
    security_group = ec2_connection.get_all_security_groups(filters={'group-name': [group_name], 'vpc_id': vpc_id})

    security_group_details = dict()
    security_group_details["id"] = security_group[0].id
    security_group_details["tag"] = security_group[0].tags
    security_group_details["name"] = security_group[0].name
    security_group_details["description"] = security_group[0].description
    security_group_details["vpc_id"] = security_group[0].vpc_id
    security_group_details["rules"] = jsonify_security_group_rules(security_group[0].rules)
    security_group_details["rules_egress"] = jsonify_security_group_rules(security_group[0].rules_egress)

    return json.dumps(security_group_details)

print get_security_group_facts()