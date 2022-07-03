# js字符串去重方法支持数组，数字

**js字符串去重方法：**

去重思路两个数组中的值进行比较相等则跳出内层循环，如果遍历至最后一个都还都不相等则push至新的数组。

【功能】：

1、支持数组去重，数组里面的为数字

2、支持数组对象去重，数组里面的可以是json对象

3、支持字符串去重

4、支持数字去重

5、以上四种混合去重，去重的外层对象必须为 Array

【代码示例】：

	/*
	      数组去重函数
	      @param tempArr 需要去重的数组，支持比较json对象，支持字符和数字串去重
	 
	  */
	
	 function remRepeat(tempArr) {
	
	     var tempArrStatus = null;
	
	     var newTempArr = [];
	
	     if (tempArr instanceof Array) {
	
	         tempArrStatus = 'array';
	
	     } else if (typeof tempArr == 'string' || typeof tempArr == 'number') {
	
	         tempArr = JSON.stringify(tempArr).replace(/[\"|\']/g, "");
	
	         tempArr = tempArr.split('');
	
	         tempArrStatus = 'string';
	
	     } else { return false; }
	     
	     
	     for (let i in tempArr) {
	
	         if(i == 0){ newTempArr[0] = tempArr[0]; }
	
	         for (let j in newTempArr) {
	
	             if (JSON.stringify(tempArr[i]) == JSON.stringify(newTempArr[j])) {
	                 break;
	             }
	
	             if (j == newTempArr.length - 1) {
	                 newTempArr.push(tempArr[i]);
	             }
	         }
	     }
	
	     if(tempArrStatus == 'string'){ return newTempArr.join('')}
	
	     return newTempArr;
	 }
	 
	
	 // 函数调用示例
	
	 var tempArr = [1, 5, 5, 5, 5, 5656, 6, 3, 5, 1, 69, 89, 89, 1, 568, 36, 99];
	
	 console.log(remRepeat(tempArr));
	
	 // 支持数组里面json对象比较
	
	 var tempArrObj = [1, 5, 5, 5, 5, 5656, 6, { name: '张三' }, { name: '李四' }, 3, 5, { name: '王五' }, 1, 69, { name: '张三' }, 89, { name: '李四' }];
	
	 console.log(remRepeat(tempArrObj));
	
	 // 支持去重字符串或者数字
	
	 var tempStr = '张三123李四12586111王五999999张三';
	
	 var tempNum = 12312586111;
	
	 console.log(remRepeat(tempStr));
 	 console.log(remRepeat(tempNum));

【简洁版】缺点是不能比较json对象

代码：

	/*
	数组去重函数
	@param tempArr 需要去重的数组，支持字符和数字串去重
	@param result 这个是返回值，不用传入
	*/
	function remRepeat(tempArr,result=[]){
	    for(let i in tempArr){
	        if(result.indexOf(tempArr[i]) == -1){
	          result.push(tempArr[i])
	        }
	    }
	    return typeof tempArr == "string" ? result.join('') : result;
	}       

	// 函数调用示例
	var tempArr = [1, 5, 5, 5, 5, 5656, 6, 3, 5, 1, 69, 89, 89, 1, 568, 36, 99];
	console.log(remRepeat(tempArr));

	// 支持去重字符串或者数字
	var tempStr = '张三123李四12586111王五999999张三';
	console.log(remRepeat(tempStr));