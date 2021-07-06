function showStacks() {
    Java.perform(function () {
        send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
    });
}

function ttsz() {
    Java.perform(function () {
        Java.openClassFile("data/local/tmp/gson-2.8.5.dex").load()
        var Gson = Java.use("com.google.gson.Gson")
        var gson = Gson.$new()
        var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
        SwitchConfig.zJ.overload().implementation = function () {
            return false;
        }

        // var InnerProtocolParamBuilderImpl = Java.use("mtopsdk.mtop.protocol.builder.impl.InnerProtocolParamBuilderImpl")
        // InnerProtocolParamBuilderImpl.buildParams.implementation = function (mtopContext) {
        //     showStacks()
        //     var ret = this.buildParams(mtopContext)
        //     console.log("params", gson.toJson(ret))
        //     console.log("*******************")
        //     return ret
        // }

        // var InnerSignImpl = Java.use("mtopsdk.security.InnerSignImpl")
        // InnerSignImpl.getUnifiedSign.implementation = function (params, ext, appKey, authCode, useWua, requestId) {
        //     showStacks()
        //     var ret = this.getUnifiedSign(params, ext, appKey, authCode, useWua, requestId)
        //     console.log("params", gson.toJson(ret))
        //     console.log("*******************")
        //     return ret
        // }
        // var current_application = Java.use('android.app.ActivityThread').currentApplication();
        // var context = current_application.getApplicationContext();
        // // console.log(context)
        // var WVWebPushService = Java.use("android.taobao.windvane.extra.uc.WVWebPushService")
        // console.log(WVWebPushService)
        // var methods = WVWebPushService.class.getDeclaredMethods();
        // for (var i in methods) {
        //     console.log(methods[i].toString());
        // }
        var DeviceSecuritySDK = Java.use("com.taobao.dp.DeviceSecuritySDK")

        DeviceSecuritySDK.getSecurityToken.overload().implementation = function () {
            showStacks()
            var current_application = Java.use('android.app.ActivityThread').currentApplication();
            var context = current_application.getApplicationContext();
            var res = this.getSecurityToken()
            console.log(res)
            return res;
        }

        // var devi = DeviceSecuritySDK.$new(context)
        // var res = devi.getSecurityToken()
        // console.log("sadsadad", res)
        // var utut = UTUtdid.instance(context)
        // var res = utut.readUtdid()
        // var dit = sess.System.getString(context, "mqBRboGZkQPcAkyk")
        // var res = utut.generateUtdid()
        // console.log(gson.toJson(res))
        // console.log(Base64.encodeToString(res, 2))
        // console.log(res)

        // var wvws = WVWebPushService.getInstance(context)
        // console.log(wvws)
        // wvws.init()
        // var res = wvws.getUtdidBySdk()
        // console.log(res)
        // return res
    })
}

function hook_all() {

    Java.perform(function () {
        Java.enumerateLoadedClasses({
            //枚举已经加载的类
            onMatch: function (name, handle) {
                //每枚举一个类就会调用一次这个函数
                console.log('\n***class\n' + name);
                var clazz = Java.use(name);
                console.log('\n***name' + clazz);
                var methods = clazz.class.getDeclaredMethods();
                for (var i = 0; i < methods.length; i++) {
                    console.log('\n***methods\n' + methods[i])
                }
            },
            onComplete: function () {
                //所有的类枚举完了会调用这个函数(只会调用一次)
                console.log('完成所有类的枚举')
            }
        });
    });
}

function main() {
    ttsz()
}

setImmediate(main);