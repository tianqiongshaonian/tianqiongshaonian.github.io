# js之数组对象排序【选择排序法】

js之数组对象选择排序法：

【原理】：通过比较首先选出最小的数放在一个位置上，然后在其余的数中选择次小数放在第二个位置，以此类推，直到所有的数有序序列。

	/*
	     函数名：_sortArr
	
	     功能：通过数组中值排序，正向排序，反向排序，采用选择排序
	
	     参数1：tempArr 传入数组
	
	     参数2：传入排序方式，1 从小到大排序 ，-1 从大到小排序 ，其他值则不进行排序
	
	
	 */
	
	
	
	 function _sortArr(tempArr = [], sort_order = 1) {
	
	     var tempArr = JSON.parse(JSON.stringify(tempArr)); // 深赋值一份，保证原来的数组不被改变
	
	     var tempArrLength = tempArr.length;
	
	     for (var i = 0; i < tempArrLength; i++) {
	
	         for (var j = i + 1; j < tempArrLength; j++) {
	
	             if (sort_order == 1) { //排序从小到大
	                 if (tempArr[i] > tempArr[j]) {
	                     var temp = tempArr[i];
	                     tempArr[i] = tempArr[j];
	                     tempArr[j] = temp;
	                 }
	             } else if (sort_order == -1) { // 排序从大到小
	
	                 if (tempArr[i] < tempArr[j]) {
	                     var temp = tempArr[i];
	                     tempArr[i] = tempArr[j];
	                     tempArr[j] = temp;
	                 }
	             } else { // 不排序
	                 return tempArr;
	             }
	
	         }
	
	     }
	
	     return tempArr;
	
	 }
	
	
	 // _sortArr 方法调用示例
	
	 var tempArr = [1, 8, 96, 66666, 2, 3, 5, 68, 567, 888888];
	
	 console.log(_sortArr(tempArr,1)); //从小到大排序
	
	 console.log(_sortArr(tempArr, -1)); //从大到小排序
	
	 console.log(tempArr); // 原始数组



【示例2】：数组对象id排序

	/*
	     函数名：_sortObj
	
	     功能：通过数组中下面的对象排序，正向排序，反向排序，选择排序
	
	     参数1：tempArr 传入数组对象
	
	     参数2：传入排序方式，1 从小到大排序 ，-1 从大到小排序 ，其他值则不进行排序
	
	     参数3：排序的key值
	
	 */
	
	 function _sortObj(tempArr = [], sort_order = 1, key) {
	
	     var tempArr = JSON.parse(JSON.stringify(tempArr)); // 深赋值一份，保证原来的数组对象不被改变
	
	     var tempArrLength = tempArr.length;     
	
	     for (var i = 0; i < tempArrLength; i++) {
	
	         for (var j = i + 1; j < tempArrLength; j++) {
	
	             if (sort_order == 1) { //排序从小到大
	                 if (tempArr[i][key] > tempArr[j][key]) {
	                     var temp = tempArr[i];
	                     tempArr[i] = tempArr[j];
	                     tempArr[j] = temp;
	                 }
	             } else if (sort_order == -1) { // 排序从大到小
	                 if (tempArr[i][key] < tempArr[j][key]) {
	                     var temp = tempArr[i];
	                     tempArr[i] = tempArr[j];
	                     tempArr[j] = temp;
	                 }
	             } else { // 不排序
	                 return tempArr;
	             }
	
	         }
	
	     }
	
	     return tempArr;
	
	 }
	
	 // _sortObj 方法调用示例
	
	 var tempArrObj = [{ id: 265, name: '张山' }, { id: 0, name: '李四' }, { id: 2, name: '王武' }, { id: 3, name: '赵四' }, { id: 5, name: "刘建" }, { id: 9999, name: '万龙' }];
	
	 console.log(_sortObj(tempArrObj, 1, 'id')); //从小到大排序
	
	 console.log(_sortObj(tempArrObj, -1, 'id')); //从大到小排序
	
	 console.log(tempArrObj); // 原始数组对象