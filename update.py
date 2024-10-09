import urllib.request
import urllib.parse
import ssl
import html
import json
import zlib
import base64
import subprocess
import os
import sys
import traceback
from xml.dom import minidom

# GetCookie.xml
GET_COOKIE_XML = zlib.decompress(base64.b64decode(b'eNrFVFtvmzAUft+viPIOtoGUBNFIbVptldppEmSd9jI5cJpYBYxs0yT79TsOhGTpups67QFh+9y/850TX1dPUMgaBpuyqHS00eJ8uDKmjghZr9fu2nelWhKPUkY+3d0m2QpK7ohKG15lMOyt8l9bdcovKPqEjoiWvHagy2g4fTMYxO+A56DsES8XmRGyGuR+zaKy0WZeocymguHZPhkr/f0gP01qROiY8DxXoLWolsPpkVYpMiW1fDBuJkuS4GHNFVwJbZRYNDZPkoB6AkVmhYDK3MPC3kUG5C2YmZSPAmLSVtSVd4dh+BJurv4sqUZVUdOIPFpMFoEfjkLH84LQCfJw4XAYPzg8ZAs+5p7nj89i0kfpoqbyPwOqUe0BfDeHQiBeW7esT9B9hmC2e3C5LjcxSWVXSQJZo4TZ/st6cplpV3IttIPSame41toaBwTp3orsjTIHBfbr0nLwABvjMJe6ODHDNmvbAVECJlnWrxgLGVjY/2kwDDdTwA3kU4+y0GGeQ72U0oidRWzkeox+jsle42BzvakFNq238SYpPYu8URT47iTw0WavsS+K9FX1T/eiyuVaz+scvaciewSjU/kIONEBNkxgk9pO3yUXfbOCo2a9JiAnWOvdjtInxCt1Y72zgDBKvkv/ojErqcRXbuf3GN22rnSLK/U9L+F8uCvmI9IQFZGFLh0OPshCZFsUXd58SZLbI3N0MNegBuTIIzm4PKD7IpbdLJD9MOy2KDms0fhS5ttOqV9EPxjav99vB2LLIm/9H/J+/lRwbWYrXi3BsmvkMOp4LGVhRFlEQ5cFoTdhlmFHintbLFFhbEu1F+gcouGx1t6yVtLITBZdY6bMDWhMTl87LHucWjBbBJHy3Y6YfgMAjFBH')).decode("utf-8")

# WUIDRequest.xml
WUID_REQUEST_XML = zlib.decompress(base64.b64decode(b'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')).decode("utf-8")

unverifiedContext = ssl.create_default_context()
unverifiedContext.check_hostname = False
unverifiedContext.verify_mode = ssl.CERT_NONE

cookie = os.getenv("COOKIE")
# getting the encrypted cookie for the fe3 delivery api
def getCookie():
    global cookie
    if cookie:
        return cookie
    cookie_content = GET_COOKIE_XML
    request=urllib.request.Request(
        "https://fe3.delivery.mp.microsoft.com/ClientWebService/client.asmx",
        data=cookie_content.encode("utf-8"),
        headers={"Content-Type": "application/soap+xml; charset=utf-8"}
    )
    out = urllib.request.urlopen(request, context=unverifiedContext, timeout=20)
    doc = minidom.parseString(out.read())
    # extracting the cookie from the EncryptedData tag
    cookie = doc.getElementsByTagName('EncryptedData')[0].firstChild.nodeValue
    return cookie

# getting the update id,revision number and package name from the fe3 delivery api by providing the encrpyted cookie, cat_id, realse type
def getUpdates(cookie, categoryID):
    # Map {"retail": "Retail", "release preview": "RP","insider slow": "WIS", "insider fast": "WIF"}
    release_type = "Retail"
    cat_id_content = WUID_REQUEST_XML.format(cookie, categoryID, release_type)
    request=urllib.request.Request(
        "https://fe3.delivery.mp.microsoft.com/ClientWebService/client.asmx",
        data=cat_id_content.encode("utf-8"),
        headers={'Content-Type': 'application/soap+xml; charset=utf-8'}
    )
    out = urllib.request.urlopen(request, context=unverifiedContext, timeout=20)
    text = html.unescape(out.read().decode("utf-8"))
    return text

def getUpdateIdentityByCategoryId(categoryId, withOriginalUpdatesString = False):
    result = []
    cookie = getCookie()
    updatesString = getUpdates(cookie, categoryId)
    updatesDoc = minidom.parseString(updatesString)
    nodes = updatesDoc.getElementsByTagName("SecuredFragment")
    for node in nodes:
        xml = node.parentNode.parentNode
        updateID = xml.firstChild.attributes["UpdateID"].nodeValue
        packageMoniker = xml.getElementsByTagName("AppxMetadata")[0].attributes["PackageMoniker"].nodeValue
        id = xml.parentNode.firstChild.firstChild.nodeValue
        result.append((updateID, packageMoniker, id))

    if not withOriginalUpdatesString:
        return result
    return result, updatesString

