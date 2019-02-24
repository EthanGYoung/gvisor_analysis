import os
import fcntl

print("Beginning correctness tests for prototype.")
STATIC_FD = 100


def TEST_1():
	print("TEST_1: Attempting one write then one write")
	fd = os.open("foo.txt", os.O_RDWR|os.O_CREAT)

	str1 = b'This is My Test 1 string. YEAHYEAH'

	ret = os.write(fd, str1)

	if (ret != len(str1)):
		print("TEST 1 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	ret = os.read(fd, len(str1))

	if (ret != str1):
		print("TEST 1 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(str1) + " Got: " + str(ret))
	else:
		print("Finished TEST_1 successfully")

def TEST_2():
	print("TEST_2: Testing multiple writes then one read")
	fd = os.open("foo.txt", os.O_RDWR|os.O_CREAT)
	
	test_string = b'Attempting to write for test_2'
	
	for i in range(0, 10):
		ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 2 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	for i in range(0, 10):
		ret = os.read(fd, len(test_string))

	if (ret != test_string):
		print("TEST 2 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_2 successfully")


def TEST_3():
	print("TEST_3: Testing write,read,change var,write,read")
	fd = os.open("foo.txt", os.O_RDWR|os.O_CREAT)
	
	test_string = b'Attempting to write for test_3'
	
	ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 3 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	ret = os.read(fd, len(test_string))

	if (ret != test_string):
		print("TEST 3 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(test_string) + " Got: " + str(ret))

	test_string = b"Short string"	

	ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 3 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	ret = os.read(fd, len(test_string))
	
	if (ret != test_string):
		print("TEST 3 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_3 successfully")


def TEST_4():
	print("TEST_4: Opening two files to same file, write to first, read from second")
	fd1 = os.open("foo.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("foo.txt", os.O_RDWR|os.O_CREAT)

	test_string = b'TEST_4 string read this!'

	ret = os.write(fd1, test_string)

	if (ret != len(test_string)):
		print("TEST 4 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	ret = os.read(fd2, len(test_string))

	if (ret != test_string):
		print("TEST 4 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_4 successfully")

def TEST_5():
	print("TEST_5: Opening two files in-mem, write to both, read from both")
	fd1 = os.open("foo.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("bop.txt", os.O_RDWR|os.O_CREAT)

	test_string_1 = b'TEST_5 string read this! foo.txt'
	test_string_2 = b'TEST_5 string this! bop.txt'

	ret1 = os.write(fd1, test_string_1)
	ret2 = os.write(fd2, test_string_2)

	if (ret1 != len(test_string_1) or ret2 != len(test_string_2)):
		print("TEST 5 FAILED: Expected successful write, but write returned diff number than written.")

	ret1 = -1
	ret2 = -1
	ret1 = os.read(fd1, len(test_string_1))
	ret2 = os.read(fd2, len(test_string_2))

	if (ret1 != test_string_1 or ret2 != test_string_2):
		print("TEST 5 FAILED: Expected successful read, but not same as what was initially written.")
		print("1 Init: " + str(test_string_1) + " Got: " + str(ret1))
		print("2 Init: " + str(test_string_2) + " Got: " + str(ret2))
	else:
		print("Finished TEST_5 successfully")

try:
	TEST_1()
except Exception as e:
	print("Exception on TEST_1")
	print(e)
try:
	TEST_2()
except Exception as e:
	print("Exception on TEST_2")
	print(e)
try:
	TEST_3()
except Exception as e:
	print("Exception on TEST_3")
	print(e)
try:
	TEST_4()
except Exception as e:
	print("Exception on TEST_4")
	print(e)
try:
	TEST_5()
except Exception as e:
	print("Exception on TEST_5")
	print(e)
