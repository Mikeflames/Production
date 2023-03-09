# Import a Text file and display its contents

# Open the file for reading
# file=open('potting_coating\PART_TABLE.txt',"r")
# data=file.readlines()
# print(data[0])


with open('potting_coating\PART_TABLE.txt', 'rb') as f:
    byte_sequence = f.read()


ptf_file_content = byte_sequence.decode('utf-8')
