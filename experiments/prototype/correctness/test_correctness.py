import os

print("Beginning correctness tests for prototype.")
STATIC_FD = 100


def TEST_1():
	fd = os.open("foo.txt", os.O_RDWR|os.O_CREAT)

	str1 = b'This is My Test 1 string. YEAHYEAH'
	ret = os.write(fd, str1)

	if (ret != len(str1)):
		print("TEST 1 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	os.lseek(fd, 0, 0)
	ret = os.read(fd, len(str1))
	print("Getting: %s as returned value"%ret)
	print("Should be: ",str1)

	if (ret != str1):
		print("TEST 1 FAILED: Expected successful read, but not same as what was initially written.")
		print("Init: " + str(str1) + " Got: " + str(ret))

	print("Finished TEST_1")

def TEST_2():

	str1 = b'Test2'
	ret = os.write(STATIC_FD, str1)

	if (ret != len(str1)):
		print("TEST 2 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	ret = os.read(STATIC_FD, len(str1))

	if (ret != str1):
		print("Getting: %s as returned value"%ret)
		print("Should be: ",str1)
		print("TEST 2 FAILED: Expected successful read, but not same as what was initially written")

	print("Finished TEST_2")
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
