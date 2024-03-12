from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import string, datetime, asyncio

# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')
print("main裡面的token: ",TOKEN)


# set up bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#set a response to track if there's record or not
response = {"response":None, "record":None}
print("一起動時的response: ", response)

#remove punctuation marks
def remove_punctuation(user_input_string):
    translator = str.maketrans('', '', string.punctuation)
    result = user_input_string.translate(translator)
    return result

#combine user input and record
def combine_userinput_record(user_message):
    global response
    #pull out previous record
    previous_user_input = response["record"].values()
    print("pull out previous record: ", previous_user_input)

    previous_user_input_str = ""

    for val in previous_user_input:
        if val != None:
            previous_user_input_str = previous_user_input_str + " " +  val

    #add current user input
    previous_user_input_str = previous_user_input_str + " " +  user_message

    print("整理好的previous_user_input_str: ",previous_user_input_str)
    return previous_user_input_str


#message functionality
async def send_message(message: Message, user_message) -> None:
    print("*****send_message---user_message 應該都要是string: ", message, user_message)

    global response
    # user_message_to_str = None
    is_private = False
    if not user_message:
        print("Message is empty")
        return

    #private response
    is_private = user_message[0] == "?"
    if is_private :
        user_message = user_message[1:]

    try:
        # if user_message_to_str:
        #     user_message_rmv_punctuation= remove_punctuation(user_message_to_str)
        # else:
        #     user_message_rmv_punctuation= remove_punctuation(user_message)
        user_message_rmv_punctuation= remove_punctuation(user_message)
        print("拿掉標點符號的樣子ˋ,",user_message_rmv_punctuation)

        # #if the message is still hello and user_message is "there's no previous record" (which means user didn't input anything)
        # if message['response'] == "Hello there! How can I help you ?" and user_message_rmv_punctuation == "theres no previous record":
        #     #送進get_response的是 hello
        #     response = get_response(message['response'])
        # else:
        #     #送進get_response的是 user input並且移除標點符號的字串
        #     response = get_response(user_message_rmv_punctuation)
        response = get_response(user_message_rmv_punctuation)


        print("準備紀錄zipcode and date",response)
        channel = client.get_channel(1186427997851488266)
        # await message.author.send(response) if is_private else await message.channel.send(response)
        # await message.author.send(response["response"]) if is_private else await message.channel.send(response["response"])
        await message.author.send(response["response"]) if is_private else await channel.send(response["response"])



    except Exception as e:
        print("有錯誤")
        print(e)


async def schedule_daily_message():
    print("一開始run schedule_daily_message時的response: ", response)
    while True:
        #wait for some time
        now = datetime.datetime.now()
        then = now + datetime.timedelta(minutes= 1)
        wait_time = (then-now).total_seconds()
        print("看看now ",now)
        print("看看then ",then)

        await asyncio.sleep(wait_time)

        #check if there's previous record
        #send message
        channel = client.get_channel(1186427997851488266)
        await channel.send("test by specific time")

        #no previous record
        if response["record"] is None:
            print("***clock自動 並確認沒有之前紀錄")
            await send_message(response,"there's no previous record")

        #there's previous record
        elif response["record"] is not None:
            print("***clock自動 並確認 有之前紀錄: ",response["record"])
            input_record_str = ""
            for input_record in response["record"].values():
                #only collect data which is not none
                if input_record != None:
                    input_record_str = input_record_str + " " + input_record
            await send_message(None,input_record_str)


# handle incoming messages
@client.event
async def on_ready():
    print(f"{client.user} is now running!")
    print("*****一開啟")
    await schedule_daily_message()

@client.event
async def on_message(message: Message)-> None:
    print("*****當user有輸入任何文字時")
    print("on_message on fire時候的response: ", response)
    # check if bot is not responding itself
    if message.author == client.user:
        print("傳送message的是client自己")
        print("--------------END---------------")
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print("傳送message 不是client自己")

    print(f"[{channel}] {username}: '{user_message}'")
    print("這裡的message: ", message)

    #check if there's no record in response
    if response["record"] is None:
        print("*****當user有輸入任何文字時---檢查 沒有previous record")
        await send_message(message,user_message)

    #check if there's record in response
    elif response["record"] is not None:
        print("*****當user有輸入任何文字時---檢查 有previous record")


        # new_user_message = await combine_userinput_record(user_message)
        new_user_message = combine_userinput_record(user_message)
        await send_message(message,new_user_message)






# run bot
def main()->None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
