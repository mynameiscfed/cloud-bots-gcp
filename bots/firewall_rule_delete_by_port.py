from googleapiclient import discovery
from googleapiclient.errors import HttpError, Error
from oauth2client.client import GoogleCredentials
from pprint import pprint

fw_port_check = 3389
fw_destination_check_cidr = '0.0.0.0/0'

def run_action(project_id, rule, entity, params):
    gcp_credentials = GoogleCredentials.get_application_default()
    gcp_service = discovery.build('compute', 'v1', credentials=gcp_credentials)
    gcp_project_id = entity.get('accountNumber')
    
    fw_destination_port_to_delete, fw_destination_scope_to_delete = params
    print(f'{__file__} - run_action started')
    fw_rules = entity.get('inboundRules')

    try:
      for r in fw_rules:
          fw_source = r.get('source')
          fw_destination = r.get('destination')
          fw_protocol = r.get('protocol')
          fw_action = r.get('action')
          fw_destination_port = r.get('destinationPort')
          fw_destination_port_to = r.get('destinationPortTo')
          fw_direction = r.get('direction')
          fw_rule_name = r.get('name')
          if (fw_destination_port == fw_port_check and fw_destination_check_cidr == fw_destination):
              fw_rule_to_delete = fw_rule_name
              print(f'Match found on rule name : {fw_rule_to_delete}')
              print(f'Deleting rule : {fw_rule_to_delete}')
              request = gcp_service.firewalls().delete(project=gcp_project_id, firewall=fw_rule_to_delete)
              response = request.execute()
              pprint(response)
    except (HttpError, Error) as e:
      print(f'An error occured : {e}')
