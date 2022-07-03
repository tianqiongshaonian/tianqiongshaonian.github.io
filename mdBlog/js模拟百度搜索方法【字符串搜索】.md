# js模拟百度搜索方法【字符串搜索】

【功能】：搜索字符串进行排序，支持数字和字符串搜索。这里排序算法采用了【插入排序】。

【注意】：不建议在数组中传入json对象，否者会被强制转换为字符串。

【代码示例】

【注意事项】内层json名字不建议外层json名称重名，否者内层json对象会覆盖外层json对象

	/*
	    函数名：strSearch 模拟百度搜索工能
	    参数：tempArr 需要搜索的数组, 数组中的值建议为字符串
	    参数：searchVal 搜索数组中的值，支持模糊搜索，值为字符串
	*/
	
	function strSearch(tempArr, searchVal) {
	
	    var newTempArr = [];
	    var tempArrLength = tempArr.length;
	
	    // 取出包含 searchVal 的值，放入数组中
	    for (var k = 0; k < tempArrLength; k++) {
	        // 如果不是string 则转换为字符串
	        typeof tempArr[k] != 'string' && (tempArr[k] = JSON.stringify(tempArr[k]));
	        if (tempArr[k].indexOf(searchVal) != -1) {
	            newTempArr.push(tempArr[k]);
	        } else {
	            continue;
	        }
	    }
	
	    tempArrLength = newTempArr.length;
	
	    // 通过字符串长度排序，最短的在最前面，这里采用了插入排序算法
	    for (var i = 0; i < tempArrLength; i++) {
	        var minIndex = i;
	        for (var j = i; j < tempArrLength; j++) {
	            if (newTempArr[j].length < newTempArr[minIndex].length) { //找到最小的数
	                minIndex = j; //将最小数的索引保存
	            }else{ continue;}
	
	        }
	        var temp = newTempArr[minIndex];
	        newTempArr[minIndex] = newTempArr[i];
	        newTempArr[i] = temp;
	    }
	
	    return newTempArr;
	}
	
	// 函数调用示例
	var tempArr = ['王五', '章守法的发', 81568888888888888888, 8, 88, 818, '88888888899999999', 1888111, '章守9法888888888的发', 'fafadfadfaf', 'fadfa', '5', '898989', 'fafadfadfaf', 'fasdfa', 'fafadfadfaf', 'rqerq', 'fafadfadfaf', '章守法88rqerq8888888的发', 'fafadfadfaf'];
	var searchVal = '88';
	
	console.log(strSearch(tempArr, searchVal))

js 模拟百度搜索方法【简洁版】

	/*
	    函数名：strSearch 模拟百度搜索工能
	    参数：tempArr 需要搜索的数组, 数组中的值建议为字符串
	    参数：searchVal 搜索数组中的值，支持模糊搜索，值为字符串
	*/
	
	function strSearch(tempArr, searchVal) {
	    
	    var newTempArr = [];
	        // 取出包含 searchVal 的值，放入数组中并且通过长度排序
	        newTempArr = tempArr.filter(function(v){
	            typeof v != 'string' && (v = JSON.stringify(v));
	            return (v.indexOf(searchVal) != -1);
	        }).join(',').split(',').sort(function(a,b){return a.length - b.length;});
	        
	    return newTempArr;
	}
	
	// 函数调用示例
	var tempArr = ['王五', '章守法的发', 81568888888888888888, 8, 88, 818, '88888888899999999', 1888111, '章守9法888888888的发', 'fafadfadfaf', 'fadfa', '5', '898989', 'fafadfadfaf', 'fasdfa', 'fafadfadfaf', 'rqerq', 'fafadfadfaf', '章守法88rqerq8888888的发', 'fafadfadfaf'];
	var searchVal = '88';
	console.log(strSearch(tempArr, searchVal))