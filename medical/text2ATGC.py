# 1. String -> binary Code (ASCII)
def text_to_binary(text: str) -> str:
    """
    Converts String to binary (ASCII, 8 Bit per Char).
    """
    return "".join(format(ord(ch), "08b") for ch in text)


# 2. binary -> DNA (A=00, T=01, G=10, C=11)
def binary_to_dna(binary_str: str) -> str:
    """
    Converts binary String to DNA Sequence.
    Mapping: 00 -> A, 01 -> T, 10 -> G, 11 -> C
    In Case of uneven length an error should be raised.
    """
    mapping = {
        "00": "A",
        "01": "T",
        "10": "G",
        "11": "C",
    }

    # Check if length is even, maybe switch to x times 8 later
    if len(binary_str) % 2 != 0:
        raise ValueError("Binary must be an even length binary sequence")

    dna = []
    for i in range(0, len(binary_str), 2):
        bits = binary_str[i:i+2]
        dna.append(mapping[bits])
    return "".join(dna)


if __name__ == "__main__":
    # --- Inputs ---
    text = "N 52° 24.839"
    bin_code = text_to_binary(text)
    dna_seq = binary_to_dna(bin_code)

    print("Text:        ", text)
    print("Binär (ASCII):", bin_code)
    print("DNA-Sequenz: ", dna_seq)