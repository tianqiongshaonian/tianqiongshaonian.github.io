# vue限制用户只能输入浮点数

	<!DOCTYPE html>
	<html lang="en">
	
	<head>
	    <meta charset="UTF-8">
	    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <title>限制用户只能输入整数或浮点数金额</title>
	    <script src="./vue.js"></script>
	    <style>
	        .input-box{
	            width: 500px;
	            height: 60px;
	            margin-left: 30%;
	            margin-top: 20%;
	            font-size: 28px;
	        }
	    </style>
	</head>
	
	<body>
	    <div id="app">
	        <input v-model="inputMoney" placeholder="只能输入金额" class="input-box">
	    </div>
	
	    <script>
	        var app = new Vue({
	            el: '#app',
	            data: {
	                inputMoney: ''
	            },
	
	            watch: {
	                inputMoney(newVal, oldVal) {
	                    let reg = /^(\d{0,5})(\.(\d{0,2}))?$/g;
	                    if (!reg.test(newVal)) {
	                        if (newVal == '') {
	                            this.inputMoney = '';
	                            return;
	                        }
	                        this.inputMoney = oldVal;
	                    } else {
	                        this.inputMoney = newVal;
	                    }
	                },
	                
	            },
	            methods: {
	
	            }
	        })
	
	    </script>
	</body>
	
	</html>