#!/usr/bin/python3
# coding: latin-1
import socket,random

kill_message = ""
store_kill_message = ""

def create_message(object_id,pos_x,pos_y):
    new_string = "object_message:"+str(object_id)+"@"+str(pos_x)+"$"+str(pos_y)
    return new_string

def create_projectile_message(angle,pos_x,pos_y):
    new_string = "projectile_message:"+str(angle)+"@"+str(pos_x)+"$"+str(pos_y)
    new_string = new_string.replace("\n","")
    return new_string

def create_projectile_pos_message(angle,pos_x,pos_y):
    new_string = "projectile_pos_message:"+str(angle)+"@"+str(pos_x)+"$"+str(pos_y)
    new_string = new_string.replace("\n","")
    return new_string

def decode_message(incoming_string):
    try:
        part1 = incoming_string[0:incoming_string.index("@")]
        part2 = incoming_string[incoming_string.index("@")+1:incoming_string.index("$")]
        part3 = incoming_string[incoming_string.index("$")+1:]
        return part1,part2,part3
    except Exception as e:
        print(e)
        return None

def decode_kill(incoming_string):
    try:
        part1 = incoming_string[0:incoming_string.index("@")]
        part2 = incoming_string[incoming_string.index("@")+1:incoming_string.index("$")]
        return part1,part2
    except Exception as e:
        print(e)
        return None

def collect_kills(data,data_store):

    global kill_message
    global store_kill_message

    try:
        data_store = data_store.decode("utf-8")
        data = data.decode("utf-8")
    except Exception as e:
        print(e)

    collect = []
    collect2 = []


    for x in range(data.count("object_message:")):
        data = data[15:]
        try:
            newdata = data[:data.index("object_message:")]
        except:
            newdata = data[:]
        data1,data2,data3 = decode_message(newdata)
        data1 = data1.replace(":","")
        # for dio in socket_dios:
        #     if dio.label == int(data1):
        #         dio.rect.left = float(data2)
        #         dio.rect.top = float(data3)
        collect.append((int(data1),float(data2),float(data3)))
        if data.count("object_message:") >= 1:
            data = data[data.index("object_message:"):]

    for x in range(data_store.count("object_message:")):
        data_store = data_store[15:]
        try:
            newdata = data_store[:data_store.index("object_message:")]
        except:
            newdata = data_store[:]
        data1,data2,data3 = decode_message(newdata)
        data1 = data1.replace(":","")
        # for dio in socket_dios:
        #     if dio.label == int(data1):
        #         dio.rect.left = float(data2)
        #         dio.rect.top = float(data3)
        collect2.append((int(data1),float(data2),float(data3)))
        if data_store.count("object_message:") >= 1:
            data_store = data_store[data_store.index("object_message:"):]
        # print(str((float(data1),float(data2),float(data3))))


    for dio in collect:
        for socket_dio in collect2:
            if (((((dio[1]-socket_dio[1])**2)+((dio[2]-socket_dio[2])**2))**0.5)) < 80:
                surrounding_dios = 0
                surrounding_socket_dios = 0
                for surrounding_dio in collect:
                    if surrounding_dio != dio:
                        if (((((dio[1]-surrounding_dio[1])**2)+((dio[2]-surrounding_dio[2])**2))**0.5)) < 25:
                            surrounding_dios += 1

                for surrounding_dio in collect2:
                    if surrounding_dio != socket_dio:
                        if (((((socket_dio[1]-surrounding_dio[1])**2)+((socket_dio[2]-surrounding_dio[2])**2))**0.5)) < 25:
                            surrounding_socket_dios += 1

                chance = surrounding_dios - surrounding_socket_dios

                if chance > 0:
                    if random.randint(0,chance) >= (chance**0.5):
                        kill_message += "kill_message:"+str(dio[0])+"@"+"1$"
                        store_kill_message += "kill_message:"+str(dio[0])+"@"+"2$"
                    else:
                        kill_message += "kill_message:"+str(socket_dio[0])+"@"+"1$"
                        store_kill_message += "kill_message:"+str(socket_dio[0])+"@"+"2$"
                if chance < 0:
                    if random.randint(chance,0) <= -1*(abs(chance)**0.5):
                        kill_message += "kill_message:"+str(dio[0])+"@"+"1$"
                        store_kill_message += "kill_message:"+str(dio[0])+"@"+"2$"
                    else:
                        kill_message += "kill_message:"+str(socket_dio[0])+"@"+"1$"
                        store_kill_message += "kill_message:"+str(socket_dio[0])+"@"+"2$"
                if chance == 0:
                    if random.randint(0,1) == 0:
                        kill_message += "kill_message:"+str(dio[0])+"@"+"1$"
                        store_kill_message += "kill_message:"+str(dio[0])+"@"+"2$"
                    else:
                        kill_message += "kill_message:"+str(socket_dio[0])+"@"+"1$"
                        store_kill_message += "kill_message:"+str(socket_dio[0])+"@"+"2$"


def main():
    global kill_message
    global store_kill_message

    clients = []
    clients_responded = []
    data_store = ""
    from_addr_store = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    host = s.getsockname()[0]
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # port = int(input('Port:'))
    port = 1245


    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    print('Server Started:\nServer Key/Ip: '+host)
    while True:
        data, addr = s.recvfrom(1024)
        if addr not in clients_responded:
            clients_responded.append(addr)

        if addr not in clients:
            clients.append(addr)
            print("new connection, address name: "+str(addr))

        if len(clients) > 1:
            if len(clients_responded) == len(clients):
                try:
                    data = data.decode('utf-8')
                except Exception as e:
                    print(e)
                collect_kills(data,data_store)
                clients_responded = []
                if data_store != '':
                    data_store = data_store.decode('utf-8')
                    data_store = str(data_store)
                    for client in clients:
                        if client != from_addr_store:
                            try:
                                s.sendto(str.encode(data_store+store_kill_message),client)
                            except Exception as e:
                                print(e)
                    data_store = str.encode("")
                    from_addr_store = str.encode("")
                if data != '':
                    data = data.decode('utf-8')
                    data = str(data)
                    for client in clients:
                        if client != addr:
                            try:
                                s.sendto(str.encode(data+kill_message),client)
                            except Exception as e:
                                print(e)
                kill_message = ""
                store_kill_message = ""

            else:
                data_store = data
                from_addr_store = addr

    s.close()

main()
