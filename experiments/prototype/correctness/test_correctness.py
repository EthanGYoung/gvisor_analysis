import os
import fcntl

print("Beginning correctness tests for prototype.")
STATIC_FD = 100


def TEST_1():
	print("TEST_1: Attempting one write then one write")
	fd = os.open("test_1.txt", os.O_RDWR|os.O_CREAT)

	str1 = b'This is My Test 1 string. YEAHYEAH'

	ret = os.write(fd, str1)


	if (ret != len(str1)):
		print("TEST 1 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 1 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	ret = -1
	ret = os.read(fd, len(str1))

	if (ret != str1):
		print("TEST 1 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(str1) + " Got: " + str(ret))
	else:
		print("Finished TEST_1 successfully")

def TEST_2():
	print("TEST_2: Testing multiple writes then one read")
	fd = os.open("test_2.txt", os.O_RDWR|os.O_CREAT)

	test_string = b'Attempting to write for test_2'

	for i in range(0, 10):
		ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 2 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 2 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

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
	fd = os.open("test_3.txt", os.O_RDWR|os.O_CREAT)

	test_string = b'Attempting to write for test_3'

	ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 3 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 3 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	ret = -1
	ret = os.read(fd, len(test_string))

	if (ret != test_string):
		print("TEST 3 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(test_string) + " Got: " + str(ret))

	test_string = b"Short string"

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 3 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))


	ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 3 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 3 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	ret = -1
	ret = os.read(fd, len(test_string))

	if (ret != test_string):
		print("TEST 3 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_3 successfully")


def TEST_4():
	print("TEST_4: Opening two files to same file, write to first, read from second")
	fd1 = os.open("test_4.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("test_4.txt", os.O_RDWR|os.O_CREAT)

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
	fd1 = os.open("test_5_1.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("test_5_2.txt", os.O_RDWR|os.O_CREAT)

	test_string_1 = b'TEST_5 string read this! test_5_1.txt'
	test_string_2 = b'TEST_5 string this! test_5_2.txt'

	ret1 = os.write(fd1, test_string_1)
	ret2 = os.write(fd2, test_string_2)

	if (ret1 != len(test_string_1) or ret2 != len(test_string_2)):
		print("TEST 5 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd1, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 5 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	seek = os.lseek(fd2, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 5 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

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

def TEST_6():
	print("TEST_6: Open file, write to it, lseek to middle, write, read and check if overwrite")
	fd = os.open("test_6.txt", os.O_RDWR|os.O_CREAT)

	test_string = b'Test string for test number 6.'

	ret = os.write(fd, test_string)

	if (ret != len(test_string)):
		print("TEST 6 FAILED: Expected successful write, but write returned diff number than written.")

	SEEK_LEN = 5
	seek = os.lseek(fd, SEEK_LEN, os.SEEK_SET)

	if (seek != SEEK_LEN):
		print("TEST 6 FAILED: seek position not equal to target SEEK_LEN")

	add_string = b"added"
	ret = os.write(fd, add_string)

	if (ret != len(add_string)):
		print("TEST 6 FAILED: Expected successful write (2), but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 6 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	expected = test_string[0:SEEK_LEN] + add_string + test_string[SEEK_LEN + len(add_string):len(test_string)]
	ret = os.read(fd, len(test_string))

	if (ret != expected):
		print("TEST 6 FAILED: Expected " + str(expected) + " Got: " + str(ret))
	else:
		print("Finished TEST_6 successfully")

def TEST_7():
	print("TEST_7: Open file with create flag, open without, check point to same file")

	fd1 = os.open("test_7.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("test_7.txt", os.O_RDWR)

	test_string = b'Test string for test number 7.'

	ret = os.write(fd1, test_string)
	if (ret != len(test_string)):
		print("TEST 7 FAILED: Expected successful write, but write returned diff number than written.")

	ret = os.read(fd2, len(test_string))
	if (ret != test_string):
		print("TEST_7 FAILED: Expected to read: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_7 successfully")

def TEST_8():
	print("TEST_8: Write over boundary block size and read all successfully")
	BLOCK_SIZE = 1100000
	test_string = bytearray([1]*2*BLOCK_SIZE)

	fd = os.open("test_8.txt", os.O_RDWR|os.O_CREAT)

	ret = os.write(fd, test_string)
	if (ret != len(test_string)):
		print("TEST 8 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)

	if (seek != 0):
		print("TEST 8 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	ret = os.read(fd, len(test_string))
	if (ret != test_string):
		print("TEST_8 FAILED: Expected to read: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_8 successfully")

def TEST_9():
	print("TEST_9: Open and close file")
	fd = os.open("test_9.txt", os.O_RDWR|os.O_CREAT)
	os.close(fd)
	try:
		os.write(fd, b'Test')
		print("TEST_9 FAILED: Expected exception.")
	except:
		print("Finished TEST_9 successfully")

def TEST_10():
	print("TEST_10: Open same file twice, write to one, close one, and read from the still open fd")
	fd1 = os.open("test_10.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("test_10.txt", os.O_RDWR|os.O_CREAT)

	test_string = b'Test string for test number 10.'

	ret = os.write(fd1, test_string)
	if (ret != len(test_string)):
		print("TEST 10 FAILED: Expected successful write, but write returned diff number than written.")

	os.close(fd1)

	ret = os.read(fd2, len(test_string))
	if (ret != test_string):
		print("TEST_10 FAILED: Expected to read: " + str(test_string) + " Got: " + str(ret))
	else:
		print("Finished TEST_10 successfully")

def TEST_11():
	print("TEST_11: Open file with append, write twice, seek to front, read total and check that it is the length of both")
	fd = os.open("test_11.txt", os.O_RDWR|os.O_CREAT|os.O_APPEND)
	test_string_1 = b'This is the init string.'

	ret = os.write(fd, test_string_1)
	if (ret != len(test_string_1)):
		print("TEST 11 FAILED: Expected successful write, but write returned diff number than written.")

	test_string_2 = b'Second string that I will add'

	ret = os.write(fd, test_string_2)
	if (ret != len(test_string_2)):
		print("TEST 11 FAILED: Expected successful write, but write returned diff number than written.")

	seek = os.lseek(fd, 0, os.SEEK_SET)
	if (seek != 0):
		print("TEST 11 FAILED: Attempted to seek to beginning of file. Got: " + str(seek))

	ret = os.read(fd, len(test_string_1) + len(test_string_2))
	if (ret != (test_string_1 + test_string_2)):
		print("TEST_11 FAILED: Expected to read: " + str(test_string_1 + test_string_2) + " Got: " + str(ret))
	else:
		print("Finished TEST_11 successfully")

def TEST_12():
	print("TEST_12: import numpy and use it")
	import numpy as np
	a = np.array([[1,2],[3,4]])
	b = np.array([[5,6],[7,8]])
	ret = np.multiply(a,b)
	exp = np.array([[ 5, 12],[21, 32]])
	if (not np.array_equal(ret,exp)):
		print("TEST_12 FAILED: Expected: " + str(exp) + " Got: " + str(ret))
	else:
		print("Finished TEST_12 successfully")

def TEST_13():
	print("TEST_13: open and close")
	fd1 = os.open("test_13.txt", os.O_RDWR|os.O_CREAT)

	fd1_ret = os.close(fd1)
	if ((fd1_ret != None)):
		print("TEST_13 FAILED: Expected: None Got: " + str(fd1_ret))
	else:
		print("Finished TEST_13 successfully")

def TEST_14():
	print("TEST_14: open two files in differennt fs close")
	fd1 = os.open("test_14.txt", os.O_RDWR|os.O_CREAT)
	fd2 = os.open("test_14.txt", os.O_RDWR)

	test_string = b'Test string for test number 14.'

	ret1 = os.write(fd1, test_string)
	if (ret1 != len(test_string)):
		print("TEST 14 FAILED: Expected successful write, but write returned diff number than written.")
	ret2 = os.write(fd2, test_string)
	if (ret2 != len(test_string)):
		print("TEST 14 FAILED: Expected successful write, but write returned diff number than written.")

	fd1_ret = os.close(fd1)
	fd2_ret = os.close(fd2)
	if ((fd1_ret != None)):
		print("TEST_14 FAILED: Expected: None Got: " + str(fd1_ret))
	else:
		print("Finished TEST_14 part A successfully")
	if ((fd2_ret != None)):
		print("TEST_14 FAILED: Expected: None Got: " + str(fd2_ret))
	else:
		print("Finished TEST_14 part B successfully")

def TEST_15():
	print("TEST_15: Open and close file and create a new one with the same name and read directly")
	fd = os.open("test_15.txt", os.O_RDWR|os.O_CREAT)
	test_string = b'Test string for test number 15.'
	os.write(fd, test_string)
	os.close(fd)
	fd = os.open("test_15.txt", os.O_RDWR|os.O_CREAT)
	ret = os.read(fd, len(test_string))
	if (ret == test_string):
		print("TEST_15 FAILED: Expected to read: None Got: " + str(ret))
	else:
		print("Finished TEST_15 successfully")

def TEST_16():
	print("TEST_16: Open and close file read directly")
	fd = os.open("test_16.txt", os.O_RDWR|os.O_CREAT)
	test_string = b'Test string for test number 16.'
	os.close(fd)
	ret = os.read(fd, len(test_string))
	if (ret == test_string):
		print("TEST_16 FAILED: Expected to read: None Got: " + str(ret))
	else:
		print("Finished TEST_16 successfully")

def TEST_17():
	print("TEST_17: Open and read directly")
	fd = os.open("test_17.txt", os.O_RDWR|os.O_CREAT)
	test_string = b'Test string for test number 17.'
	ret = os.read(fd, len(test_string))
	if (ret == test_string):
		print("TEST_17 FAILED: Expected to read: None Got: " + str(ret))
	else:
		print("Finished TEST_17 successfully")
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
try:
	TEST_6()
except Exception as e:
	print("Exception on TEST_6")
	print(e)
try:
	TEST_7()
except Exception as e:
	print("Exception on TEST_7")
	print(e)
try:
	TEST_8()
except Exception as e:
	print("Exception on TEST_8")
	print(e)
try:
	TEST_9()
except Exception as e:
	print("Exception on TEST_9")
	print(e)
try:
	TEST_10()
except Exception as e:
	print("Exception on TEST_10")
	print(e)
try:
	TEST_11()
except Exception as e:
	print("Exception on TEST_11")
	print(e)
try:
	TEST_12()
except Exception as e:
	print("Exception on TEST_12")
	print(e)
try:
	TEST_13()
except Exception as e:
	print("Exception on TEST_13")
	print(e)
try:
	TEST_14()
except Exception as e:
	print("Exception on TEST_14")
	print(e)
try:
	TEST_15()
except Exception as e:
	print("Exception on TEST_15")
	print(e)
try:
	TEST_16()
except Exception as e:
	print("Exception on TEST_16")
	print(e)
try:
	TEST_17()
except Exception as e:
	print("Exception on TEST_17")
	print(e)
