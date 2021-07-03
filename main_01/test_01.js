Java.perform(function () {
    Java.openClassFile("data/local/tmp/gson-2.8.5.dex").load()
    var Gson = Java.use("com.google.gson.Gson")
    var gson = Gson.$new()
    var InnerSignImpl = Java.use("mtopsdk.security.InnerSignImpl")
    function a(params) {
        var keyset = params.keySet()
        var it = keyset.iterator()
        while (it.hasNext()) {
            var keystr = it.next().toString()
            var valuestr
            if (params.get(keystr) != null) {
                valuestr = params.get(keystr).toString()
            } else {
                valuestr = params.get(keystr)
            }
            console.log(keystr, valuestr)
        }
        console.log("*******************")
    }

    var InnerSignImpl = Java.use("mtopsdk.security.InnerSignImpl")
    InnerSignImpl.getUnifiedSign.implementation = function (params, ext, appKey, authCode, useWua, requestId) {
        console.log("params", gson.toJson(params))
        console.log("ext", gson.toJson(ext))
        console.log(appKey)
        console.log(authCode)
        console.log(useWua)
        console.log(requestId)
        console.log("*******************")
        var ret = this.getUnifiedSign(params, ext, appKey, authCode, useWua, "r_1")
        console.log(ret.toString())
        console.log("*******************")
        return ret
    }
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.zJ.overload().implementation = function () {
        return false;
    }
})