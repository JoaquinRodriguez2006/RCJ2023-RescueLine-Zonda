import hub
from spike import Motor


# Initialize the motor
motor = Motor('A')


class SerialCommunicator:
    def __init__(self, is_receiver=False):
        self.symbols = {
            "separator":",",
            "equals":":",
            "start_message":"<<",
            "end_message":">>"
        }

        if is_receiver:
            self.mode = hub.USB_VCP.RTS
        else:
            self.mode = hub.USB_VCP.CTS

        self.connection = hub.USB_VCP()
        self.connection.init(flow=self.mode)

    def dict_to_string(self, input_dict:dict):
        final_list = []

        for key, value in input_dict.items():
            final_list.append(str(key) + self.symbols["equals"] + str(value))

        final_string = self.symbols["separator"].join(final_list)

        return self.symbols["start_message"] + final_string + self.symbols["end_message"]
    
    def find_message(self, input_str:str):
        start_index = input_str.find(self.symbols["start_message"])
        start_index += len(self.symbols["start_message"])

        end_index = input_str[start_index:-1].find(self.symbols["end_message"])
        end_index -= len(self.symbols["end_message"]) - 1

        return input_str[start_index : end_index]

    def string_to_dict(self, input_str:str):
        final_dict = {}
        message = self.find_message(input_str)
        print("message:", message)

        variables = message.split(",")

        for v in variables:
            var_list = v.split(":")
            final_dict[var_list[0]] = var_list[1]

        return final_dict

    def send_dict(self, message:dict):
        self.connection.write(self.dict_to_string(message))
    
    def recieve_data(self):
        if self.connection.any():
            return self.string_to_dict(self.connection.readline().decode())
    


communicator = SerialCommunicator()

#communicator.send_dict({"a":"1", "hello":"4"})

while True:
    data = communicator.recieve_data()
    if data is not None:
        if data["mover"] == "1":
            motor.start(50)
        elif data["mover"] == "2":
            motor.stop()