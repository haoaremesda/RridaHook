import frida, sys
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function () {
    function a(params) {
        var keyset = params.keySet()
        var it = keyset.iterator()
        while(it.hasNext()){
            var keystr = it.next().toString()
            var valuestr
            if (params.get(keystr) != null){
                valuestr = params.get(keystr).toString()
            } else{
                valuestr = params.get(keystr)
            }
            console.log(keystr, valuestr)
        }
        console.log("*******************")
    }
    
    var InnerSignImpl = Java.use("mtopsdk.security.InnerSignImpl")
        InnerSignImpl.getUnifiedSign.implementation = function (params, ext, appKey, authCode, useWua, requestId) {
            a(params)
            a(ext)
            console.log(appKey)
            console.log(authCode)
            console.log(useWua)
            console.log(requestId)
            var ret = this.getUnifiedSign(params, ext, appKey, authCode, useWua, "r_1")
            console.log(ret.toString())
            return ret
        }
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.zJ.overload().implementation = function () {
            return false;
        }
})
"""

process = frida.get_usb_device().attach('com.taobao.idlefish')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()