from tools import *


class Tx:
    def __init__(self, blockchain):
        self.tx_inputs = ""
        self.tx_outputs = ""
        self.version = uint32(blockchain)
        self.tx_in_count = var_int(blockchain)
        for i in range(0, self.tx_in_count):
            self.tx_inputs += f"{TxInput(blockchain)}\n"
        self.tx_out_count = var_int(blockchain)
        if self.tx_out_count > 0:
            for i in range(0, self.tx_out_count):
                self.tx_outputs += f"{TxOutput(blockchain)}\n"
        self.lockTime = uint32(blockchain)

    def __str__(self):
        return f"{'=' * 50} New Transaction {'=' * 42}\n" \
               f"{'Tx Version:':15}{self.version}\n" \
               f"{'Input Count:':15}{self.tx_in_count}\n" \
               f"{'Output Count:':15}{self.tx_out_count}\n" \
               f"{'Lock Time:':15}{self.lockTime}\n" \
               f"{self.tx_inputs}" \
               f"{self.tx_outputs}"


class TxInput:
    def __init__(self, blockchain):
        self.prev_block = double_hash_char(blockchain, 32)
        self.tx_out_id = uint32(blockchain)
        self.script_len = var_int(blockchain)
        self.script_sig = char(blockchain, self.script_len)
        self.seq_no = uint32(blockchain)

    def __str__(self):
        return f"{'=' * 50} Transaction Input {'=' * 40}\n" \
               f"{'Previous Hash:':15}{self.prev_block}\n" \
               f"{'Index:':15}{self.tx_out_id}\n" \
               f"{'Script Length:':15}{self.script_len}\n" \
               f"{'Script Sig:':15}{self.script_sig}\n" \
               f"{'Sequence #:':15}{self.seq_no}"


class TxOutput:
    def __init__(self, blockchain):
        self.value = int64(blockchain)
        self.pk_script_len = var_int(blockchain)
        self.pk_script = char(blockchain, self.pk_script_len)

    def __str__(self):
        return f"{'=' * 50} Transaction Output {'=' * 39}\n" \
               f"{'Value:':15}{self.value}\n" \
               f"{'Script Length:':15}{self.pk_script_len}\n" \
               f"{'Script:':15}{self.pk_script}"
