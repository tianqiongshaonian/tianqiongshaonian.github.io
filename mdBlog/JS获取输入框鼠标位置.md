# JS获取输入框鼠标位置

代码调用示例（支持IE）：

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <title>Document</title>
	</head>
	<body>
	    <textarea name="" id="txt" cols="30" rows="10" onclick="userClick()" oninput="Vchange()" value="测试文本"></textarea>
	    <script>
	        function userClick(){
	            console.log('用户点击------------',getPosition('txt'))
	        }
	        function Vchange(){
	            console.log('用户输入------------',getPosition('txt'))
	        }
	
	        // 获取input，textarea焦点位置
	        function getPosition (id) {
	            let oElement = document.getElementById(id);
	            let cursorPos = 0;
	            if (document.selection) { //IE
	                var selectRange = document.selection.createRange();
	                selectRange.moveStart('character', -oElement.value.length);
	                cursorPos = selectRange.text.length;
	            } else if (oElement.selectionStart || oElement.selectionStart == '0') {
	                cursorPos = oElement.selectionStart;
	            }
	            return cursorPos;
	        }
	        
	      </script>
	</body>
	</html>
 