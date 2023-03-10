from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_carousel, push_message, send_button_message
from invoice import sendUse, showCurrent, showOld, show3digit, show5digit


mode = ""
digit3 = ""
status = 0


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_lobby(self, event):
        return True

    def is_going_to_back_lobby(self, event):
        return True

    def is_going_to_show_current(self, event):
        text = event.message.text
        return text == "當期號碼"

    def is_going_to_show_use(self, event):
        text = event.message.text
        return text == "使用說明"

    def is_going_to_show_old(self, event):
        text = event.message.text
        return text == "前期號碼"

    def is_going_to_match(self, event):
        text = event.message.text
        return text == "兌獎"

    def is_going_to_match1(self, event):
        global mode, digit3, status
        number = event.message.text
        mode = "special"
        digit3 = number
        if(number.isdigit()):
            status = show3digit(event, number)
        return status == 1

    def is_going_to_match2(self, event):
        global mode, digit3, status
        number = event.message.text
        mode = "head"
        digit3 = number        
        return status == 2

    def is_going_to_match3(self, event):
        global status
        return status == 3

    def is_going_to_match0(self, event):
        global status
        return status == -1   

    def is_going_to_end_match(self, event):
        text = event.message.text
        return text == "退出"

    def is_going_to_prize_match(self, event):
        try:
            global mode, digit3, status
            text = event.message.text
            if(text.isdigit()):
                show5digit(event, text, mode, digit3)
            mode = ""
            digit3 = ""
            status = 0
            return True
        except:
            self.go_back(event)
            return False

    def is_going_to_back_match(self, event):
        text = event.message.text
        return text == "是"

    def is_going_to_back_lobby(self, event):
        text = event.message.text
        return text == "否"

    def on_enter_lobby(self, event):
        print("I'm entering lobby")

        userid = event.source.user_id
        send_button_carousel(userid)

    def on_enter_show_use(self, event):
        print("I'm entering show use")

        reply_token = event.reply_token
        send_text_message(reply_token, sendUse())
        self.go_back(event)


    def on_enter_show_current(self, event):
        print("I'm entering show current")

        showCurrent(event)
        self.go_back(event)
    
    def on_enter_match(self, event):
        print("I'm entering match")

        userid = event.source.user_id
        labels = ["退出"]
        texts = ["退出"]
        msg = "請輸入發票後三碼數字："
        send_button_message(userid, msg, labels, texts)

    def on_enter_match1(self, event):
        print("I'm entering match1")
        self.go_second_match(event)

    def on_enter_match2(self, event):
        print("I'm entering match2")
        self.go_second_match(event)

    def on_enter_match3(self, event):
        global status
        
        print("I'm entering match3")
        status = 0
        self.go_back_match(event)
    
    def on_enter_match0(self, event):
        print("I'm entering match0")
        self.go_back(event)

    def on_enter_end_match(self, event):
        print("I'm entering end match")

        text = "已退出兌獎功能。"
        reply_token = event.reply_token
        send_text_message(reply_token, text)        
        self.go_back(event)

    def on_enter_second_match(self, event):
        print("I'm entering second match")

    def on_enter_prize_match(self, event):
        print("I'm entering prize match")

        userid = event.source.user_id
        msg = "請問是否要繼續兌獎？"
        labels = ['是', '否']
        texts = ['是', '否']
        send_button_message(userid, msg, labels, texts)





    """
    def on_exit_state1(self):
        print("Leaving state1")
    """

    def on_enter_show_old(self, event):
        print("I'm entering show old")

        showOld(event)
        self.go_back(event)
