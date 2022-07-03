# js中用setTimeout方式实现setinterval功能

当初写这个功能主要是 **setinterval** 实现不了我的需求。我对执行次数不确定，而且还要规定执行次数。

对此功能 做了修改：

1、s 参数是间隔多久执行，单位毫秒

2、n为执行次数，如果想 一直执行传入数字0就可以了

3、fn为你要执行代码块，是一个回调函数

	function _setInterval(s, n, fn) {
	    let tempIndex = 0;
	    let timeOut = (s, fn) => {
	        setTimeout(() => {
	        if (n && n <= tempIndex) { return false; }
	            tempIndex++;
	            fn();
	            timeOut(s, fn);
	        }, s)
	    }
	    timeOut(s, fn);
	}
	
	_setInterval(1000, 5, () => { console.log("hello world!") })