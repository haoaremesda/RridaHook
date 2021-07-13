from mitmproxy import http
import json


class Fans():
    def response(self, flow: http.HTTPFlow):
        if "gw/mtop.taobao.idle.search.glue/8.0/" in flow.request.url:
            if "itemId" in flow.response.text:
                resultList = json.loads(flow.response.text)["data"]["resultList"]
                for item in resultList:
                    item_text = json.dumps(item)
                    print("***************************************************************************")
                    print(item_text)
                    print("***************************************************************************")

addons = [
    Fans()
]