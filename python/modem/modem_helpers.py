class ConnectionError(Exception):
    pass

def readlines_helper(serialConnection):
    response = []
    while True:
        line = serialConnection.readline()
        if not line:
            break
        response.append(line)
    return response

def parse_all_sms(response):
    messages = []
    current_message = {}

    for line in response:
        decoded_line = line.decode('utf-8').strip()
        if decoded_line.startswith('+CMGL:'):
            if current_message:
                messages.append(current_message)
                current_message = {}
            t = decoded_line.split(",")
            current_message["index"] = t[0].strip("+CMGL: ")
            current_message["state"] = t[1].strip('"')
            current_message["number"] = t[2].strip('"')
            current_message["date"] = [t[4].strip('"'), t[5].strip('"')]
        elif current_message and decoded_line != '' and not decoded_line.startswith('OK'):
            current_message["message"] = decoded_line

    if current_message:
        messages.append(current_message)
    return messages



