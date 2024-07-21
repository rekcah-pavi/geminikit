# <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" width="35px" alt="Gemini Icon" /> GeminiKit

An unofficial Python wrapper, geminikit, has been developed through reverse-engineering. This tool utilizes cookie values to interact with Google Gemini for testing purposes.

<br>


## Installation
```bash
pip install -U geminikit
```
or

```bash
pip install git+https://github.com/rekcah-pavi/geminikit
```

***

## Log Cookies 
<h6>video guide</h6>
<a href="https://youtu.be/IUCJg2KWcJs">
  <img src="https://img.youtube.com/vi/IUCJg2KWcJs/maxresdefault.jpg" alt="Watch the video" width="40%" height="250" />
</a>
<br>


### 1. Close All Tabs
Ensure all tabs are closed in Google Chrome.

### 2. Access Network Export
- Open a new tab and navigate to `chrome://net-export/`.

### 3. Configure Logging Settings
- Check the box labeled `Include cookies and credentials`.
- Set the `Maximum log size` to `1 MB`.
- Click the `Start logging` button.

### 4. Perform Actions
- Open a new tab and go to [gemini.google.com](https://gemini.google.com).
- Log in to your Gemini account.
- Send a sample message and wait for Gemini's response.

### 5. Stop Logging
- Return to the logging tab and click the `Stop logging` button.

### 6. Retrieve Cookies
- The cookies will be saved in a JSON file.

### 7. Get cookies from your saved file
```python
from geminikit import get_cookies_from_file

with open("chrome-net-export-log.json",'r') as f:
	cookies = get_cookies_from_file(f.read())

print(cookies)
```
***

## Usage
## Setup gemini
```python
from geminikit import Gemini
gemini = Gemini(cookies)

```

### Ask a message
```python
res = gemini.ask("hello")
print(res['text'])
```


### Text to Voice
```python
res = gemini.speech("hello")
with open("a.wav","wb") as f:
	f.write(res)
```



