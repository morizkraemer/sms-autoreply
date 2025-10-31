from modem import Modem
from message_queue import Message_Queue
import time

REPLY_MESSAGE = "Hey there, got your message :)"

def loop(mqueue, modem):
    while True:
        if mqueue.delete_empty():
            mqueue.append_delete(modem.get_all_sms())

        if not mqueue.send_empty():
            while not mqueue.send_empty():
                message = mqueue.get_first_send()
                if (modem.send_sms(message["number"], REPLY_MESSAGE)):
                    mqueue.remove_first_send()
                else:
                    break
        else:
            while not mqueue.delete_empty():
                message = mqueue.get_first_delete()
                if (modem.delete_sms(message["index"])):
                    mqueue.append_send(message)
                    mqueue.remove_first_delete()
                else:
                    break
        time.sleep(1)

def main():
    modem = Modem()
    mqueue = Message_Queue()

    # mqueue.append_delete(modem.get_all_sms())
    # print(mqueue.get_all_delete())
    # print(mqueue.get_first_delete())

    # print(modem.get_all_sms())

    loop(mqueue, modem)



if __name__ == "__main__":
    main()
