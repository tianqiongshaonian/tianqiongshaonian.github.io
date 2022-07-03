# js扁平化json和array【递归方式处理】

**js扁平化json代码：**

【注意事项】内层json名字不建议外层json名称重名，否者内层json对象会覆盖外层json对象

	/*
	
	    递归扁平化json对象
	
	    jsonArr 传入json 对象列表 和 json 对象都可以
	
	    注意事项:内层json名字不建议外层json名称重名，否者内层json对象会覆盖外层json对象
	
	*/
	
	
	function delayeringJson(jsonArr = {}) {
	    // 赋值一份，不改变原数组
	    jsonArr = JSON.parse(JSON.stringify(jsonArr));
	    // 赋值给一个变量，防止闭包内存泄漏
	    let innerFun = function (jsons = {}, newJson = {}) {
	        for (let i in jsons) {
	            // 只处理json对象，不处理数组
	            if (jsons[i] instanceof Object && jsons[i] instanceof Array == false) {
	                innerFun(jsons[i], newJson);
	            } else {
	                newJson[i] = jsons[i];
	            }
	        }
	        return newJson;
	    }
	    return innerFun(jsonArr);
	}
	
	// 代码调用示例
	var tempObj = [{ name: '张山', age: 35, sex: '男', classB: { page: 1, test: '没有', ren: '计算中' } },{ nameA: '张山', ageA: 35, sexA: '男', classBA: { pageA: 1, testA: '没有', renA: '计算中' } }];
	console.log(delayeringJson(tempObj));

**js扁平化array代码：**

【建议】传入数字和字符串

	/*

	    递归扁平化json对象
	
	    tempArr 传入数组无限层级得数组
	
	*/
	
	function delayeringArray(tempArr = []) {
	    // 解决对象引用类型
	    tempArr = JSON.parse(JSON.stringify(tempArr));
	    // 赋值给一个变量，防止闭包内存泄漏
	    let innerFun = function (tempArr = [], newTempArr = []) {
	        for (let i = 0; i < tempArr.length; i++) {
	            if (tempArr[i] instanceof Array) {
	                innerFun(tempArr[i], newTempArr);
	            } else {
	                newTempArr.push(tempArr[i]);
	            }
	        }
	        return newTempArr;
	    }
	    return innerFun(tempArr);
	}
	
	// 代码调用示例
	var tempArr = [1, 889, 38989, 8989, 555, [5887, '89898989', 1, [5888, 125, [89652, 656], 56556], 8989], 85, 26, 35, 15, 48, 58];
	console.log(delayeringArray(tempArr));

**js扁平化array代码【简洁版本】：**

【缺点】所有的值会被强制转换为字符串，可以满足工作中大部分需求

	// 代码调用示例
	var tempArr = [1, 889, 38989, 8989, 555, [5887, '89898989', 1, [5888, 125, [89652, 656], 56556], 8989], 85, 26, 35, 15, 48, 58];
	    tempArr = JSON.stringify(tempArr).replace(/[\[|\]|\'|\"]/g,'').split(',');

	    console.log(tempArr)