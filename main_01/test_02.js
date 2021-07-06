var result;

function callEleMeFun() { //定义导出函数
    Java.perform(function () {
        Java.openClassFile("data/local/tmp/gson-2.8.5.dex").load()
        var Gson = Java.use("com.google.gson.Gson")
        var gson = Gson.$new()
        var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
        SwitchConfig.zJ.overload().implementation = function () {
            return false;
        }
        var MtopConfig = Java.use('mtopsdk.mtop.global.MtopConfig');
        var mtop = MtopConfig.$new("INNER")
        console.log(mtop.toString())
        var Map = Java.use("java.util.HashMap")
        var map = Map.$new()
        map.put("deviceId", "Ag23HLdawAbgQeik2J5WKp-9MvkFWZ2_BirN3qVAFrs_")
        map.put("appKey", "21407387")
        map.put("extdata", "openappkey=DEFAULT_AUTH")
        map.put("utdid", "YNq63rgMqdIDAIsQ6dch9NzI")
        map.put("x-features", "27")
        map.put("ttid", "1564988752866@fleamarket_android_6.9.50")
        map.put("v", "1.0")
        var timestamp = Math.round(new Date().getTime() / 1e3).toString()
        map.put("t", timestamp)
        map.put("api", "mtop.taobao.idlehome.home.tabdetail")
        map.put("data", '{\"abtag\": \"style_masonryLayouts_1.0_mamaAD\", \"city\": \"\\\u5317\\\u4eac\", \"enableDx\": \"false\", \"gps\": \"39.908588595920136,116.39731499565973\", \"lastResponseCount\": 0, \"name\": \"\\\u63a8\\\u8350\", \"needBanner\": \"true\", \"needCustomsUrlParams\": \"true\", \"needMario\": \"false\", \"pageNumber\": \"1\", \"selectedTabId\": \"7996221\", \"spmPrefix\": \"a2170.7897990.feeds_7996221.\", \"trackName\": \"Item\"}')
        map.put("lng", "116.39731499565973")
        map.put("lat", "39.908588595920136")
        var map2 = Map.$new()
        map2.put("pageName", "")
        map2.put("pageId", "")
        var a = Java.use("mtopsdk.security.InnerSignImpl")
        console.log(a.toString())
        var sign_impl = a.$new()
        console.log(sign_impl)
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