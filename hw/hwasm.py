import sys

class Assembler:
    @staticmethod
    def processHexValue(hexValue):
        hexValue = hexValue.replace(',', '')
        if len(hexValue) > 4:
            firstHex = int(hexValue[:4], 16)
            secondHex = int('0x' + hexValue[4:], 16)
            return bytes([secondHex, firstHex])

        hexValue = int(hexValue.replace(',', ''), 16)
        return bytes([hexValue])

    @staticmethod
    def processCharValue(charValue: str):
        return charValue.replace(',', '').replace('\'', '').encode('utf-8')

    @staticmethod
    def getRegisterMovOpcode(register):
        return {
            'al': bytes([176]),
            'ah': bytes([180])
        }.get(register)

    @staticmethod
    def processMovInstruction(instructions, index):
        value = instructions[index + 1].replace('$', '')
        register = instructions[index + 2].replace('%', '')

        if register[0] == '\'':
            register = instructions[index + 3].replace('%', '')

        prefix = value[0]
        if prefix == '0':
            value = Assembler.processHexValue(value)
        if prefix == '\'':
            value = Assembler.processCharValue(value)

        register = Assembler.getRegisterMovOpcode(register)

        return register + value

    @staticmethod
    def processIntInstruction(instructions, index):
        value = instructions[index + 1].replace('$', '')
        return bytes([205]) + Assembler.processHexValue(value)

    @staticmethod
    def processJmpInstruction(instructions, index):
        return bytes([235, 253])

    @staticmethod
    def processHltInstruction():
        return bytes([255])

    @staticmethod
    def processWordInstruction(instructions, index):
        return bytes([0])

    @staticmethod
    def processInstructions(instructions):
        result = b""
        for index, instruction in enumerate(instructions):
            if instruction == '#':
                break
            elif instruction == 'hlt':
                binary = Assembler.processHltInstruction()
            elif instruction == 'jmp':
                binary = Assembler.processJmpInstruction(instructions, index)
            elif instruction == '.fill':
                binary = bytes(461)
            elif instruction == 'mov':
                binary = Assembler.processMovInstruction(instructions, index)
            elif instruction == 'int':
                binary = Assembler.processIntInstruction(instructions, index)
            elif instruction == '.word':
                binary = Assembler.processWordInstruction(instructions, index)
            else:
                continue

            result += binary

        return result

    @staticmethod
    def main():
        inputFilename, outputFilename = sys.argv[1], sys.argv[2]

        with open(inputFilename, "r") as inputFile:
            with open(outputFilename, "wb") as outputFile:
                for line in inputFile:
                    instructions = line.rstrip().split()
                    binaryData = Assembler.processInstructions(instructions)
                    outputFile.write(binaryData)

if __name__ == '__main__':
    Assembler.main()
