# el-tree生成唯一索引，通过索引值回溯到父级

el-tree 选择值必须是唯一索引

我们可以通过索子元素的索引还原父级的索引值，从而达到展开的效果

![](../images/6251920174592.png)

代码如下：
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <title>Document</title>
	</head>
	<body>
	    <script>
	
	        let treedata = [{"id":53,"group_id":1,"area_id":1,"pid":0,"name":"asd","number":"12","sort":0,"created_at":"2020-10-12 13:53","child":[{"id":54,"group_id":1,"area_id":1,"pid":53,"name":"aaaa1","number":"2323","sort":0,"created_at":"2020-10-12 14:01","child":[{"id":56,"group_id":1,"area_id":1,"pid":54,"name":"qqww","number":"2222","sort":0,"created_at":"2020-10-12 14:02"}]}]},{"id":62,"group_id":1,"area_id":1,"pid":0,"name":"总经办","number":"","sort":1,"created_at":"1970-01-01 08:00","child":[{"id":84,"group_id":1,"area_id":1,"pid":62,"name":"dsfd","number":"总经办","sort":0,"created_at":"2020-12-04 15:20"}]},{"id":63,"group_id":1,"area_id":1,"pid":0,"name":"市场部","number":"","sort":2,"created_at":"1970-01-01 08:00"}];
	        
	        // 给 tree 生成唯一索引
	        function setTreeIndex(tempArr,key,flag){
	            for(let i in tempArr){
	                if(tempArr[i] instanceof Object){
	                    if(tempArr[i] instanceof Object && !(tempArr[i] instanceof Array)){
	                        tempArr[i].localLevelId = flag + '-' + tempArr[i][key];
	                    }
	                    tempArr[i] = setTreeIndex(tempArr[i],key,tempArr.localLevelId || '');
	                }
	            }
	            return tempArr;
	        }
	
	        setTreeIndex(treedata,'id','group')
	        console.log(treedata)
	
	        // 把树里面所有的索引找出来
	        function getTreeIndex(tempArr,key,reslut=[]){
	            for(let i in tempArr){
	                if(tempArr[i] instanceof Object){
	                    getTreeIndex(tempArr[i],key,reslut);
	                }else{
	                    if(i == 'localLevelId'){
	                        reslut.push(tempArr[i]);
	                    }
	                }
	            }
	            return reslut;
	        }
	
	        let tempTreeArr = getTreeIndex(treedata,'localLevelId');
	        console.log(tempTreeArr)
	
	        // 还原所有的父级值
	        function reductionIndex(tempArr,Str,reslut=[]){
	            for(let i in tempArr){
	                let tempRes = tempArr[i].split('-');
	                let tempStr = Str;
	                for(let j=1; j<tempRes.length; j++){
	                    tempStr += ('-' + tempRes[j]);
	                    if (reslut.indexOf(tempStr) == -1) {
	                        reslut.push(tempStr);
	                    }
	                }
	            }
	            return reslut;
	        }
	        let reductionV =  ["group-53-54-56", "group-53-54-56-58","group-53-54", "group-53", "group-62-84","group-62-84-258", "group-62-84-25-19-8", , "group-62", "group-63"];
	        console.log(reductionIndex(reductionV,'group'))
	        
	      </script>
	</body>
	</html>
