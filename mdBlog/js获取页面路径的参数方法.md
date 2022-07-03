# js获取页面路径的参数方法

我这里给搭建简单的弄了一种，也是我最常用的方法之一。其实方法有很多

**思路：**

主要是把window对象下面的location属性中的search取出来。

假如路径是这样子：**index.html?name=zhangshan&password=mima**

然后我们取出的值就会是：?name=zhangshan&password=mima

最后把值取出来，改成一个json对象就ok了。废话不多说了代码示例就在下面


	// 前端获取url参数方法

	function getUrlParams() {
	    var params = [];
	    var query = window.location.href.replace(/.*\?/, "");
	    var tempVar = query.split("&");
	    for (var k in tempVar) {
	        params.push({ [tempVar[k].split('=')[0]]: tempVar[k].split('=')[1] });
	    }
	    return params;
	}
	
	console.log(getUrlParams())  //  结果  [{name: "zhangshan"},{password: "mima"}]