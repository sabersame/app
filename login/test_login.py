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
<<<<<<< HEAD
        
=======

>>>>>>> f689bfc999c8d298268fa9aaf88d3ead0d5fd608
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

