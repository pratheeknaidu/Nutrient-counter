def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']}.")

    import boto3
    from google.cloud import storage
    import pandas as pd
    import fsspec
    import gcsfs
    from google.cloud import pubsub_v1
    import json
    import requests
    from bs4 import BeautifulSoup

    ACCESS_KEY_ID = 'AKIA4EG24ZT6ZDHHCYEK'
    ACCESS_KEY = 'ciN2fJEkRg4ejpheHBqDx5wK4SqIhK+ngjMKBgNL'
    REGION_NAME = 'us-east-1'

    project_id = "nomadic-talon-318102"
    topic_id = "test-gcp-1"
    publisher = pubsub_v1.PublisherClient()

    df = pd.read_excel('gs://{}/{}'.format(file['bucket'], 'nutrients_usda.xlsx'))


    def rekognition():
        rekognition_client = boto3.client('rekognition', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY,
                                      region_name=REGION_NAME)
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(file['bucket'])
        source_blob = source_bucket.blob(file['name'])
        uploaded_image = source_blob.download_as_string()
        response = rekognition_client.detect_labels(Image={'Bytes': uploaded_image})

        df_list = df['name'].to_list()
        df_set = set(df_list)

        food_pred = []
        unwanted_labels = {'dish', 'meal', 'food', 'plant', 'platter', 'vegetable', 'produce'}
        for label in response['Labels']:
            print(label['Name'] + ' : ' + str(label['Confidence']))
            res = [i for i in df_set if ((label['Name'].lower() in i.lower()) or (i.lower() in label['Name'].lower())) and (label['Name'].lower() not in unwanted_labels)]
            if res:
                food_pred.append({'name': label['Name'], 'confidence': label['Confidence']})

        print("food_pred", food_pred)
        return food_pred[0]['name']

    def get_recipe(predicted_label):
        receipe_link = None
        base_url = "https://www.allrecipes.com/search/results/?search="
        URL = base_url + predicted_label
        print("SearchUrl", URL)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(class_="component card card__recipe card__facetedSearchResult")

        if results is not None:
            results_class = results.find(class_="card__imageContainer")
            elements = results_class.find("a", class_="card__titleLink")
            # print("Ele", elements)
            print("Link", elements.get("href"))
            print("Title", elements.get("title"))
            recipe_link = elements.get("href")
        return recipe_link

    def get_nutrients(predicted_label):
        agg = df.query('name.str.contains("{}")'.format(predicted_label), engine='python')
        calories = round(agg['Energy (kcal)'].mean(), 2)
        total_fat = round(agg['Total Fat (g)'].mean(), 2)
        cholestrol = round(agg['Cholesterol (mg)'].mean(), 2)
        sodium= round(agg['Sodium (mg)'].mean(), 2)
        total_carb= round(agg['Carbohydrate (g)'].mean(), 2)
        fiber= round(agg['Fiber, total dietary (g)'].mean(), 2)
        sugars= round(agg['Sugars, total(g)'].mean(), 2)
        protein= round(agg['Protein (g)'].mean(), 2)
        vitamin_d= round(agg['Vitamin D (D2 + D3) (mcg)'].mean(), 2)
        calcium= round(agg['Calcium (mg)'].mean(), 2)
        iron= round(agg['Iron(mg)'].mean(), 2)
        potassium= round(agg['Potassium (mg)'].mean(), 2)
        
        #Getting receipe Link
        recipe_url = get_recipe(predicted_label)

        print(calories,total_fat,cholestrol,sodium,total_carb,fiber,sugars,
          protein,vitamin_d,calcium,iron,potassium,recipe_url)

        nutrient_dict = {"image_name": file['name'], "predicted_label": predicted_label,
                     "calorie_values": {"calories": calories, "total_fat": total_fat, "cholestrol": cholestrol,
                                        "sodium": sodium, "total_carb": total_carb,
                                        "fiber": fiber, "sugars": sugars,
                                        "protein": protein, "vitamin_d": vitamin_d, "calcium": calcium, "iron": iron,
                                        "potassium": potassium},
                     "recipe_link": recipe_url}
        return json.dumps(nutrient_dict)


    def publish(nutrient_values):
        publisher = pubsub_v1.PublisherClient()
        # The `topic_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/topics/{topic_id}`
        topic_path = publisher.topic_path(project_id, topic_id)
        nutrient_values = nutrient_values.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, nutrient_values)
        print(future.result())
        print(f"Published messages to {topic_path}.")


    predicted_label = rekognition().lower().strip()
    nutrient_values = get_nutrients(predicted_label)
    publish(nutrient_values)
