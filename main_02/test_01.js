function showStacks() {
        Java.perform(function () {
            send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
        });
    }
Java.perform(function () {
    Java.openClassFile("data/local/tmp/gson-2.8.5.dex").load()
    var Gson = Java.use("com.google.gson.Gson")
    var gson = Gson.$new()

    // var InnerProtocolParamBuilderImpl = Java.use("mtopsdk.mtop.protocol.builder.impl.InnerProtocolParamBuilderImpl")
    // InnerProtocolParamBuilderImpl.buildParams.implementation = function (mtopContext) {
    //     showStacks()
    //     var ret = this.buildParams(mtopContext)
    //     console.log("params", gson.toJson(ret))
    //     console.log("*******************")
    //     return ret
    // }

    var InnerSignImpl = Java.use("mtopsdk.security.InnerSignImpl")
    InnerSignImpl.getUnifiedSign.implementation = function (params, ext, appKey, authCode, useWua, requestId) {
        showStacks()
        var ret = this.getUnifiedSign(params, ext, appKey, authCode, useWua, requestId)
        console.log("params", gson.toJson(ret))
        console.log("*******************")
        return ret
    }


    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.zJ.overload().implementation = function () {
        return false;
    }
})