import pwn
import json
import curses

address = ("socket.cryptohack.org", 13421)
connection = pwn.connect(address[0], address[1])
connection.recvline()

def createEncryptCommand() -> str:
    return "{\"option\":\"encrypt\"}"

def createUnpadCommand(ct: str) -> str:
    return "{\"option\":\"unpad\",\"ct\":\"" + ct + "\"}"

def createCheckCommand(message: str) -> str:
    return "{\"option\":\"check\",\"message\":\"" + message + "\"}"

def splitBlocks(value: str, size: int):
    blocks = []
    for i in range(0, len(value), size):
        blocks.append(value[i: min(i + size, len(value))])
    return blocks

def joinToHex(array):
    result = ""
    for value in array:
        result += "{0:02x}".format(value)
    return result

def main(stdscr):

    curses.resize_term(100, 300)
    stdscr.refresh()
    curses.start_color()
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    stdscr.clear()

    stdscr.addstr(0, 0, "***************************************************{ AES CBC PKCS7 PADDING ORACLE ATTACK }***************************************************", curses.color_pair(2))

    stdscr.addstr(3, 0, "[*] Getting ciphertext", curses.color_pair(1))
    stdscr.refresh()

    # Получаем зашифрованное сообщение
    command = createEncryptCommand()
    connection.sendline(command.encode())
    ciphertext = json.loads(connection.recvline().decode())["ct"]
    stdscr.addstr(4, 4, "Received ciphertext: " + ciphertext, curses.color_pair(2))
    stdscr.refresh()

    stdscr.addstr(6, 0, "[*] Preparing attack", curses.color_pair(1))
    stdscr.refresh()
    blocks = splitBlocks(ciphertext, 32)
    ivHex = blocks[0]
    ct1Hex = blocks[1]
    ct2Hex = blocks[2]

    ivBytes = bytes.fromhex(ivHex)
    ct1Bytes = bytes.fromhex(ct1Hex)
    ct2Bytes = bytes.fromhex(ct2Hex)

    ivArr = []
    ct1Arr = []
    ct2Arr = []
    for idx in range(0, 16):
        ivArr.append(ivBytes[idx])
        ct1Arr.append(ct1Bytes[idx])
        ct2Arr.append(ct2Bytes[idx])

    stdscr.addstr(7, 4, f"IV hex: {ivHex}, IV bytes: {ivArr}", curses.color_pair(2))
    stdscr.addstr(8, 4, f"Block 1 hex: {ct1Hex}, Block 1 bytes: {ct1Arr}", curses.color_pair(2))
    stdscr.addstr(9, 4, f"Block 2 hex: {ct2Hex}, Block 2 bytes: {ct2Arr}", curses.color_pair(2))

    stdscr.addstr(11, 0, "[*] Attacking", curses.color_pair(1))
    stdscr.refresh()

    knownPlaintext = ""
    decryptedArr = []

    while len(decryptedArr) < 32:
        knownLength = len(decryptedArr)
        attackingIndex = knownLength
        isFirstBlock = knownLength < 16

        paddingSize = knownLength % 16 + 1
        targetValue = paddingSize

        knownPlaintextString = f"Knwon plaintext: {knownPlaintext}, "
        stdscr.addstr(12, 4, knownPlaintextString, curses.color_pair(2))
        stdscr.addstr(12, 4 + len(knownPlaintextString), f"Target padding: {targetValue}", curses.color_pair(2))
        stdscr.refresh()

        replacingValues = []
        for idx in range(knownLength):
            replacingValues.append(decryptedArr[idx] ^ targetValue)
        
        replacedIvArr = ivArr.copy()
        replacedCt1Arr = ct1Arr.copy()
        for idx in range(knownLength):
            if idx < 16:
                if isFirstBlock:
                    replacedCt1Arr[len(replacedCt1Arr) - idx - 1] = replacingValues[idx]
            else:
                replacedIvArr[len(replacedIvArr) - (idx - 16) - 1] = replacingValues[idx]

        stdscr.addstr(13, 4, "Sending values: ", curses.color_pair(2))
        stdscr.refresh()
        for attackingValue in range(256):
            foundX = attackingValue ^ targetValue
            if isFirstBlock:
                plaintextChar = chr(foundX ^ ct1Arr[len(ct1Arr) - knownLength - 1])
            else:
                plaintextChar = chr(foundX ^ ivArr[len(ivArr) - (knownLength - 16) - 1])
            if plaintextChar not in "0123456789abcdef": continue

            stdscr.addstr(14, 0, " " * 1000)
            if isFirstBlock:
                replaceIndex = len(replacedCt1Arr) - attackingIndex - 1
                replacedCt1Arr[replaceIndex] = attackingValue

                lineOffest = 8
                stringBeforeReplacedIdx = f"IV: {joinToHex(replacedIvArr)} Block 1: {joinToHex(replacedCt1Arr[:replaceIndex])}"
                stdscr.addstr(14, lineOffest, stringBeforeReplacedIdx, curses.color_pair(2))
                lineOffest += len(stringBeforeReplacedIdx)

                replacedCt1ValueString = "{0:02x}".format(replacedCt1Arr[replaceIndex])
                stdscr.addstr(14, lineOffest, replacedCt1ValueString, curses.color_pair(1))
                lineOffest += len(replacedCt1ValueString)

                stringAfterReplacedIdx = f"{joinToHex(replacedCt1Arr[replaceIndex + 1:])} Block 2: {joinToHex(ct2Arr)}"
                stdscr.addstr(14, lineOffest, stringAfterReplacedIdx, curses.color_pair(2))
            else:
                replaceIndex = len(replacedIvArr) - (attackingIndex - 16) - 1
                replacedIvArr[replaceIndex] = attackingValue

                lineOffest = 8
                stringBeforeReplacedIdx = f"IV: {joinToHex(replacedIvArr[:replaceIndex])}"
                stdscr.addstr(14, lineOffest, stringBeforeReplacedIdx, curses.color_pair(2))
                lineOffest += len(stringBeforeReplacedIdx)

                replacedIvArrValueString = "{0:02x}".format(replacedIvArr[replaceIndex])
                stdscr.addstr(14, lineOffest, replacedIvArrValueString, curses.color_pair(1))
                lineOffest += len(replacedIvArrValueString)

                stringAfterReplacedIdx = f"{joinToHex(replacedIvArr[replaceIndex + 1:])} Block 1: {joinToHex(ct1Arr)}"
                stdscr.addstr(14, lineOffest, stringAfterReplacedIdx, curses.color_pair(2))

            combinedValue = replacedIvArr + replacedCt1Arr
            if isFirstBlock:
                combinedValue += ct2Arr

            combinedHex = joinToHex(combinedValue)
            command = createUnpadCommand(combinedHex)
            stdscr.addstr(15, 8, f"Command: {command}", curses.color_pair(2))

            connection.sendline(command.encode())
            answer = connection.recvline().decode()
            result = json.loads(answer)["result"]
            if result == True:
                foundX = attackingValue ^ targetValue
                if isFirstBlock:
                    knownPlaintext = chr(foundX ^ ct1Arr[len(ct1Arr) - knownLength - 1]) + knownPlaintext
                else:
                    knownPlaintext = chr(foundX ^ ivArr[len(ivArr) - (knownLength - 16) - 1]) + knownPlaintext
                
                decryptedArr.append(foundX)
                break

            stdscr.refresh()
    
    command = createCheckCommand(knownPlaintext)
    connection.sendline(command.encode())

    answer = connection.recvline().decode()
    flag = json.loads(answer)["flag"]

    stdscr.addstr(16, 0, f"Flag: {flag}", curses.color_pair(3))
    stdscr.refresh()

    while True:
        pass

curses.wrapper(main)