from mitmproxy import http
import json


class Fans():
    def request(self, flow: http.HTTPFlow) -> None:
        request_url = flow.request.url
        print(request_url)
        if request_url.endswith(".webp") or request_url.endswith(".jpg") or request_url.endswith(".png"):
            flow.response = http.HTTPResponse.make(
                400,
                "",
                {"Content-Type": "image/gif"}
            )
    def response(self, flow: http.HTTPFlow):
        # print(flow.request.url)
        try:
            print("***************************************************************************")
            print(flow.request.url)
            print(json.loads(flow.response.text))
            print("***************************************************************************")
        except:
            pass
        if "gw/mtop.taobao.idlehome.home.tabdetail/1.0/" in flow.request.url:
            if "itemId" in flow.response.text:
                resultList = json.loads(flow.response.text)["data"]["cardList"]
                for item in resultList:
                    item_text = json.dumps(item)
                    # print("***************************************************************************")
                    # print(item_text)
                    # print("***************************************************************************")

addons = [
    Fans()
]