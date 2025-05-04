
import requests
import time
import tkinter as tk
import vlc
import json


prompt = input("Enter a promt to generate 3d model: ")

with open("status.txt",'w') as file:
    file.truncate()

api_key = "msy_D5AOushksHiLEKc1MThWAaBgx2toQY6LjcAU" # Enter your API key here

payload = {
    "mode": "preview",
    "prompt": prompt,
    "art_style": "realistic",
    "negative_prompt": "low quality, low resolution, low poly, ugly"
}

headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.post(
        "https://api.meshy.ai/openapi/v2/text-to-3d",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()  
    
    print(response.json())
    with open('link2.txt', 'w') as file:
        file.truncate()
        link = file.write(response.json().get('result'))
    
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


time.sleep(55)
headers = {
"Authorization": f"Bearer {api_key}"
}


with open('link2.txt', 'r') as file:
        task_id = file.read()


response = requests.get(
f"https://api.meshy.ai/openapi/v2/text-to-3d{task_id}",
headers=headers,
)
response.raise_for_status()
response_data = response.json()[0]  # Get the first dict from the list
url = response_data.get('video_url')
url2 = response_data.get('model_urls', {}).get('obj')



def download_video(url, file_name):
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Video downloaded successfully as {file_name}")
    else:
        print(f"Failed to download video. HTTP Status code: {response.status_code}")


def download_model(url, file_name):
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"model downloaded successfully as {file_name}")
        with open("status.txt",'w') as file:
            file.write("done")
    else:
        print(f"Failed to download model. HTTP Status code: {response.status_code}")

download_video(url, "output.mp4")
download_model(url2, "model.obj")




class MediaPlayer:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("Python Media Player")
        self.root.geometry("600x400")
        
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        self.filepath = file_path
        media = self.instance.media_new(self.filepath)
        self.player.set_media(media)
        
        self.create_ui()

        self.player.play()

    def create_ui(self):
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(expand=True, fill="both")

        self.player.set_hwnd(self.video_frame.winfo_id())  
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    video_path = "output.mp4"
    root = tk.Tk()
    player = MediaPlayer(root, video_path)
    player.run()


print(json.dumps(response.json(), indent=2))

# import requests
# API_KEY="msy_D5AOushksHiLEKc1MThWAaBgx2toQY6LjcAU" # Enter your API key here
# headers = {
#   "Authorization": f"Bearer {API_KEY}",
# }

# response = requests.get(
#   "https://api.meshy.ai/openapi/v1/balance",
#   headers=headers,
# )
# response.raise_for_status()
# print(response.json())
