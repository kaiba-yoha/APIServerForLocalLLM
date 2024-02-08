from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import json
from llama_cpp import Llama
from urllib.parse import parse_qs, urlparse

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):


    def do_POST(self):
      
        response= dict()
        print('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))

        print('headers\r\n-----\r\n{}-----'.format(self.headers))

        content_length = int(self.headers['content-length'])
        
        body=self.rfile.read(content_length).decode('utf-8')
        data=json.loads("{\"name\":\"kaiba\",\"history\":[{\"name\":\"kaiba\",\"content\":\"こんにちは\"},{\"name\":\"rico\",\"content\":\"やっほー、お昼食べた？\"}]}")
        name=data['name']
        instruction="<<SYS>>貴方は「都内大学生雑談グループ！」という名前のグループチャット上で複数人と会話しています。貴方のユーザーネームは{}です。以下は会話の履歴です。{}として、この会話に続くように一度だけ返答を行ってください。ただし、必ず返答は20字程度で行ってください。 <</SYS>>".format(name,name)
        attribute="[ATTR] helpfulness: 0 correctness: 4 coherence: 4 complexity: 4 verbosity: 4 quality: 4 toxicity: 4 humor: 4 creativity: 4 [/ATTR]"
        llm = Llama(model_path = "../karakuri-lm-70b-chat-v0.1-q4_0.gguf", n_gpu_layers = 81)
        output = llm(" <s>[INST]"+instruction+ data['history'] +attribute+"[/INST]")
        print(output['choices'][0]['text'])
        response["content"]=(output['choices'][0]['text'])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dump(response).encode())


server_address = ('localhost', 8000)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
httpd.serve_forever()
