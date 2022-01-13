from socket import timeout
from google.cloud.devtools import cloudbuild_v1
from google.cloud import storage
import tarfile

Bucket_Name = "cliu201-bucket"
Object_Name = "Dockerfile.tar.gz"
Image_Name = "gcr.io/cliu201/getloggingtoken"
SA_Mail="cliu201-sa@cliu201.iam.gserviceaccount.com"
RUN_NAME="test-cloud-build-api"


def main():
    # 1. tar and compress the docker and app finel into tar.gz
    # https://github.com/googleapis/python-cloudbuild/blob/532d4f9499b8aafaac0880fc5c4fe25e9304fb58/google/cloud/devtools/cloudbuild_v1/types/cloudbuild.py#L127
    print(f'creating {Object_Name}')
    with tarfile.open(Object_Name, mode='w|gz') as tar:
        tar.add('Dockerfile')
        tar.add("requirements.txt")
        tar.add('app', arcname="app")

    # 2. upload the tarfile into google cloud storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(Bucket_Name)
    blob = bucket.blob(Object_Name)
    blob.upload_from_filename(Object_Name)
    print(
        "File {} uploaded to {}.".format(
            Object_Name, Object_Name
        )
    )

    # 3. build image, push image, deploy cloud run service
    """Create and execute a simple Google Cloud Build configuration,
    print the in-progress status and print the completed status."""

    # Authorize the client with $GOOGLE_APPLICATION_CREDENTIALS
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient()

    build = cloudbuild_v1.Build()

    build.steps = [{"name": "docker",
                    "args": ["build", "-t", Image_Name, "."]},
                    {"name": "gcr.io/google.com/cloudsdktool/cloud-sdk",
                    "entrypoint": "gcloud",
                    "args": ['run', 'deploy', RUN_NAME, '--image', Image_Name, 
                            '--region', 'us-central1', '--platform', 'managed', '--allow-unauthenticated', '--port=3000',
                            f'--service-account={SA_Mail}']}]

    build.images=[Image_Name]

    storage_source = cloudbuild_v1.StorageSource(bucket=Bucket_Name, object_=Object_Name)
    build.source = cloudbuild_v1.Source(storage_source=storage_source)


    operation = client.create_build(project_id="cliu201", build=build, timeout=1000)
    # Print the in-progress operation
    print("IN PROGRESS:")
    print(operation.metadata)

    result = operation.result()
    # Print the completed status
    print("RESULT:", result.status)


if __name__ == '__main__':
    main()
