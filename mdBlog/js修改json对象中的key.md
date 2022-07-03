# js修改json对象中的key

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
	        /*
	            递归替换对象中的key
	            oldKey 旧的key
	            newKey 新的key
	            repObj 替换的对象
	        */
	 
	         function replaceKey(oldKey,newKey,repObj){
	            for(let i in repObj){
	                if(repObj[i] instanceof Object){
	                    replaceKey(oldKey,newKey,repObj[i]);
	                }else{
	                    typeof oldKey == 'string' &&
	                    typeof newKey == 'string' && 
	                    i == oldKey &&
	                    (repObj[newKey] = repObj[i],delete repObj[i]);
	                    if(oldKey instanceof Array && newKey instanceof Array && (oldKey.length == newKey.length)){
	                        for(let i1 in oldKey){
	                            oldKey[i1] == i && (repObj[newKey[i1]] = repObj[i],delete repObj[i]);
	                        }
	                    }
	                }
	            }
	            return repObj;
	        }
	        // 调用示例
	        let tempData = [{"id":53,"group_id":1,"area_id":1,"pid":0,"name":"asd","number":"12","sort":0,"created_at":"2020-10-12 13:53","child":[{"id":54,"group_id":1,"area_id":1,"pid":53,"name":"aaaa1","number":"2323","sort":0,"created_at":"2020-10-12 14:01","child":[{"id":56,"group_id":1,"area_id":1,"pid":54,"name":"qqww","number":"2222","sort":0,"created_at":"2020-10-12 14:02"}]}]},{"id":62,"group_id":1,"area_id":1,"pid":0,"name":"总经办","number":"","sort":1,"created_at":"1970-01-01 08:00","child":[{"id":84,"group_id":1,"area_id":1,"pid":62,"name":"dsfd","number":"总经办","sort":0,"created_at":"2020-12-04 15:20"}]},{"id":63,"group_id":1,"area_id":1,"pid":0,"name":"市场部","number":"","sort":2,"created_at":"1970-01-01 08:00"}];
	       
	        // console.log('原始数据-----------',tempData)
	        // console.log('单个修改-----------',replaceKey('pid','parentId',tempData)); 
	        console.log('多个修改-----------',replaceKey(['group_id','area_id'],['groupId','areaId'],tempData)); 
	      </script>
	</body>
	</html>
 