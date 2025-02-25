from DToolslib import StaticEnum


class VersionEnum(StaticEnum):
    class FileFlags:
        VS_FF_UNKNOWN = 0x00000000  # 未指定标志. 
        VS_FF_DEBUG = 0x00000001  # 该文件包含调试信息, 或者在启用调试功能的情况下进行编译. 
        VS_FF_PRERELEASE = 0x00000002  # 该文件是开发版本, 而不是商业发布的产品. 
        VS_FF_PATCHED = 0x00000004  # 该文件已修改, 与同一版本号的原始发货文件不同. 
        VS_FF_PRIVATEBUILD = 0x00000008  # 文件不是使用标准发布过程生成的.  如果设置了此标志,  StringFileInfo 结构应包含 PrivateBuild 条目. 
        VS_FF_INFOINFERRED = 0x00000010  # 文件的版本结构是动态创建的;因此, 此结构中的某些成员可能为空或不正确.  切勿在文件的 VS_VERSIONINFO 数据中设置此标志. 
        VS_FF_SPECIALBUILD = 0x00000020  # 该文件由原始公司使用标准发布过程生成, 但是相同版本号的正常文件的变体.  如果设置了此标志,  StringFileInfo 结构应包含 SpecialBuild 条目. 

    class FileOS:
        VOS_UNKNOWN = 0x00000000  # 系统不知道为其设计文件的操作系统. 
        VOS_DOS = 0x00010000  # 该文件是为 MS-DOS 设计的. 
        VOS_NT = 0x00040000  # 该文件是为 Windows NT 设计的. 
        VOS__WINDOWS16 = 0x00000001  # 该文件专为 16 位 Windows 设计. 
        VOS__WINDOWS32 = 0x00000004  # 该文件专为 32 位 Windows 设计. 
        VOS_OS216 = 0x00020000  # 该文件专为 16 位 OS/2 设计. 
        VOS_OS232 = 0x00030000  # 该文件专为 32 位 OS/2 设计. 
        VOS__PM16 = 0x00000002  # 该文件专为 16 位演示文稿管理器设计. 
        VOS__PM32 = 0x00000003  # 该文件专为 32 位演示文稿管理器设计. 

    class FileType:
        VFT_UNKNOWN = 0x00000000  # 系统不知道文件类型. 
        VFT_APP = 0x00000001  # 文件包含一个应用程序. 
        VFT_DLL = 0x00000002  # 文件包含 DLL. 
        VFT_DRV = 0x00000003  # 文件包含设备驱动程序.  如果 dwFileTypeVFT_DRV,  则 dwFileSubtype 包含驱动程序的更具体说明. 
        VFT_FONT = 0x00000004  # 文件包含字体.  如果 dwFileTypeVFT_FONT,  则 dwFileSubtype 包含字体文件的更具体说明. 
        VFT_VXD = 0x00000005  # 该文件包含一个虚拟设备. 
        VFT_STATIC_LIB = 0x00000007  # 文件包含静态链接库. 

    class FileSubtype:
        VFT2_UNKNOWN = 0x00000000  # 系统未知驱动程序类型. 
        VFT2_DRV_PRINTER = 0x00000001  # 文件包含打印机驱动程序. 
        VFT2_DRV_KEYBOARD = 0x00000002  # 文件包含键盘驱动程序. 
        VFT2_DRV_LANGUAGE = 0x00000003  # 文件包含语言驱动程序. 
        VFT2_DRV_DISPLAY = 0x00000004  # 文件包含显示驱动程序. 
        VFT2_DRV_MOUSE = 0x00000005  # 文件包含鼠标驱动程序. 
        VFT2_DRV_NETWORK = 0x00000006  # 文件包含网络驱动程序. 
        VFT2_DRV_SYSTEM = 0x00000007  # 文件包含系统驱动程序. 
        VFT2_DRV_INSTALLABLE = 0x00000008  # 文件包含可安装的驱动程序. 
        VFT2_DRV_SOUND = 0x00000009  # 该文件包含声音驱动程序. 
        VFT2_DRV_COMM = 0x0000000A  # 文件包含通信驱动程序. 
        VFT2_DRV_VERSIONED_PRINTER = 0x0000000C  # 文件包含版本控制打印机驱动程序. 

    class FileFont:
        VFT2_UNKNOWN = 0x00000000  # 系统未知字体类型. 
        VFT2_FONT_RASTER = 0x00000001  # 文件包含光栅字体. 
        VFT2_FONT_VECTOR = 0x00000002  # 文件包含矢量字体. 
        VFT2_FONT_TRUETYPE = 0x00000003  # 文件包含 TrueType 字体. 

    class LangID:
        Albanian = 0x041C  # 阿尔巴尼亚语
        Arabic = 0x0401  # 阿拉伯语
        Bahasa = 0x0421  # 印尼语
        Belgian_Dutch = 0x0813  # 比利时荷兰语
        Belgian_French = 0x080C  # 比利时法语
        Bulgarian = 0x0402  # 保加利亚语
        Canadian_French = 0x0C0C  # 加拿大法语
        Castilian_Spanish = 0x040A  # 卡斯蒂利亚西班牙语
        Catalan = 0x0403  # 加泰罗尼亚语
        Croato_Serbian_Latin = 0x041A  # Croato-Serbian (拉丁语)
        Czech = 0x0405  # 捷克语
        Danish = 0x0406  # 丹麦语
        Dutch = 0x0413  # 荷兰语
        Finnish = 0x040B  # 芬兰语
        French = 0x040C  # 法语
        German = 0x0407  # 德语
        Greek = 0x0408  # 希腊语
        Hebrew = 0x040D  # 希伯来语
        Hungarian = 0x040E  # 匈牙利语
        Icelandic = 0x040F  # 冰岛语
        Italian = 0x0410  # 意大利语
        Japanese = 0x0411  # 日语
        Korean = 0x0412  # 韩语
        Norwegian_Bokmal = 0x0414  # 挪威语 Bokmal
        Norwegian_Nynorsk = 0x0814  # 挪威语 尼诺斯克
        Polish = 0x0415  # 波兰语
        Portuguese_Brazil = 0x0416  # 葡萄牙语(巴西)
        Portuguese_Portugal = 0x0816  # 葡萄牙语(葡萄牙)
        Rhaeto_Romanic = 0x0417  # 罗曼语
        Romanian = 0x0418  # 罗马尼亚语
        Russian = 0x0419  # 俄语
        Serbo_Croatian_Cyrillic = 0x081A  # 塞尔维亚-克罗地亚语(西里尔文)
        Simplified_Chinese = 0x0804  # 简体中文
        Slovak = 0x041B  # 斯洛伐克语
        Spanish_Mexico = 0x080A  # 西班牙语(墨西哥)
        Swedish = 0x041D  # 瑞典语
        Swiss_French = 0x100C  # 瑞士法语
        Swiss_German = 0x0807  # 瑞士德语
        Swiss_Italian = 0x0810  # 瑞士意大利语
        Thai = 0x041E  # 泰语
        Traditional_Chinese = 0x0404  # 繁体中文
        Turkish = 0x041F  # 土耳其语
        Urdu = 0x0420  # 乌尔都语
        UK_English = 0x0809  # 英国英语
        US_English = 0x0409  # 美国英语

    class CharsetID(StaticEnum):
        ANSI = 0x0000  # 7 位 ASCII
        Arabic = 0x04E8  # 阿拉伯语
        Big5 = 0x03B6  # 台湾 (Big5)
        Cyrillic = 0x04E3  # 西里尔语
        Greek = 0x04E5  # 希腊语
        Hebrew = 0x04E7  # 希伯来语
        Latin_2 = 0x04E2  # 拉丁语-2 (东欧)
        Multilingual = 0x04E4  # 多语言
        SHIFT_JIS_X_0208 = 0x03A4  # 日本 (JIS X-0208)
        SHIFT_KSC_5601 = 0x03B5  # 韩国 (KSC 5601)
        Turkish = 0x04E6  # 土耳其语
        Unicode = 0x04B0  # Unicode
