input_file = "input.txt"
with open(input_file, "r") as file:
    lines = file.readlines()

output_file = "output.txt"
with open(output_file, "w") as file:
    file.write("Hello, World!!\n")
    file.write("Lorem ipsum")

process_file = "file.txt"
with open(process_file, "a+") as file:
    lines = file.readlines()
    file.write("Hello, World!!\n")
    file.write("Lorem ipsum")
