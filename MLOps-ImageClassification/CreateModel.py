from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials
import time
import datetime
import wget
import os

cv_endpoint = os.getenv('ENDPOINT')
training_key = os.getenv('KEY')
training_images = os.getenv('IMAGES')
project_id = os.getenv('PROJECT')
resource_id = os.getenv('RESOURCE')

publish_iteration_name = "AnimalClassificationModel-" + \
    time.strftime("%Y-%m-%d-%H%M")
tag_list = []
image_list = []
tag_dict = dict()

# Create a training client
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(cv_endpoint, credentials)

# Create the tags and add the images to a list
directories = os.listdir(training_images)
tag_list = trainer.get_tags(project_id)

# Filter tag names
for tags in tag_list:
    tag_dict.setdefault(tags.name, tags.id)

# Create tag in Custom Vision Project if doesnt exists
for tagName in directories:
    if tagName not in tag_dict.keys():
       tag = trainer.create_tag(project_id, tagName)

for tagName in directories:
    images = os.listdir(os.path.join(training_images, tagName))
    for img in images:
        with open(os.path.join(training_images, tagName, img), "rb") as image_contents:
            image_list.append(ImageFileCreateEntry(
                name=img, contents=image_contents.read(), tag_ids=[tag_dict.get(tagName)]))

# Create chunks of 64 images


def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]


batchedImages = chunks(image_list, 64)

# Upload the images in batches of 64 to the Custom Vision Service
for batchOfImages in batchedImages:
	upload_result = trainer.create_images_from_files(
	    project_id, ImageFileCreateBatch(images=batchOfImages))

# Train the model
# try:
iteration = trainer.train_project(project_id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project_id, iteration.id)
    print("Training status: " + iteration.status)
    time.sleep(1)

# Publish the iteration of the model
trainer.publish_iteration(project_id, iteration.id,
                          publish_iteration_name, resource_id)

trainer.export_iteration(project_id, iteration.id,
                         'DockerFile', raw=False, flavor='ARM')
time.sleep(10)
download_url = (trainer.get_exports(project_id, iteration.id)[0].download_uri)
print(download_url)
with open('modelurl.txt', 'w') as f:
    f.write(download_url)