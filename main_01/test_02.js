var result;

function callEleMeFun() { //定义导出函数
    Java.perform(function () {
        Java.openClassFile("data/local/tmp/gson-2.8.5.dex").load()
        var Gson = Java.use("com.google.gson.Gson")
        var gson = Gson.$new()
        var MtopConfig = Java.use('mtopsdk.mtop.global.MtopConfig');
        var mtop = MtopConfig.$new("INNER")
        var Map = Java.use("java.util.HashMap")
        var map = Map.$new()
        map.put("deviceId", "AnuREX-s6kr2da8IIiv5PDTELdu0ZIhkhIDUHXxq5cv1")
        map.put("appKey", "21407387")
        map.put("extdata", "openappkey=DEFAULT_AUTH")
        map.put("utdid", "YPFcJnrnI5EDAE5Ul5oZADVw")
        map.put("x-features", "27")
        map.put("ttid", "1564988752866@fleamarket_android_6.9.50")
        map.put("v", "1.0")
        map.put("sid", "1a01f9001599cc544df9b657bc54f6f7")
        var timestamp = Math.round(new Date().getTime() / 1e3).toString()
        map.put("t", timestamp)
        map.put("api", "mtop.taobao.idle.awesome.detail")
        map.put("data", '{"gps":"22.507642,113.899287","itemId":"650178372851","latitude":"22.507642","longitude":"113.899287","needSimpleDetail":false}')
        map.put("uid", "2276087233")
        map.put("lng", "113.899287")
        map.put("lat", "22.507642")
        var map2 = Map.$new()
        map2.put("pageName", "")
        map2.put("pageId", "")
        var a = Java.use("mtopsdk.security.InnerSignImpl")
        var sign_impl = a.$new()
        sign_impl.init(mtop)
        var appKey = "21407387"
        console.log(gson.toJson(map))
        var res = sign_impl.getUnifiedSign(map, map2, appKey, null, false, "r_1");
        console.log(gson.toJson(res))
        result = gson.toJson(res)
    })
    return result
}

Java.perform(function () {
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
        SwitchConfig.zJ.overload().implementation = function () {
            return false;
        }
});

function callDYFun(url) { //定义导出函数
    Java.perform(function () {
        var ss = Java.use('com.ss.sys.ces.gg.tt$1');
        var HashMap = Java.use("java.util.HashMap").$new();
        var jsonObj = Java.use('org.json.JSONObject');
        var str = Java.use("java.lang.String");
        var res = jsonObj.$new(ss.$new().a(url, HashMap));
        result = str.valueOf(res);
    });
    return result;
}


rpc.exports = {
    callsecretfunctioneleme: callEleMeFun,
    callsecretfunctionedy: callDYFun,
};