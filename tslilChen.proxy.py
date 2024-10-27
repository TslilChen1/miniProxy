import socket
import datetime
import time
def client_message():
    """
    the function listening to the client and when a request as been sent it takes it takes it and
    return it and the conversation sock
    :return: a tuplw that contains othe client sic and the client message
    :rtype: tuple
    """
    with socket.socket() as listening_sock:
        LISTEN_PORT = 9090
        server_address = ('', LISTEN_PORT)
        listening_sock.bind(server_address)
        # Listen for incoming connections
        listening_sock.listen(1)
        #Create a new conversation socket
        client_soc, client_address = listening_sock.accept()
        client_msg = client_soc.recv(1024)
        client_msg = client_msg.decode()
    return (client_soc, client_msg)

def server_messege(client_msg, client_soc):
    """
    the function send to the film4me server the message and get an answer , edit it and return it
    :return: server_msg
    :rtype: string
    """
    SERVER_IP = "54.71.128.194"
    SERVER_PORT = 92
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = (SERVER_IP, SERVER_PORT)
        sock.connect(server_address)
        sock.sendall(client_msg.encode())
        server_msg = sock.recv(1024)
        server_msg = server_msg.decode()
        server_msg = check_messege(server_msg, client_msg)
    return server_msg

def check_messege(server_msg, client_msg):
    """
    the function check the message that the server return/the messege the the user send and chrck if it
    stands in the conditions
    :return: the server fixed message
    :rtype: string
    """
    if "france" in client_msg.lower():
        server_msg = 'ERROR#"France is banned!"'
    elif "MOVIEDATA" in server_msg:
        #fix immage issue
        server_msg = server_msg[:server_msg.find("jpg")] + ".jpg" + server_msg[server_msg.find("jpg") + 3:]
        #now we will ass our own errors - mewning that if the app "works" we will senf the ERROR
        if len(client_msg[client_msg.find("genre:") + 6: client_msg.find("&")]) > 20:
            server_msg = 'ERROR#"The genre is too long"'
    elif "SERVERERROR" in server_msg:
        #the serever error ruin the prof thats why i changed it to regulur error
        server_msg = "ERROR" + server_msg[server_msg.find("#"):]
    elif "ERROR" in server_msg:
        #no future date
        today = datetime.date.today()
        year = today.year
        if (int(client_msg[client_msg.find("year:") + 5: client_msg.find("-")]) > int(year)) or \
                (int(client_msg[client_msg.find("-") + 1: client_msg.find("-") + 5] > int(year))):
            server_msg = 'ERROR#"The year is in the future"'
    return server_msg


def main():
    start_time = time.time()
    MINUTE = 60
    count = 0
        while True:
        count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        #saving the conversation sic between the user and the proxy, and the client message
        client_soc, client_msg = client_message()
        #no more than 6 request in a minute
        if count > 5 and elapsed_time <= MINUTE:
            current_time = 0
            elapsed_time = 0
            count = 0
            server_msg = 'ERROR#"No more request allows! Please wait 1 minute"'
        else:
            #saving to server_msg the server answer using the server_messege func
            server_msg = server_messege(client_msg, client_soc)
        #sending info to client
        client_soc.sendall(server_msg.encode())
        #close the socket that send the user messages
        client_soc.close()

if __name__ == "__main__":
    main()

