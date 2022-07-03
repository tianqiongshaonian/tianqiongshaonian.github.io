// 文章类型 technology 文章列表 ，title 文章列表标题
var G_articleType = [
    {
        list: [],
        title: '技术'
    },
    {
        list: [],
        title: '软件'
    },
    {
        list: [],
        title: '笔记'
    }
];

// 所有的文章, txtType 文章类型， value 文章标题
var G_data = [
    {
        articleType: '笔记',
        value: ' 开源压力测试工具（siege）',
        id: 39,
    },
    {
        articleType: '技术',
        value: '递归检索对象中是否包含某个值',
        id: 1,
    },
    {
        articleType: '技术',
        value: '模拟textarea效果高度自适应',
        id: 2,
    },
    {
        articleType: '软件',
        value: '批量修改文件名方法',
        id: 3,
    },
    {
        articleType: '技术',
        value: '前端开发之防抖和节流函数',
        id: 4,
    },
    {
        articleType: '技术',
        value: '前端限制用户只能输入手机号码（中国手机号码）',
        id: 5,
    },
    {
        articleType: '技术',
        value: '前端限制用户只能输入邮箱格式',
        id: 6,
    },
    {
        articleType: '技术',
        value: '前端之最优雅的模板引擎实现',
        id: 7,
    },
    {
        articleType: '技术',
        value: '微信小程序监听属性变化方法',
        id: 8,
    },
    {
        articleType: '技术',
        value: '微信小程序将异步api改成同步处理方法',
        id: 9,
    },
    {
        articleType: '技术',
        value: '微信小程序优惠券领取弹框组件',
        id: 10,
    },
    {
        articleType: '技术',
        value: '微信小程序之数组对象排序【冒泡排序】',
        id: 11,
    },
    {
        articleType: '技术',
        value: '微信小程序自定义数据加载中',
        id: 12,
    },
    {
        articleType: '技术',
        value: '小程序绘制曲线图',
        id: 13,
    },
    {
        articleType: '技术',
        value: 'css 元素垂直水平居中方法',
        id: 14,
    },
    {
        articleType: '技术',
        value: 'el-calendar组件静止用户点击灰色日历',
        id: 15,
    },
    {
        articleType: '技术',
        value: 'el-tree生成唯一索引，通过索引值回溯到父级',
        id: 16,
    },
    {
        articleType: '笔记',
        value: 'frp远程桌面部署',
        id: 17,
    },
    {
        articleType: '技术',
        value: 'javaScript对调两个变量的方法有那些？',
        id: 18,
    },
    {
        articleType: '技术',
        value: 'js扁平化json和array【递归方式处理】',
        id: 19,
    },
    {
        articleType: '技术',
        value: 'js获取当前月份的开始日期和结束日期',
        id: 20,
    },
    {
        articleType: '技术',
        value: 'JS获取输入框鼠标位置',
        id: 21,
    },
    {
        articleType: '技术',
        value: 'js获取页面路径的参数方法',
        id: 22,
    },
    {
        articleType: '技术',
        value: 'js计算两个经纬度之间的距离',
        id: 23,
    },
    {
        articleType: '技术',
        value: 'js模拟百度搜索方法【字符串搜索】',
        id: 24,
    },
    {
        articleType: '技术',
        value: 'js数据加密解密方法实现',
        id: 25,
    },
    {
        articleType: '技术',
        value: 'js通过出生年月计算年龄方法',
        id: 26,
    },
    {
        articleType: '技术',
        value: 'js修改json对象中的key',
        id: 27,
    },
    {
        articleType: '技术',
        value: 'js证件信息脱敏处理方法',
        id: 28,
    },
    {
        articleType: '技术',
        value: 'js之数组对象排序【选择排序法】',
        id: 29,
    },
    {
        articleType: '技术',
        value: 'js之json序列化【解决对象引用类型方法】',
        id: 30,
    },
    {
        articleType: '技术',
        value: 'js中用setTimeout方式实现setinterval功能',
        id: 31,
    },
    {
        articleType: '软件',
        value: 'ps批量压缩图片脚本源码',
        id: 32,
    },
    {
        articleType: '软件',
        value: 'vscode修改前端代码常用正则表达式',
        id: 33,
    },
    {
        articleType: '软件',
        value: 'vscode中批量删除console.log',
        id: 34,
    },
    {
        articleType: '技术',
        value: 'vue限制用户只能输入浮点数',
        id: 35,
    },
    {
        articleType: '笔记',
        value: '图片压缩工具（在线压缩）',
        id: 36,
    },
    {
        articleType: '笔记',
        value: '常用的开源软件',
        id: 37,
    },
    {
        articleType: '技术',
        value: 'js字符串去重方法支持数组，数字',
        id: 38,
    },

]



// 文章归类处理
for (let i in G_articleType) {
    if (!G_articleType[i].list) {
        G_articleType[i].list = [];
    }
    for (let j in G_data) {
        if (G_articleType[i].title.replace(/\s/g, '').toLowerCase() == G_data[j].articleType.replace(/\s/g, '').toLowerCase()) {
            G_data[j].href = './blog/' + G_data[j].id + '.html'
            G_articleType[i].list.push(G_data[j])
        }
    }
}