#------------------------------------------------------------------------------------------------------------------------------------

def getPackageIdentityName(packageFamilyName):
    return packageFamilyName[:packageFamilyName.rfind("_")]

def getPackageVersionAndArch(packageMoniker):
    firstIdx = packageMoniker.find("_")
    secondIdx = packageMoniker.find("_", firstIdx + 1)
    thirdIdx = packageMoniker.find("_", secondIdx + 1)
    if firstIdx != -1 and secondIdx != -1 and thirdIdx != -1:
        return packageMoniker[firstIdx + 1:secondIdx], packageMoniker[secondIdx + 1:thirdIdx]
    return None

# [(updateID, packageMoniker, id, version, arch)...]
def getCurrentVersionInfo(packageFamilyName, categoryId):
    packageIdentityName = getPackageIdentityName(packageFamilyName)
    versions = []
    result, xmlStr = getUpdateIdentityByCategoryId(categoryId, withOriginalUpdatesString=True)
    for i in result:
        packageMoniker = i[1]
        if packageIdentityName in packageMoniker:
            versions.append(i + getPackageVersionAndArch(packageMoniker))
    return versions, xmlStr

def appxVer2GameVer(appxVersion: str) -> tuple[int]:
    arr = appxVersion.split(".")
    if (n := 4 - len(arr[2])) > 0:
        arr[2] = ("0" * n) + arr[2]
    major = arr[0]
    minor = arr[1]
    patch = arr[2][:-2]
    revision = arr[2][-2:]
    fifth = arr[3]
    return (int(major), int(minor), int(patch), int(revision), int(fifth))

def gameVer2Str(gameVer: tuple[int], withFifth = False) -> str:
    if withFifth:
        return f"{gameVer[0]}.{gameVer[1]}.{gameVer[2]}.{gameVer[3]}.{gameVer[4]}"
    else:
        return f"{gameVer[0]}.{gameVer[1]}.{gameVer[2]}.{gameVer[3]}"

def checkForUpdate(pfn, categoryId, releaseType):
    updateInfo, xml = getCurrentVersionInfo(pfn, categoryId)
    
    with open("versions.json.min", "r") as f:
        versions = json.load(f)

    newVersion = True
    gameVer = None
    idt = getPackageIdentityName(pfn)
    updateTxt = ""
    for i in updateInfo:
        if idt in i[1]:
            updateTxt += f"{i[0]} {i[1]} {i[2]}\n"
            if i[4] == "x64":
                gameVer = gameVer2Str(appxVer2GameVer(i[3]))
                for ver in versions:
                    if ver[2] == releaseType and ver[0] == gameVer:
                        newVersion = False
                        break
                if newVersion:
                    versions.append([gameVer, i[0], releaseType])

    if newVersion and gameVer:
        print("New version detected:", idt, gameVer)

        commitMsg = "Minecraft " + gameVer
        if releaseType == 2:
             commitMsg += " (Preview)"
            
        result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True)
        latest_tag = result.stdout.strip()

        if latest_tag.startswith('v'):
            tag_number = int(latest_tag[1:]) + 1
        else:
            tag_number = 1
        

        with open("versions.json.min", "w") as f:
            json.dump(versions, f)
        with open("versions.txt", "r") as f:
            verTxt = f.read()
            target = "Releases" if releaseType == 0 else "Preview"
            start = verTxt.find("\n\n", verTxt.find(target))
            with open("versions.txt", "w") as wf:
                wf.write(verTxt[:start] + "\n" + updateTxt + verTxt[start:])

        subprocess.run(["git", "add", "versions.json.min", "versions.txt"])
        subprocess.run(["git", "-c", "user.name='github-actions[bot]'", "-c", "user.email='github-actions[bot]@users.noreply.github.com'", "commit", "-m", commitMsg])
        subprocess.run(["git", "push", "origin"])

        # Add the new tag
        tag_name = f"v{tag_number}"
        subprocess.run(["git", "tag", tag_name])
        subprocess.run(["git", "push", "origin", tag_name])

        if os.getenv("ENABLE_NOTIFICATION"):
            try:
                import notification
                cp = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
                commitId = cp.stdout.decode("utf-8").strip()
                notification.pushNotification(pfn, gameVer, releaseType, commitId)
            except:
                print("Failed to push notification.")
                traceback.print_exc()
    else:
        print(idt, "is up to date.")

if __name__ == "__main__":
    checkForUpdate("Microsoft.MinecraftUWP_8wekyb3d8bbwe", "d25480ca-36aa-46e6-b76b-39608d49558c", 0)
    checkForUpdate("Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe", "188f32fc-5eaa-45a8-9f78-7dde4322d131", 2)
