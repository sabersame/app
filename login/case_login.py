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
