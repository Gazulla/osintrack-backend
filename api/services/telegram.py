from telethon.sync import TelegramClient, functions
import asyncio

def setClient(apiId, apiHash):
    session = "osintrack-app-session"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(session, api_id=apiId, api_hash=apiHash, loop=loop)
    client.connect()
    return client

def getTelegramGroup(groupIdentifier,apiId,apiHash):
    try:
        client = setClient(apiId, apiHash)
        full = client(functions.channels.GetFullChannelRequest(groupIdentifier))
        full_channel = full.full_chat
        channel = client.get_entity(groupIdentifier)
        client.disconnect()
    except Exception as exc:
        return {"success": False, "detail":str(exc)}

def connectTelegramRequest(apiId,apiHash,phone):
    try:
        client = setClient(apiId, apiHash)
        if not client.is_user_authorized():
            response = client.send_code_request(phone)
            phone_code_hash = response.phone_code_hash
            client.disconnect()
            return  {"success": True, "detail":phone_code_hash}
        return {"success": False, "detail":"Already connected!"}
    except Exception as exc:
         return {"success": False, "detail":str(exc)}
        
def connectTelegramInputCode(apiId,apiHash,phone,code, phone_code_hash):
    try:
        client = setClient(apiId, apiHash)
        client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
        client.disconnect()
        result = {"success": True, "detail":"Connected!"}
        return  result
    except Exception as exc:
        return {"success": False, "detail":str(exc)}

def logOutTelegram(apiId,apiHash):
    try:
        client = setClient(apiId, apiHash)
        client.log_out()
    except Exception as exc:
        return exc

def checkTelegramConnection(apiId,apiHash):
    try:
        client = setClient(apiId, apiHash)
        isConnected = client.is_user_authorized()
        client.disconnect()
        return isConnected
    except Exception as exc:
        return exc

    




