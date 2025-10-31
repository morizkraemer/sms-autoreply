
class Message_Queue:
    def __init__(self):
        self.send_queue = []
        self.delete_queue = []
        pass

    def get_first_delete(self):
        return self.delete_queue[0]

    def remove_first_delete(self):
        del self.delete_queue[0]

    def get_all_delete(self):
        return self.delete_queue

    def get_num_delete(self):
        return len(self.delete_queue)

    def delete_empty(self):
        return len(self.delete_queue) == 0

    def append_delete(self, items):
        if (isinstance(items, list)):
            self.delete_queue = self.delete_queue + items
        else:
            self.delete_queue.append(items)

    def get_first_send(self):
        return self.send_queue[0]

    def remove_first_send(self):
        del self.send_queue[0]

    def get_all_send(self):
        return self.send_queue

    def get_num_send(self):
        return len(self.send_queue)

    def send_empty(self):
        return len(self.send_queue) == 0

    def append_send(self, items):
        if (isinstance(items, list)):
            self.send_queue = self.send_queue + items
        else:
            self.send_queue.append(items)
