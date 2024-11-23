
import struct

def parse_and_convert(input_file, output_file):
    try:
        # Abrindo os arquivos de entrada e saída
        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "wb") as outfile:
            current_address = 0
            array_addresses = []

            for line in infile:
                line = line.strip()
                if not line or line.startswith("#"):  # Ignorar linhas vazias ou comentários
                    continue
                
                type_indicator = line[0]  # O primeiro caractere indica o tipo
                values = line[1:].strip()  # O restante contém os valores

                # Processar com base no tipo
                if type_indicator == "i":  # Inteiros de 32 bits
                    numbers = [int(x) for x in values.split(",")]
                    for number in numbers:
                        outfile.write(struct.pack("i", number))
                        current_address += 4

                elif type_indicator == "f":  # Floats de 32 bits
                    numbers = [float(x) for x in values.split(",")]
                    for number in numbers:
                        outfile.write(struct.pack("f", number))
                        current_address += 4

                elif type_indicator == "c":  # Caracteres (1 byte cada)
                    chars = [chr(int(x)) for x in values.split(",")]
                    for char in chars:
                        outfile.write(struct.pack("c", char.encode("latin1")))
                        current_address += 1

                elif type_indicator == "s":  # Strings
                    string = values.replace("\\n", "\n").replace("\\r", "\r")
                    outfile.write(string.encode("utf-8"))
                    current_address += len(string)

                elif type_indicator == "z":  # Buffer de bytes zero
                    count = int(values)
                    outfile.write(b"\x00" * count)
                    current_address += count

                elif type_indicator == "h":  # Hexadecimais
                    hex_values = [int(x, 16) for x in values.split(",")]
                    for value in hex_values:
                        outfile.write(struct.pack("B", value))
                        current_address += 1

                # Registrar o endereço inicial da array
                array_addresses.append((line, current_address))

        # Imprimindo endereços
        print("\nEndereços de início de cada array:")
        for line, address in array_addresses:
            print(f"Linha: {line} -> Endereço inicial: {address:08X}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    input_file = input("Digite o nome do arquivo de entrada (.txt): ").strip()
    if not input_file.endswith(".txt"):
        print("Erro: O arquivo deve ter a extensão .txt")
        return

    output_file = input_file.replace(".txt", ".dat")
    parse_and_convert(input_file, output_file)
    print(f"\nArquivo binário gerado: {output_file}")


if __name__ == "__main__":
    main()
