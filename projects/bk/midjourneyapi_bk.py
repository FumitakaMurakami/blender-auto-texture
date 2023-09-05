import requests
import json

@app.get("/images/create")
async def get_midj_image(prompt:str):
    url = "https://demo.imagineapi.dev/items/images/"

    payload = {
        "prompt" : f"{ prompt } --ar 9:21 --chaos 40 --stylize 1000",
    };

    print("pay load",payload)
    
    headers = {
        f'Authorization': "Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=payload)

    print(response.text)
    response_obj = json.loads(response.text)

    if response_obj["data"]["error"] == True:
        raise Exception("midjourney APIでメッセージIDが取得できませんでした。")

    # API Resultはこの形で取れる
    #  data: {
    #    id: '7bf67cb7-93a1-46b4-90b1-d9d374ae617c',
    #    prompt: 'a pretty lady at the beach --ar 9:21 --chaos 40 --stylize 1000',
    #     results: null,
    #     user_created: '7516648b-4996-4809-849d-d095c6067e4a',
    #     date_created: '2023-09-04T06:51:22.074Z',
    #     status: 'pending',
    #     progress: null,
    #     url: null,
    #     error: null,
    #     upscaled_urls: null,
    #     upscaled: []
    #   }

    message_id = response_obj["data"]["id"];
    status = response_obj["data"]["status"];
    return { "id" :message_id,"status":status}


@app.get("/images/progress/{message_id}")
async def get_progress(message_id):
    url = f"https://demo.imagineapi.dev/items/images/{message_id}"

    print(url)

    headers = {
        'Authorization': 'Bearer {token}', 
        'Content-Type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers)

    print(response.text)

    return response.text
    