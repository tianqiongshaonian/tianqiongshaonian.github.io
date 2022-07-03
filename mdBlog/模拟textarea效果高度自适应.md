# 模拟textarea效果高度自适应

首先来给大家介绍一个属性 **contenteditable 这个属性的功能是把普通元素设置为编辑状态**

	contenteditable 属性指定元素内容是否可编辑
	contenteditable="true"  指定元素是可编辑的
	contenteditable="false" 指定元素是不可编辑的

**注意：当元素中没有设置 contenteditable 属性时，元素将从父元素继承**

	<!DOCTYPE html>
	<html lang="en">
	
	<head>
	    <meta charset="UTF-8">
	    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <title>Document</title>
	    <style>
	
	        /* 设置div样式 */
	        .simulation-textarea {
	            width: 500px;
	            min-height: 20px;
	            max-height: 300px;
	            margin-left: auto;
	            margin-right: auto;
	            padding: 3px;
	            outline: 0;
	            border: 1px solid #a0b3d6;
	            font-size: 12px;
	            line-height: 24px;
	            padding: 2px;
	            word-wrap: break-word;
	            overflow-x: hidden;
	            overflow-y: auto;
	            border-color: rgba(82, 168, 236, 0.8);
	            padding: 10px;
	            border-radius: 5px;
	        }
	        /* 滚动条整体部分 */
	        .simulation-textarea::-webkit-scrollbar{
	            width:5px;
	            height:5px;
	        }
	        /* 滚动条的轨道（里面装有Thumb） */
	        .simulation-textarea::-webkit-scrollbar-track{
	            background: rgb(239, 239, 239);
	            border-radius:2px;
	        }
	        /* 滚动条里面的小方块，能向上向下移动（或往左往右移动，取决于是垂直滚动条还是水平滚动条） */
	        .simulation-textarea::-webkit-scrollbar-thumb{
	            border-radius: 2px;
	            background: #bfbfbf;
	            border-radius:5px;
	        }
	        .simulation-textarea::-webkit-scrollbar-thumb:hover{
	            background: #999;
	        }
	
	
	    </style>
	</head>
	
	<body>
	
	    <div class="simulation-textarea" contenteditable="true"></div>
	
	</body>
	
	</html>

如果想给div 设置焦点效果可以参考以下代码：

	<div tabindex="0"  onfocus='getOnfocus()' onblur='getOnblur()'></div>