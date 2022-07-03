# ps批量压缩图片脚本源码

此脚本可以批量压缩图片，支持的格式有（jpg，gif，png），压缩比例参数可自行设置 pictureQuality  图片的压缩质量。数字范围为1至100。

准备工作：在任意盘符的根目录下新建一个images文件夹，放入你想要压缩的图片。如：E:\images

脚本使用教程

第一步：在桌面或者任意盘符下新建一个 .js 后缀的文件。如：ImgHandle_jpg.js

第二步：将下面的源码复制进去

第三步：打开Photoshop

第四步：选择：文件 –> 脚本 –> 浏览（选择ImgHandle_jpg.js）
	
	var filePath = ""; //图片所在的目录,此目录不能为系统盘，如C

	var pictureQuality = 1; // 图片的压缩质量。数字范围为1至100。
	
	var driveLetter = ["Q:\\", "W:\\", "E:\\", "R:\\", "T:\\", "Y:\\", "U:\\", "I:\\", "O:\\", "P:\\", "A:\\", "S:\\",
	    "D:\\", "F:\\", "G:\\", "H:\\", "J:\\", "K:\\", "L:\\", "Z:\\", "X:\\", "C:\\", "V:\\", "B:\\", "N:\\", "M:\\"
	];
	
	var reg = new RegExp('[.+\.JPEG|.+\.jpg|.+\.jfif|.+\.png|.+\.gif|.+\.JPG]$', 'i');
	
	
	for (var k = 0; k < driveLetter.length; k++) {
	
	    filePath = "images";
	    filePath = driveLetter[k] + filePath;
	
	    //定义一个变量[sampleFolder]，用来表示硬盘某个路径上的文件夹。
	    var samplesFolder = Folder(filePath);
	
	    //定义一个变量[fileList]，用来表示使用[getFiles]命令获得的文件夹下的所有文档。
	    var fileList = samplesFolder.getFiles();
	
	
	    //创建一个for循环，用来遍历[fileList]数组里面的所有文档。
	    for (var i = 0; i < fileList.length; i++) {
	
	
	        if (fileList[i] instanceof File && reg.test(fileList[i])) {
	
	            open(fileList[i]);
	
	            //定义一个变量[document]，用来表示Photoshop当前的活动文档。
	            var document = app.activeDocument;
	
	            //定义一个变量[fileOut]，用来表示导出后的GIF图片路径。
	            var fileOut = new File(fileList[i]);
	
	            //定义一个变量[exportOptionsSaveForWeb]，用来表示导出文档为Web格式的设置属性。
	            var exportOptionsSaveForWeb = new ExportOptionsSaveForWeb();
	
	
	            if (/\.JPEG/.test(fileList[i]) || /\.jpg/.test(fileList[i]) || /\.jfif/.test(fileList[i])) {
	
	                //设置导出文档时，图片将被存储为.jpeg格式。
	                exportOptionsSaveForWeb.format = SaveDocumentType.JPEG;
	
	                //设置导出文档时，图片的压缩质量。数字范围为1至100。
	                exportOptionsSaveForWeb.quality = Number(pictureQuality) || 1;
	
	
	            } else if (/\.png/.test(fileList[i])) {
	
	                //设置导出文档时，图片将被执行PNG-8压缩，如果值为false则执行PNG-24压缩，如果追求速度甚于质量请设置为true。
	                exportOptionsSaveForWeb.PNG8 = true;
	
	
	            } else if (/\.gif/.test(fileList[i])) {
	
	                //设置导出文档时，是否支持文档的透明度。
	                exportOptionsSaveForWeb.transparency = false;
	
	                //设置导出文档时，是否包含文档中内置的颜色档案(即色彩空间配置文件)。
	                exportOptionsSaveForWeb.includeProfile = true;
	
	                //设置导出文档时，有损压缩的程度。
	                exportOptionsSaveForWeb.lossy = 0;
	
	                //设置导出文档时，图片包含的色彩量(256种颜色)。
	                exportOptionsSaveForWeb.colors = 256;
	
	                //设置导出文档时，图片的减色算法为默认值ColorReductionType.SELECTIVE。共有9种压缩算法，详情请查看Photoshop脚本手册。
	                exportOptionsSaveForWeb.colorReduction = ColorReductionType.SELECTIVE;
	
	                //设置导出文档时，图片将被存储为.gif格式。
	                exportOptionsSaveForWeb.format = SaveDocumentType.COMPUSERVEGIF;
	
	                //设置导出文档时，图片的像素抖动值。
	                exportOptionsSaveForWeb.ditherAmount = 0;
	
	                //设置导出文档时，图片的像素抖动类型。抖动类型共有4种，详情请查看Photoshop脚本手册。
	                exportOptionsSaveForWeb.dither = Dither.NOISE;
	
	                //设置导出文档时，图片的调色板的类型。调色板类型共有12种，详情请查看Photoshop脚本手册。
	                exportOptionsSaveForWeb.palette = Palette.LOCALADAPTIVE;
	
	
	            } else {
	
	                //设置导出文档时，图片将被存储为.jpeg格式。
	                exportOptionsSaveForWeb.format = SaveDocumentType.JPEG;
	
	                //设置导出文档时，图片的压缩质量。数字范围为1至100。
	                exportOptionsSaveForWeb.quality = Number(pictureQuality) || 1;
	            }
	
	
	            //调用[document]的[exportDocument]方法，使用上面设置的各种参数，将当前文档导出并转换为gif，png,jpg格式的文档。
	            document.exportDocument(fileOut, ExportType.SAVEFORWEB, exportOptionsSaveForWeb);
	
	
	            //调用[document]对象的[close]方法，关闭文档。[close]方法里的参数保证关闭文档时，不再保存文档。
	            app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
	        } else {
	            continue;
	        }
	
	    }
	}

[**脚本下载地址**](../file/ImgHandle_jpg.zip)