# 自动化测试框架

   * [简述](##简述)
        * [框架使用简述](#框架使用简述)
        * [框架注意事项](#框架注意事项)
   * [公共模块介绍](#公共模块介绍)
        * [common](#common) 
        * [case](#case)
        * [data](#data)
		* [public](#public)
        * [imgs](#imgs)
        * [log](#log)
        * [main](#main)
        * [result](#result)
        * [set](#set)
        * [suite](#suite)
	* [流程介绍](#流程介绍)
		* [流程讲解](#流程讲解)
		* [配置文件讲解](#配置文件讲解)
		* [data文件讲解](#data文件讲解)
		* [case文件讲解](#case文件讲解)
		* [suite文件讲解](#suite文件讲解)
	* [方法解释](#方法解释)
		* [Windows端](#Windows端)
		* [App端](#App端)
		* [Web端](#Web端)
	* [参数注意事项](#参数注意事项)
		* [Windows参数](#Windows参数)
		* [App参数](#App参数)
		* [Web参数](#Web参数)


##简述

###框架使用简述
        
    1.该框架为基于POM/ATM + KDT模型设计的一套持续集成框架.
    
    2.该框架主要用于Web, App, Widnows端应用的UI自动化测试.
    
    3.该框架一个完整流程为: 从远端(Git仓库)拉取测试数据 --> 本地运行生成报告 --> 通过邮箱以及钉钉通知接收人;从而达到持续集成的目的.  
    
    4.名词解释: 
        (1) POM: Page Object Moduel, 指将一个页面当作一个对象; 对该对象中每个可以互动的元素赋予一个独立的识别特征.
         
        (2) ATM: Activity Testing Moduel, 指将一个测试流程当作一个对象; 对该对象中每个可以互动的元素赋予一个独立的识别特征.
        
        (3) KDT: Keyword Driver Test, 指将测试数据通过关键字的方式读取进行测试.
        
###框架注意事项

    1.该框架建议使用python 3.6.x版本; 3.8.x版本不支持windows端测试.
    
    2.所需第三方库: pytest, pytest-html, pytest-order, uiautomation, uiautomator2, selenium, git-python, pillow, opencv-python
	
	3.该框架定义一个测试用例由:测试数据(data), 测试基本动作(case), 测试套件(suite)组成. 
	
	4.App元素定位建议使用 weditor库, 具体方法 -> adb连接设备(如'adb connect 127.0.0.1:7555'), 然后cmd中运行'python -m uiautomator2 init', 最后cmd运行'python -m weditor'将会打开一个web页面, 注意该cmd窗体不要关闭.
    
	5.windows元素定位使用的是windowsSDK中的Inspect.
##公共模块介绍

###common

	1.该路径下存放整个框架的底层代码以及入口模块; 所有的基本动作都在这里定义. 除Web方向外都由'Main_Unit'以及'Base_Unit'组成;(Web方向多一个'Support_Unit')
	
	2.Base_Unit: 整个框架的底层代码, 用于封装各个动作.
	
	3.Main_Unit: 整个框架的入口模块, 用于调用框架各个模块完成一次完整的流程.
	
	4.Support_Unit: Web方向独有的一个模块, 主要用于对Base_Unit的辅助支持; 其他方向的对应功能已经整合入Base_Unit.
	
###public

	1.该路径下存在整个框架的辅助模块, 一个测试的"前中后"中'前', '后'阶段在这里完成. 除App方向外由'Data_Unit', 'Dingding_Unit', 'Git_Unit', 'Logging_Unit', 'Mail_Unit' 以及'Setting_Unit'组成;(App方向多'Decorator_Unit'以及'Relay_Unit')
	
	2.Data_Unit: 读取组装测试数据的模块.
	
	3.Dingding_Unit: 负责编辑并发送测试完成通知到钉钉群.
	
	4.Git_Unit: 负责在测试开始前从远程仓库下载测试用例并初始化环境.
	
	5.Logging_Unit: 负责编辑并记录日志记录在控制台, 日志文件中输出.
	
	6.Mail_Unit: 发送邮件模块, 负责组装测试报告为邮件并发送到指定邮箱.
	
	7.Setting_Unit: 负责读取配置文件.
	
	8.Decorator_Unit: 负责存放自定义装饰器的模块.
	
	9.Relay_Unit: App方向测试中负责调用测试类型的模块.

###main

	1.该路径下仅有'Main'文件, 调用整个框架的主模块.
	
###case

	1.存放测试用例组成中测试基本动作的路径, 一般命名方式为case_xxx:Case_Xxx.
	
###data

	1.存放测试用例组成中测试数据的路径, 仅支持csv格式的数据源.

###suite

	1.存放测试用例组成中测试套件的路径, 一般命名方式为test_xxx:Test_Xxx.
	
###imgs

	1.用于存放错误截图的路径.

###log

	1.用于存放用例日志, 测试日志的路径.
	
###result
	1.用于存放html格式测试报告的路径.

###set
	1.用于存放配置文件的路径.

##流程介绍

###流程讲解

我们框架都是通过调用main路径下的'Main'文件完成的, 该文件源码:
```python
# 实例化Main以及设置模块
M = Main_Base()
S = Set() # Set = Setting_Unit
# 克隆测试数据
M.git_clone(S.git_addr)
# 开始测试
M.run()
# 构建邮件并发送
M.build_mail(S.sender, S.receivers_m, S.sender_name, S.title_m, S.content_m, S.smtp_addr, S.smtp_user, S.smtp_passwd)
# 构建钉钉消息
M.build_ding_msg(S.title_d, S.content_d, S.target_url, S.receivers_d)
# 善后清理
M.clear()
```
首先, 我们在实例化'Main'模块与'Set'模块中, 就完成了对配置文件的读取; 我们可以看一小段'Set'文件的源码:
```python
    def __init__(self):
        """
        读取配置文件
        """
        cfg = ConfigParser()
        cfg.read(f"{self.set_folder}/Setting.ini", encoding="utf-8")

        # git
        self.git_addr = cfg.get("GIT", "git_addr")
```
通过观察我们不难发现, 在'Set'被实例化的时候就调用'__init__'方法对配置文件完成读取.

现在我们可以开始从远程端下载测试数据, 即'M.git_clone(S.git_addr)'; 其中S.git_addr是读取的配置文件中远程仓库的地址. 该方法的源码:
```python
 def git_clone(self, url):
        Git_Base(url)
```
在这里原来我们是直接调用Git类, 那么我们调用的Git类代码:
```python
 def __init__(self, url):
        """
        初始化本地环境并克隆测试数据
        Args:
            url: 远程库地址
        """

        # 如果指定远程库 开始克隆
        Log(Set.history_log, "info", "正在从远程库下载数据......")
        try:
            # 如果suite文件夹存在 清空suite
            if os.path.exists(Set.suite_folder):
                for file in os.listdir(Set.suite_folder):
                    if file != "__pycache__":
                        os.remove(f"{Set.suite_folder}/{file}")
						...
						...
	
            Log(Set.history_log, "info", "下载完毕, 准备开始测试......")

        except GitCommandError:
            Log(Set.history_log, "warning", "下载测试数据出错, 请检查地址是否正确/本地是否已经存在测试数据.")
            sys.exit()
```
原来'Git'也和之前的'Set'一样, 在我们实例化它的时候就调用构造方法开始清空目录, 完成数据的下载并日志写入我们的下载操作. 注意这里except捕获的错误, 一般由远程仓库地址不正确引起, 建议使用http(s)格式的地址.

回到正题, 现在我们有了测试三件套(数据, 动作, 套件)可以开始测试了; 即'M.run()'; 该方法源码:
```python
    def run(self):
        """
        开启测试
        """
        Log(Set.history_log, "info", "开始测试......")

        pytest.main(
            [f'{Set.suite_folder}', '-q', '--tb=no', f'--html={Set.result_folder}/report.html',
             '--self-contained-html'])

        Log(Set.history_log, "info", "所有测试完成.")
```
在这里, 我们发现该方法由两条很普通的记录日志信息以及pytest.main方法构成; 而这段pytest.main的含义为: "快速测试(-q), suite目录下所有test_开头文件中test_开头类的test_开头的方法(f'{Set.suite_folder}'), 并且输出测试结果为html报告到result目录下(f'--html={Set.result_folder}/report.html',
'--self-contained-html']" ------------> 也就是, 测试所有用例并生成报告的意思.

完成测试后可以准备后续报告事宜了, 首先我们先构造报告邮件'M.build_mail(S.sender, S.receivers_m, S.sender_name, S.title_m, S.content_m, S.smtp_addr, S.smtp_user, S.smtp_passwd)'; 其中各个参数含义我们可以看源码中该方法的注释:
```python
    def build_mail(self, sender, receivers, sender_name, title, plain_message, smtp_server, smtp_user, smtp_passwd):
        """
        构造邮件
        Args:
            sender: 发送者
            receivers: 接收者 -> list
            sender_name: 发送者姓名
            title: 标题
            plain_message: 正文内容
            smtp_server: smtp服务器地址 - 127.0.0.1:1080
            smtp_user: 登录smtp服务器的用户名
            smtp_passwd: 登录smtp服务器的密码

        Returns:

        """
```
需要注意的是, 接收者需要是一个列表, 而这些参数都是从配置文件中读取的, 即在'Set'被实例化的时候就已经获取到了.

接着我们也要构造钉钉的通知消息'M.build_ding_msg(S.title_d, S.content_d, S.target_url, S.receivers_d)', 同理接收者也是个列表, 数据来源也是配置文件.

最后我们执行'M.clear()'将环境初始化即完整的进行了一次测试流程了, 该方法源码:
```python
    def clear(self):
        """
        将环境清理到初始化的状态
        Returns:

        """
        for file in os.listdir(Set.log_folder):
            if "log" in file:
                os.remove(f"{Set.log_folder}/{file}")

        for file in os.listdir(Set.img_folder):
            if "png" in file:
                os.remove(f"{Set.img_folder}/{file}")

        for file in os.listdir(Set.result_folder):
            if "html" in file:
                os.remove(f"{Set.result_folder}/{file}")

        if os.path.exists(Set.temp_folder):
            os.popen(f"rd/s/q {Set.temp_folder}")
```
原理就是根据每个路径下文件的特殊特征进行删除工作, 保证每个目录和测试开始前一样干净就行了.

###配置文件讲解

配置文件, 即set目录下的'Setting.int'文件; 一个标准的配置文件包含:
```python
[GIT]
; git_addr -> 远端测试数据存放的git地址
git_addr = https://github.com/sabersame/web.git
[MAIL]
; receivers -> 接收者列表 如 [ni@eastedu.com, wo@eastedu.com]
; smtp_addr -> smtp服务器地址 如 smtp.qq.com:233
; smtp_user & passwd -> 登录smtp服务器的用户名以及密码
sender = jiangcheng@eastedu.com
receivers = jiangcheng@eastedu.com
sender_name = epip
title = 框架测试报告
content = 测试完成! 请查收报告!
smtp_addr = smtp.exmail.qq.com:465
smtp_user = jiangcheng@eastedu.com
smtp_passwd = Qwer9979
[DING]
; group_url -> 钉钉群地址
; target_url -> 链接跳转地址
; receviers -> 被@人列表 如 [ergou, liuhan]
group_url = https://oapi.dingtalk.com/robot/send?access_token=dc66c4fdd3d2fe0af8c455cfa20f10a30c933f1c19ca481024275974c240f4c1
title = 测试完成
content = 请在企业邮箱中查收测试结果
target_url = https://exmail.qq.com/
receivers = 13730879829
[HTML]
; project_name & addr -> 测试项目的名称以及地址
; author -> 用例创建人
project_name = UI_Web_Test_Project
project_addr = 127.0.0.1
author = epip
```
每条配置详情请参考对应区域下的注释';  '开头的字符串. 其中钉钉群地址为添加一个群机器人后机器人的'Hook'值.

Web方向有额外以下配置:
```python
[OTHER]
; broswer -> 使用的浏览器
; time_default -> 每次操作间默认的停顿时间
; wait_for_time -> 最大等待元素出现的时间
broswer = chrome
time_default = 1
wait_for_time = 5
```

Windows方向额外配置:
```python
; time_out -> 最大等待元素出现的时间
; path -> 应用路径, 如果配置了环境变量可以直接使用快捷短语 比如"python", "notepad"
; root_name -> 被测应用的'ClassName' 也是整个结构树的根地址
time_out = 3
path = notepad
root_name = Notepad
```

App方向额外配置:
```python
; time_out -> 最大等待元素出现的时间
; monkey_step & count -> 快速测试的点击间隔以及总点击次数
; test_level -> 测试级别 "normal, quick, stream, all"
time_out = 3
monkey_step = 20
monkey_count = 3000
test_level = normal
```
其中如果test_level不是all或者quick的话monkey_step 以及monkey_count就没有意义; test_level的所有参数为:
```python
 normal - 用例测试
 quick - 快速测试
 stream - 安装卸载测试
 all -> 安装 - 用例测试 -> 快速测试 -> 卸载测试
```

###data文件讲解

我们用于存放测试数据的路径, 仅仅支持csv格式的数据源; 一个登录的csv数据格式为:
其中登录我们需要用户名以及密码两个输入域, 像这样:
```python
username,liuhan,huqiao
passwd,123456,654321
```
可以发现, 每个输入域占一行, 其中名称开头, 之后为他的不同参数值; 这个可以任意组合, 不做长度规定.

###case文件讲解

case文件, 为我们一个测试用例定义基本操作的地方; 拿App端登录模块举例 完整代码为:
```python
from common.Base_Unit import Base_Base
from public.Setting_Unit import Setting_Base as Set


class Case_Login(Base_Base):

    def __init__(self):
        super().__init__()

    # 清除用户名
    def username_input_clear(self, case_name):
        self._clear(case_name, "resource", "com.dfwd.wlkt:id/username_et")

    # 输入用户名
    def username_input_input(self, case_name, username):
        self._input(case_name, "resource", "com.dfwd.wlkt:id/username_et", username)

    # 清除密码
    def passwd_input_clear(self, case_name):
        self._clear(case_name, "resource", "com.dfwd.wlkt:id/password_et")

    # 输入密码
    def passwd_input_input(self, case_name, passwd):
        self._input(case_name, "resource", "com.dfwd.wlkt:id/password_et", passwd)

    # 点击登录按钮
    def login_button_click(self, case_name):
        self._click(case_name, "resource", "com.dfwd.wlkt:id/tv_login")

    # 登陆成功断言
    def toptitle_text_assertion(self, case_name):
        self._assertion(case_name, "resource", "com.dfwd.wlkt:id/tv_main_title_user", "你好，研发测试高中1")

    # 登录失败断言
    def errortitle_text_assertion(self, case_name):
        self._assertion(case_name, "resource", "com.dfwd.wlkt:id/title", "用户登录")
        
    # 登录失败确认按钮
    def errorlogin_button_click(self, case_name):
        self._click(case_name, "resource", "com.dfwd.wlkt:id/llButtonContainer")

    # 启动时日志记录
    def start_log(self):
        self.log(self.Set.history_log, "info", "正在执行登录脚本......")

    # 结束时日志记录
    def end_log(self):
        self.log(self.Set.history_log, "info", "登陆脚本执行完毕.")

    # 意外情况 - 电子笔校验
    def accident_verify_button_click(self):
        self.d.watcher.when('//*[@resource-id="com.dfwd.wlkt:id/tv_cancel"]').click()

    # 开启意外处理
    def watcher_start(self):
        self.d.watcher.start()

    # 结束意外处理
    def watcher_close(self):
        self.d.watcher.reset()
```

其中我们的导包信息的话三个方向都是通用的 即都要导入
```python
from common.Base_Unit import Base_Base
from public.Setting_Unit import Setting_Base as Set
```

现在我们可以定义一个基础的case类:
```python
class Case_Login(Base_Base):

    def __init__(self):
        super().__init__()
```
这一步我们继承父类的操作(Base_Base), 调用其实现封装好的各种操作方法.

之后我们可以根据业务特性定义不同方法, 比如输入用户名:
```python
    # 输入用户名
    def username_input_input(self, case_name, username):
        self._input(case_name, "resource", "com.dfwd.wlkt:id/username_et", username)
```
我们调用继承的'_input'方法, 即输入方法; 注意'input'前面有个'_'; 我们可以看看该方法部分源码以及注释:
```python
    def _input(self, case_name, method, position, value):
        """
        写入操作
        Args:
            case_name: 用例名称
            method: 查找方式
            position: 定位值
            value: 传入的文本值

        Returns: 对找寻到的元素进行输入操作

        """
        # 写入历史记录
        self.case_history(case_name, f"{method} - {position}:{value} - input")

        try:
            # 检验find_element方式是否正确
            method = self.check_method(method)

            if method == "r":
                self.d(resourceId=position).send_keys(value)
            if method == "x":
                self.d.xpath(position).send_keys(value)

		...
```
我们可以得知, 该方法我们需要传入四个参数, 其中用例名称我们在suite文件中传入, 这里继续设为变量即可.

查找方式支持'r'以及'x', 即'resourceID', 以及'xpath'; 具体使用那个方式根据自己喜好来.

定位值指的是查找得到的值, 直接复制过来即可.

传入的文本即我们需要输入的信息, 这里也留给suite文件传入, 继续设为变量即可.

原来我们在case中只需要编写'method'以及'position'两个参数就行了, 而这两个都是通过元素定位工具获取. 就不更多叙述.

回到之前case中我们定义的输入用户名方法:
```python
    # 输入用户名
    def username_input_input(self, case_name, username):
        self._input(case_name, "resource", "com.dfwd.wlkt:id/username_et", username)
```
我们已经通过对底层方法的封装完成了'method'以及'position'的传入构成了新的方法; 也就是其中的'resource'以及'com.dfwd.wlkt:id/username_et'

方法名采用的是'相关特性'_'对象类型'_'操作类型'; 即username_input_input, 这个看着有些绕, 那 login_button_click(self, case_name) 这个方法看着就清晰许多.

具体解析该方法的话构成就如:
```python
	def 相关特性_对象类型_操作类型(self, case_name, value):
		self._input(case_name, 'resource' 或者'xpath', 'resourceID值' 或者'xpath值', value)
```
根据这个规则, 我们定义了清理输入框, 点击按钮, 断言文本这些操作.

而app端的case文件中有段特别的代码
```python
    # 意外情况 - 电子笔校验
    def 
	_watcher_button_click(self):
        self.d.watcher.when('//*[@resource-id="com.dfwd.wlkt:id/tv_cancel"]').click()

    # 开启意外处理
    def watcher_start(self):
        self.d.watcher.start()

    # 结束意外处理
    def watcher_close(self):
        self.d.watcher.reset()
```
先介绍下self.d.watcher中watcher是uiautomator2自带的监视器; 比如有一个页面每次流程经过有20%几率会弹出; 这属于预料之外的事件. 为了不因为意外中断测试我们就可以利用watcher捕捉这个弹出页面并对他进行处理, 比如关闭.

其中一个wathcer方法命名是按照'相关特性'_'watcher'_'对象类型'_'操作类型'命名的, 如'accident_watcher_button_click(self):'; 具体语句固定为'self.d.watcher.when(定位值-只能是xpath)'.'进行的操作'.

定义了监视器后我们也需要定义对应的开启以及关闭方法, 即:
```python
    # 开启意外处理
    def watcher_start(self):
        self.d.watcher.start()

    # 结束意外处理
    def watcher_close(self):
        self.d.watcher.reset()
```

除此之外, 还有两个特殊的方法即
```python
    # 启动时日志记录
    def start_log(self):
        self.log(self.Set.history_log, "info", "正在执行登录脚本......")

    # 结束时日志记录
    def end_log(self):
        self.log(self.Set.history_log, "info", "登陆脚本执行完毕.")
```
这两个为三个方向测试用例通用, 用于日志中记录用例的执行; 编写时直接复制即可.

###suite文件讲解

App端登录用例的suite文件源码如下:
```python
from case.case_login import Case_Login
from public.Data_Unit import Data_Base
import pytest


class Test_Login:
    # driver对象
    d = None
    data_list = Data_Base("login").result

    def setup_class(self):
        self.d = Case_Login()
        self.d.start_log()
        # 预料外的弹出框关闭
        self.d.accident_watcher_button_click()
        self.d.watcher_start()

    def teardown_class(self):
        self.d.end_log()
        # 清空监控
        self.d.watcher_close()
    
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize(argnames="username", argvalues=data_list["e_username"])
    @pytest.mark.parametrize(argnames="passwd", argvalues=data_list["e_passwd"])
    def test_error_login(self, username, passwd, case_name="login_error"):

        self.d.username_input_clear(case_name)
        self.d.username_input_input(case_name, username)
        self.d.passwd_input_clear(case_name)
        self.d.passwd_input_input(case_name, passwd)
        self.d.login_button_click(case_name)

        # 断言
        self.d.errortitle_text_assertion(case_name)
        self.d.errorlogin_button_click(case_name)

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize(argnames="username", argvalues=data_list["c_username"])
    @pytest.mark.parametrize(argnames="passwd", argvalues=data_list["c_passwd"])
    def test_correct_login(self, username, passwd, case_name="login_correct"):

        self.d.username_input_clear(case_name)
        self.d.username_input_input(case_name, username)
        self.d.passwd_input_clear(case_name)
        self.d.passwd_input_input(case_name, passwd)
        self.d.login_button_click(case_name)

        # 断言
        self.d.toptitle_text_assertion(case_name)
```
其中导包信息请自行修改'case_xxx'为自己编写的case文件名称
```python
from case.case_login import Case_Login
from public.Data_Unit import Data_Base
import pytest
```

现在我们可以定义一个suite类:
```python
class Test_Login:
    # driver对象
    d = None
    data_list = Data_Base("login").result
```
其中'data_list'是我们读取login.csv获取的测试数据; login.csv格式如下:
e_username,
e_passwd,3,rccand,abc
c_username,16962201596
c_passwd,RCCand
获取后data_list是一个字典, 格式如下
```python
{
'e_username':[1,123,456],
'e_passwd':[3,rccand,abc]
}
```

之后我们需要定义一个suite文件的'测试前动作'以及'测试后动作'即:
```python
    def setup_class(self):
        self.d = Case_Login()
        self.d.start_log()
        # 预料外的弹出框关闭
        self.d.accident_watcher_button_click()
        self.d.watcher_start()

    def teardown_class(self):
        self.d.end_log()
        # 清空监控
        self.d.watcher_close()
```
其中 setup_class指的是测试前需要进行的操作.

这里我们统一实例driver对象, 即'self.d = Case_Login()'; 注意这个driver对象指的是我们自己编写的case文件中的case类

继续我们激活启动日志'self.d.start_log()', 定义监控并开启监控; 注意需要先定义监控再统一开启.

teardown_class指的是测试后的清理操作.

我们这里激活结束日志, 并关闭监控.

而我们的主体测试部分位于sertup_class以及teardown_class之间进行的, 错误流程代码部分如下:
```python
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize(argnames="username", argvalues=data_list["e_username"])
    @pytest.mark.parametrize(argnames="passwd", argvalues=data_list["e_passwd"])
    def test_error_login(self, username, passwd, case_name="login_error"):

        self.d.username_input_clear(case_name)
        self.d.username_input_input(case_name, username)
        self.d.passwd_input_clear(case_name)
        self.d.passwd_input_input(case_name, passwd)
        self.d.login_button_click(case_name)

        # 断言
        self.d.errortitle_text_assertion(case_name)
        self.d.errorlogin_button_click(case_name)
```
其中第一个装饰器'pytest.mark.run(order=1)'表明该条方法第一个执行, orider=? 表明第几个执行, 数字从1开始.

第2个装饰器'pytest.mark.parametrize(argnames="username", argvalues=data_list["e_username"])'指的是定义参数为'username', 它的值为通过data_list这个字典中key为'e_username'取出的value, 即[1,123,456]

我们的方法主题命名方式为 test_'测试类型'_'测试名称'; 即test_error_login, 如果不需要测试错误流程, 那么直接test_login也可.

其中参数我们需要'username', 'passwd', case_name; 这里将'case_name'定义为关键字参数, 因为本质是调用我们编写的case文件中的封装的方法; 因此需要传入'case_name';

'username'的来源是我们之前装饰器得到的username值, 即[1,123,456]; 而又因为这个值一共有3个, 那么该方法会运行3次, 分别取出'1', '123', '456'传入并允许.

'passwd'也是同理, 不过请注意; 因为我们获取'passwd'值的时候也是通过pytest.mark.parmetrize这个装饰器获取的; 得到的值为'3,rccand,abc', 而它的长度也是3; 那么代表该方法一共会运行3X3 即9次; 第一次:username=1, passwd=3, 第二次 username=1, passwd=rccand以此类推...

回到该方法代码主题, 我们首先清理用户名输入框'username_input_clear', 之后传入密码; 密码框同理, 之后我们点击登录按钮, 并对弹出密码不正确提示的文本进行断言; 至此, 一个错误流程测试就完成了.

而正确流程代码如下:
```python
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize(argnames="username", argvalues=data_list["c_username"])
    @pytest.mark.parametrize(argnames="passwd", argvalues=data_list["c_passwd"])
    def test_correct_login(self, username, passwd, case_name="login_correct"):

        self.d.username_input_clear(case_name)
        self.d.username_input_input(case_name, username)
        self.d.passwd_input_clear(case_name)
        self.d.passwd_input_input(case_name, passwd)
        self.d.login_button_click(case_name)

        # 断言
        self.d.toptitle_text_assertion(case_name)
```
我们观察发现, 结构和错误流程完全一样! 只是传入参数的值不同而已.

##方法解释

这里的方法仅指的是最基本的操作; 具体用例编写(case文件, data文件, suite文件请参考不同方向框架中自带的例子)

###Windows端

1.    def _click(self, case_name, control_type, method, position, depth):
点击操作, 需要传入用例名, 窗体类型, 定位方式, 定位值, 搜索深度.

这里我们具体解释下'control_type'以及'depth'参数. 在windows应用中 所以窗体都有一个对应的'control'类型; 比如'EditControl,' 'ButtonControl'; 因此我们就需要传入'Edit'以及'Button'; 注意严格区分大小写; 所有支持的窗体类型可参考'Setting_Unit'文件中的'support_control_list'类属性.

'depth'参数, 即搜索深度; 首先我们需要明确, 在windows中, windows桌面为所有应用的根, 即它的深度为0, 比如我启动一个记事本应用,并且选记事本中的关闭按钮, 那么现在目录结构为:
```python
根
---记事本
------关闭按钮
---其他应用
```
其中 根深度为0; 记事本以及其他应用为1, 关闭按钮为2; 在我们实际编写过程中, 因为我们需要把我们被测应用实例为根应用, 因此注意深度计算; 现在的目录结构为:
```python
记事本(根)
---关闭按钮
```
记事本变为根了, 其深度也变为0, 关闭按钮深度为1了; 并且注意 深度参数值只能大于或等于实际深度; 否则找不到元素.(最好等于实际深度, 不然搜索性能会降低).

2.    def _double_click(self, case_name, control_type, method, position, depth):
双击操作, 同上

3.    def _right_click(self, case_name, control_type, method, position, depth):
右击操作, 同上

3.    def _input(self, case_name, control_type, method, position, depth, text):
输入操作, 上面及除外需要额外传入需要输入的文本; 注意在Windows应用中我们可以输入{Enter}表示换行, {End}表示光标移至该行最后, {Home}最前面; {Alt}启用组合键.

4.    def _assertion(self, case_name, control_type, method, position, depth, text):
断言操作

5.    def _close(self, case_name):
关闭当前窗体(不是应用!)

###App端

1.    def _click(self, case_name, method, position):
点击操作, 需要传入用例名, 定位方式, 定位值

2.    def _double_click(self, case_name, method, position):
双击操作

3.    def _input(self, case_name, method, position, value):
输入操作

4.    def _clear(self, case_name, method, position):
清空文本操作

5.    def _assertion(self, case_name, method, position, value):
断言操作

###Web端

1.    def _start(self, url):
开启浏览器, 需要传入url地址

2.    def _delay(self, case_name):
暂停操作

3.    def _quit(self):
关闭浏览器

4.    def _click(self, case_name, method, position):
单机操作

5.    def _input(self, case_name, method, position, content):
输入操作

6.    def _chains(self, case_name, method, position):
光标停留于悬浮框上

7.    def _select(self, case_name, method, position, index):
下拉框选择值, 需要传入下标

8.    def _captcha(self, case_name, method, position):
识别验证码

9.    def _assertion(self, case_name, method, position, text):
断言操作

10.    def _handle_click(self, case_name, method, position):
切换句柄点击操作

##参数注意事项

###Windows参数

在windows框架中, 我们主要的参数为'control_type, method, position, depth'; 其中第1, 4个参数的解释请参考windows方法解释中'_click'操作的解释.

而我们支持的'method', 即定位方式为有'Name', 'ClassName', 'foundIndex'以及'AutomationId'; 注意区分大小写, 其中'AutomationId'经测试只有为数字时候才有效果, foundIndex指的是当前目录下的窗体下标, 比如WindowsControl(Name="test")有3个EditControl, 那么我们就可以WindowsControl(Name="test").EditControl(foundIndex=2)来指定它.

注意Inspect显示的position是自带了双引号的, 复制即可, 不需要我们自行添加.

###App参数

在App框架中, 我们主要的参数为'method, position'; 其中method我们支持resourceID以及XPATH; 不过在编写case文件的时候, 请记得写成'resource'以及'xpath'; position, 我们只需要复制即可.

###Web参数

在Web框架中, 我们主要的参数为'method, position'; 其中method支持'xpath, link text, id, name, css selector; 其余不过多赘述.
