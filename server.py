from concurrent import futures

import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc


class ChatServer(rpc.ChatServerServicer):  

    def __init__(self):
        # List with all the chat history
        self.chats = []

    # The stream which will be used to send new messages to clients
    def ChatStream(self, request_iterator, context):
    
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        
        # logging on server console
        print("[{}] {}".format(request.name, request.message))
        # Add it to the chat history
        self.chats.append(request)
        return chat.Empty() 


if __name__ == '__main__':
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print('Starting server. Listening on port 50051')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    
    try:
        while True:
            time.sleep(64 * 64 * 100)
    except KeyboardInterrupt:
        server.stop(0)
