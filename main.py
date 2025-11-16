# import threading
import time
import uvicorn
import logging

# from db.connection import Database
from helpers.message_queue import Message_Queue
from modem.modem import Modem
# from db.connection import Database
# from db.connection import conn_string
from helpers.shared_data import shared_data

def loop(mqueue: Message_Queue, modem: Modem):

    while True:
        if mqueue.delete_empty():
            logging.info("queue 1")
            mqueue.append_delete(modem.get_all_sms())

        if not mqueue.send_empty():
            logging.info("queue 2")
            while not mqueue.send_empty():
                message = mqueue.get_first_send()
                if (modem.send_sms(message["number"], shared_data.get_reply_message())):
                    mqueue.remove_first_send()
                else:
                    break
        else:
            logging.info("queue 3")
            while not mqueue.delete_empty():
                message = mqueue.get_first_delete()
                if (modem.delete_sms(message["index"])):
                    mqueue.append_send(message)
                    mqueue.remove_first_delete()
                else:
                    break
        time.sleep(1)

def run_web_server():
    uvicorn.run("webserver.server:app", host="0.0.0.0", port = 6969)

def main():
    print("init")
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger("base")
    modem = Modem()
    mqueue = Message_Queue()
    print("init")
    logger.info("init")

    # db = Database(conn_string)

    # web_thread = threading.Thread(target=run_web_server, daemon=True)
    # web_thread.start()

    loop(mqueue, modem)



if __name__ == "__main__":
    main()
