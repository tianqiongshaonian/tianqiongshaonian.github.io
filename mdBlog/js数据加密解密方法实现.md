# js数据加密解密方法实现

**这里主要采用了原生js的 charCodeAt 的方法加密解密**

原理其实比较简单，把字符串转换unicode编码，然后再把unicode编码转换回来就可以了。

**优点：**

1、按照这个思路来所有语言通用，且可以和其他编程语言交换数据

2、思路简单

**数据加密方法如下:**

注：str_json 要加密的数据 ，salt 加密的盐，对应解密的salt 

	// 数据加密方法

	function Encode(str_json, salt) {
		 var str_arr = JSON.stringify(str_json);
		 var res = [];
		 for (var i in str_arr) {
		 	res[i] = str_arr.charCodeAt(i) + salt;
		 }
		return JSON.stringify(res);
	}


**数据解密方法：**

	// 数据解密方法
	function Decode(str_json, salt) {
		 var str_arr = JSON.stringify(str_json).replace(/[\[|\]|\"|\']/g,'').split(/\,/);
		 var res = "";
		 for (var i in str_arr) {
		 	res += String.fromCharCode(Number(str_arr[i]) + salt);
		 }
		 return JSON.parse(res);
	}

**调用示例：**

	console.log(Decode(Encode([1,8,9,{name:'张三'}],8),-8));