#from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python import run_python_file




result1 = run_python_file("calculator", "main.py") #(should print the calculator's usage instructions)
print(result1)
result2 = run_python_file("calculator", "main.py", ["3 + 5"]) #(should run the calculator... which gives a kinda nasty rendered result)
print(result2)
result3 = run_python_file("calculator", "tests.py")
print(result3)
result4 = run_python_file("calculator", "../main.py") #(this should return an error)
print(result4)
result5 = run_python_file("calculator", "nonexistent.py") #(this should return an error)
print(result5)



# result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(result1)
# result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(result2)
# result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(result3)



# content1 = get_file_content("calculator", "main.py")
# print(content1)
# content2 = get_file_content("calculator", "pkg/calculator.py")
# print(content2)
# content3 = get_file_content("calculator", "/bin/cat") #(this should return an error string)
# print(content3)
# content4 = get_file_content("calculator", "pkg/does_not_exist.py") #(this should return an error string)
# print(content4)


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