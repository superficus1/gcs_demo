import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/crist/AppData/Roaming/gcloud/legacy_credentials/cristian.sarti@awentia.com/adc.json"

from pathlib import Path
from google.cloud import storage
from google.cloud.storage import Blob

# Initialise a client
storage_client = storage.Client("[awentia-backend-mvp]")
# Create a bucket object for our bucket
bucket = storage_client.get_bucket("awentia-data-collection-eu-ita-2022-prod")

#blob = Blob("f1463603d23ca1c0/2022-07-15T08:33:23.489Z.json", bucket)
#with open("C:/Users/crist/Desktop/vscode_projects/GCS_script/download/testFile.json", "wb") as file_obj:
#    blob.download_to_file(file_obj)

blob_list = list(bucket.list_blobs())

blobList = [file.name for file in blob_list if '.json' in file.name]

dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'download/master.json')
#fileName = "C:/Users/crist/Desktop/vscode_projects/GCS_script/download/master.json"
stringIncipit = "\"grafana_test_jsons\" : ["

with open(fileName,"a") as file_obj:
        file_obj.write(str("\n"))
        file_obj.write(str("{"))
        file_obj.write(str("\n"))
        file_obj.write(str(stringIncipit))
        file_obj.write(str("\n"))
        file_obj.close   

for blob in blobList:
    
    print(blob)

    blobReplaced = blob.replace(":","-")
    p = Path(blobReplaced)
    absoluteDir = "C:/Users/crist/Desktop/vscode_projects/GCS_script/download/"
    directoryName = str(p.parent)
    os.makedirs(absoluteDir + directoryName, exist_ok=True)
    blobName = p.name
    blobObj = Blob(blob, bucket)
    jsonData = blobObj.download_as_string()
    with open(fileName,"a") as file_obj:
        file_obj.write(jsonData.decode('utf-8'))
        file_obj.write(str("\n"))
        file_obj.write(str(","))
        file_obj.close

with open(fileName, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()

with open(fileName,"a") as file_obj:
    file_obj.write(str("\n"))
    file_obj.write(str("]"))
    file_obj.write(str("\n"))
    file_obj.write(str("}"))
    file_obj.close   


from github import Github

# First create a Github instance:
# using an access token
g = Github("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")
GITHUB_REPO = "gcs_demo"
repo = g.get_user().get_repo(GITHUB_REPO)
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

with open("C:/Users/crist/Desktop/vscode_projects/GCS_script/download/master.json", 'r') as file:
    content = file.read()

# Upload to github
git_prefix = 'superficus1/gcs_demo/'
git_file = git_prefix + 'master.json'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="main")
    print(git_file + ' CREATED')
