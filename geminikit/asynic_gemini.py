import httpx
import random
import re
import json
import urllib.parse
import uuid
import asyncio

from geminikit.headers import *
from geminikit.helpers import *

class Gemini:
    def __init__(self, cookies, SNlM0e, bott):
        self._reqid = int("1" + str(random.randint(0, 999999)).zfill(6))
        self.conversation_id = ""
        self.response_id = ""
        self.choice_id = ""
        self.client = httpx.AsyncClient(headers=header_main, follow_redirects=True,timeout=30.0)
        cookies = {key: str(value) for key, value in cookies.items()}
        self.client.cookies.update(cookies)
        self.SNlM0e = SNlM0e
        self.bott = bott

    @classmethod
    async def create(cls, cookies):
        self = cls.__new__(cls)
        self._reqid = int("1" + str(random.randint(0, 999999)).zfill(6))
        self.conversation_id = ""
        self.response_id = ""
        self.choice_id = ""
        self.client = httpx.AsyncClient(headers=header_main, follow_redirects=True)
        cookies = {key: str(value) for key, value in cookies.items()}
        self.client.cookies.update(cookies)
        self.SNlM0e, self.bott = await self.refresh_cookies()
        return self

    async def refresh_cookies(self):
        try:
            resp = await self.client.get(url="https://gemini.google.com", timeout=50)
            resp.raise_for_status()
        except httpx.RequestError as e:
            raise Exception(f"Could not get Google Bard cookies. Error: {str(e)}")

        try:
            SNlM0e = re.search(r"SNlM0e\":\"(.*?)\"", resp.text).group(1)
        except AttributeError:
            raise Exception("Could not get SNlM0e from response.")

        try:
            bott = re.search(r"cfb2h\":\"(.*?)\"", resp.text).group(1)
        except AttributeError:
            raise Exception("Could not get Bard version from response.")

        return SNlM0e, bott

    async def ask(self, text, **args):
        random_number = random.randint(10**(19-1), 10**19 - 1)
        fsid = '-' + str(random_number).zfill(19)
        user = args.get('user', None)

        if user:
            req_id = int(user['req_id']) + 100000
            SNlM0e = user['SNlM0e']
            bott = user['bott']
            conversation_id = user['conversation_id']
            response_id = user['response_id']
            choice_id = user['choice_id']
        else:
            req_id = self._reqid
            SNlM0e = self.SNlM0e
            bott = self.bott
            conversation_id = ""
            response_id = ""
            choice_id = ""

        params = {'bl': bott, 'f.sid': fsid, 'hl': 'en', '_reqid': req_id, 'rt': 'c'}
        photo = args.get('photo')
        
        if photo:
            if not isinstance(photo, list) or not len(photo) == 2:
                raise Exception("Photo format invalid. Expected a list of 2 elements (name, url).")
            
            data = 'f.req=%5Bnull%2C%22%5B%5Bedit_text%2C0%2Cnull%2C%5B%5B%5B%5C%22edit_url%5C%22%2C1%5D%2C%5C%22edit_name%5C%22%5D%5D%2Cnull%2Cnull%2C0%5D%2C%5B%5C%22en%5C%22%5D%2C%5B%5C%22edit_cid%5C%22%2C%5C%22edit_rid%5C%22%2C%5C%22edit_rc%5C%22%2Cnull%2Cnull%2C%5B%5D%5D%2C%5C%22edit_uid%5C%22%2C%5C%22edit_hex%5C%22%2Cnull%2C%5B1%5D%2C0%2C%5B%5D%2C%5B%5D%2C1%2C0%5D%22%5D&at=edit_sni&'
            pname = urllib.parse.quote(photo[0])
            purl = urllib.parse.quote(photo[1])
            data = data.replace("edit_name", pname)
            data = data.replace("edit_url", purl)
        else:    
            data = 'f.req=%5Bnull%2C%22%5B%5Bedit_text%2C0%2Cnull%2C%5B%5D%2Cnull%2Cnull%2C0%5D%2C%5B%5C%22en%5C%22%5D%2C%5B%5C%22edit_cid%5C%22%2C%5C%22edit_rid%5C%22%2C%5C%22edit_rc%5C%22%2Cnull%2Cnull%2C%5B%5D%5D%2C%5C%22edit_uid%5C%22%2C%5C%22edit_hex%5C%22%2Cnull%2C%5B1%5D%2C0%2C%5B%5D%2C%5B%5D%2C1%2C0%5D%22%5D&at=edit_sni&'
    
        otext = text
        text = json.dumps(text)
        text = json.dumps(text)[1:-1]

        data = data.replace("edit_text", urllib.parse.quote(text))
        data = data.replace("edit_cid", urllib.parse.quote(conversation_id))
        data = data.replace("edit_rid", urllib.parse.quote(response_id))
        data = data.replace("edit_rc", urllib.parse.quote(choice_id))
        data = data.replace("edit_sni", urllib.parse.quote(SNlM0e))
        data = data.replace("edit_uid", urllib.parse.quote(generate_random_string()))
        data = data.replace("edit_hex", str(uuid.uuid4().hex))

        try:
            response = await self.client.post(
                'https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate',
                params=params,
                headers=header_gen,
                data=data
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            raise Exception(f"Failed to post ask request. Error: {str(e)}")

        rdata = response.content

        try:
            conversation_id = re.search(r'c_([^\\]*)', rdata.decode('utf-8')).group(0)
        except AttributeError:
            raise Exception(f"Failed to get conversation_id\n{response.text}\n\ntext: {otext}")

        try:
            response_id = re.search(r'r_([^\\]*)', rdata.decode('utf-8')).group(0)
        except AttributeError:
            raise Exception("Failed to get response_id from response.")

        try:
            choice_id = re.search(r'rc_([^\\]*)', rdata.decode('utf-8')).group(0)
        except AttributeError:
            raise Exception("Failed to get choice_id from response.")

        try:
            content = re.search(r'\[\[\\"'+choice_id+r'\\",\[\\"(.*?)\\"]', rdata.decode('utf-8')).group(1)
        except AttributeError:
            raise Exception("Failed to get content from response.")

        def replace_unicode(match):
            code = match.group(1)
            return chr(int(code, 16))

        content = re.sub(r'u([0-9a-fA-F]{4})', replace_unicode, content)
        content = content.replace("\\n", "\n")
        content = content.replace("\\r", "\r")
        content = content.replace("\\", "")
        images = self.extract_image_urls(rdata)
        generated_images = self.extract_generated_image_urls(rdata)

        result = {
            "text": str(content),
            "conversation_id": conversation_id,
            "response_id": response_id,
            "choice_id": choice_id,
            "req_id": req_id,
            "fsid": fsid,
            'bott': bott,
            'image_urls': images,
            'generated_image_urls': generated_images,
            'SNlM0e': SNlM0e
        }

        return result

    def extract_image_urls(self, text):
        image_url_pattern = re.compile(r'https?://[^,\s]+?\.(?:png|jpe?g|gif)')
        text = text.decode('unicode_escape')
        urls = image_url_pattern.findall(str(text))

        nurl = []
        for i in urls:
            if "www.thesprucepets.com" in i or "filters:no_upscale()" in i:
                continue

            i = i.replace('\\', '')
            nurl.append(i)

        return nurl

    def extract_generated_image_urls(self, text):
        image_url_pattern = re.compile(r'https?://(?:.*?)gp.googleapis.com(.*?)\.png')
        text = text.decode('unicode_escape')
        urls = image_url_pattern.findall(str(text))
        nurl = []
        for i in urls:
            nurl.append("https://gp.googleapis.com" + i + ".png")

        return nurl

    async def share(self, response_id, conversation_id, choice_id,**args):
        title = args.get('title') or "geminikit"
        bott = self.bott
        fsid = '-' + str(random.randint(10**(19-1), 10**19 - 1))
        req_id = self._reqid + 100000
        SNlM0e = self.SNlM0e
        ccid = conversation_id.replace("c_", "")
        params = {
            'source-path': f'/chat/{ccid}',
            'bl': bott,
            'f.sid': fsid,
            'hl': 'en',
            '_reqid': req_id,
            'rt': 'c',
        }
        data = 'f.req=%5B%5B%5B%22fuVx7%22%2C%22%5B%5Bnull%2C%5B%5B%5B%5C%22edit_cid%5C%22%2C%5C%22edit_rid%5C%22%5D%2Cnull%2Cnull%2C%5B%5B%5D%2C%5B%5D%2C%5B%5D%2C%5C%22edit_rc%5C%22%2C%5B%5D%2C%5B%5D%5D%5D%5D%2C%5B0%2C%5C%22By%20%40bard_kpbot%5C%22%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5C%22en%5C%22%5D%5D%2Cnull%2C%5B%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at=edit_sni&'
        data = data.replace("edit_cid", conversation_id)
        data = data.replace("edit_rid", response_id)
        data = data.replace("edit_rc", choice_id)
        data = data.replace("edit_sni", SNlM0e)
        data = data.replace("bard_kpbot", title)

        try:
            response = await self.client.post('https://gemini.google.com/_/BardChatUi/data/batchexecute', params=params, headers=header_gen, data=data)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise Exception(f"Failed to share. Error: {str(e)}")

        text = str(response.content)
        try:
            a = (re.findall(r'null,(.*?)"]",', text)[0]).split('"')[-1].replace("\\", "")
            return f"https://g.co/bard/share/{a}"
        except IndexError:
            raise Exception(f"Failed to extract share URL from response: {text}")

    async def cookies(self):
        return self.client.cookies.jar

    async def speech(self, text,**args):
        lang_code = args.get("lang_code") or "en-GB"
        bott = self.bott
        SNlM0e = self.SNlM0e
        uid = int("1" + str(random.randint(0, 999999)).zfill(6))

        params = {
            "bl": bott,
            "_reqid": uid,
            "rt": "c",
        }

        input_text_struct = [[["XqA3Ic", json.dumps([None, text, lang_code, None, 2])]], ["generic"]]

        data = {
            "f.req": json.dumps(input_text_struct),
            "at": SNlM0e,
        }

        try:
            resp = await self.client.post("https://gemini.google.com/_/BardChatUi/data/batchexecute", params=params, data=data, timeout=50, headers=header_main)
            resp.raise_for_status()
        except httpx.RequestError as e:
            raise Exception(f"Failed to request Bard speech. Error: {str(e)}")

        try:
            resp_dict = json.loads(resp.content.splitlines()[3])[0][2]
            if not resp_dict:
                raise Exception(f"Failed to decode voice response. Response: {resp.text[:2000]}")
            resp_json = json.loads(resp_dict)
            audio_b64 = resp_json[0]
            audio_bytes = base64.b64decode(audio_b64)
            return audio_bytes
        except (IndexError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to decode Bard speech. Error: {str(e)}")

    async def upload_image(self, image_bytes):
        try:
            header_img_int['X-Goog-Upload-Header-Content-Length'] = str(len(image_bytes))
            url = f"https://content-push.googleapis.com/upload/"
            response = await self.client.put(url, headers=header_img_int, data=image_bytes)
            response.raise_for_status()
            upload_id = response.headers['X-GUploader-UploadID']
        except httpx.RequestError as e:
            raise Exception(f"Failed to get Bard upload image ID. Error: {str(e)}")

        try:
            url = f"https://content-push.googleapis.com/upload/?upload_id={upload_id}&upload_protocol=resumable"
            header_img_up['Content-Length'] = str(len(image_bytes))
            response = await self.client.put(url, headers=header_img_up, data=image_bytes)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            raise Exception(f"Failed to get Bard upload image URL. Error: {str(e)}")





