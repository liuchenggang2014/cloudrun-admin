import googleapiclient.discovery
import httplib2
import pprint




def main():
    # Application default credentials are provided in Google API Client Libraries automatically.
    # You just have to build and initialize the API:

    # service = googleapiclient.discovery.build('run', 'v1', http=None, discoveryServiceUrl="https://us-central1-run.googleapis.com")
    service = googleapiclient.discovery.build('run', 'v1')

    try:
        lists = service.namespaces().services().list(parent="namespaces/cliu201").execute()
        pprint.pprint(lists)
        pprint.pprint('**************************************')

    except httplib2.HttpLib2Error as e:
        print('Error response status code : {0}, reason : {1}'.format(
            e.status_code, e.error_details))


if __name__ == '__main__':
    main()