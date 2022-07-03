# 微信小程序将异步api改成同步处理方法

此处为测试接口 ，请自行更换成你的请求地址 和 参数。

js 代码如下：

	Page({
	  data: {
	  },
	  
	  onLoad(){
	    let that = this;
	    that.userInfo();
	  },
	  
	  // 封装promise 请求
	  postData(url, param) {
	    return new Promise((resolve, reject) => {
	      wx.request({
	        url,
	        method: 'POST',
	        data: param,
	        success(res) {
	          resolve(res)
	        },
	        fail(res) {
	          reject(res)
	        }
	      })
	    })
	  },
	  // 登录处理
	  login() {
	    return new Promise((resolve, reject) => {
	      wx.login({
	        success: function (res) {
	          resolve(res)
	        }, fail(res) {
	          reject(res)
	        }
	      })
	    })
	  },
	  // 同步处理
	  async userInfo() {
	    let that = this;
	    let accountInfo = wx.getAccountInfoSync();
	    let loginData = await that.login();
	    console.log(111111)
	    let loginParam = {
	      js_code: loginData.code,
	      appid: accountInfo.miniProgram.appId,
	    };
	    console.log(222222)
	    let loginpostData = await that.postData('https://baidu.com/Id.do', loginParam); // 请求1 ,此处未测试接口，请自行修改
	    console.log(333333)
	
	    let userInfoData = await that.postData('https://baidu.com/OpenId.do', userInfoParam); //请求2，此处未测试接口，请自行修改
	    console.log(4444444)
	
	    return loginpostData
	
	  }
	})