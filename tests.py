from functions.get_file_content import get_file_content

content1 = get_file_content("calculator", "main.py")
print(content1)
content2 = get_file_content("calculator", "pkg/calculator.py")
print(content2)
content3 = get_file_content("calculator", "/bin/cat") #(this should return an error string)
print(content3)
content4 = get_file_content("calculator", "pkg/does_not_exist.py") #(this should return an error string)
print(content4)







# content = get_file_content("calculator", "lorem.txt")
# print(content)




# from functions.get_files_info import get_files_info

# result1 = get_files_info("calculator", ".")
# #expected = (Result for current directory:
#  #- main.py: file_size=576 bytes, is_dir=False
#  #- tests.py: file_size=1343 bytes, is_dir=False
#  #- pkg: file_size=92 bytes, is_dir=True)
#  # assert result1 == expected, f"unexpected result: {result1}"

# print(result1)

# result2 = get_files_info("calculator", "pkg")
# print(result2)

# result3 = get_files_info("calculator", "/bin")
# print(result3)

# result4 = get_files_info("calculator", "../")
# print(result4)