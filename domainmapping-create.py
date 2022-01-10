import googleapiclient.discovery
import httplib2
from google.api_core.client_options import ClientOptions
import pprint



# Message data
json_payload = {
    'apiVersion': 'domains.cloudrun.com/v1',
    'kind': 'DomainMapping',
    'metadata': {
        'name': 'hello.run.goodvm.net',
        'namespace': 'cliu201'
    },
    'spec': {
        'certificateMode': 'AUTOMATIC', 
        'routeName': 'cloudrun-node-test'
    }
}


def main():
    # Application default credentials are provided in Google API Client Libraries automatically.
    # You just have to build and initialize the API:

    # service = googleapiclient.discovery.build('run', 'v1', http=None, discoveryServiceUrl="us-central1-run.googleapis.com")
    service = googleapiclient.discovery.build('run', 'v1',client_options={"api_endpoint": "https://us-central1-run.googleapis.com"})
    # service = googleapiclient.discovery.build('run', 'v1')

    try:
        # lists = service.namespaces().domainmappings().create(parent="namespaces/cliu201", body=json_payload,  dryRun="all").execute()
        lists = service.namespaces().domainmappings().create(parent="namespaces/cliu201", body=json_payload).execute()
        pprint.pprint(lists)
        pprint.pprint('**************************************')

    except httplib2.HttpLib2Error as e:
        print('Error response status code : {0}, reason : {1}'.format(
            e.status_code, e.error_details))


if __name__ == '__main__':
    main()
