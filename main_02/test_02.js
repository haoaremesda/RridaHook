function main() {
    Java.perform(function () {
        console.log("start")
        Java.enumerateClassLoaders({
            onMatch: function (loader) {
                try {
                    if (loader.findClass("com.alibaba.one.android.inner.DataReportJniBridge")) {
                        console.log("Successfully found loader")
                        console.log(loader);
                        Java.classFactory.loader = loader;
                    }
                } catch (error) {
                    // console.log("find error:" + error)
                }
            },
            onComplete: function () {
                console.log("end1")
            }
        })


        var native = Java.use("com.alibaba.one.android.inner.DataReportJniBridge");
        console.log(Object.getOwnPropertyNames(native.__proto__).join('==>'));
        console.log("end2")
    })
}

setImmediate(main)
