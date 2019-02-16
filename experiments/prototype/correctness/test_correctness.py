import os

print("Beginning correctness tests for prototype.")
STATIC_FD = 100


def TEST_1():
	str1 = "Test string."
	ret = os.write(STATIC_FD, str1)

	if (ret != len(str1)):
		print("TEST 1 FAILED: Expected successful write, but write returned diff number than written.")

	ret = -1
	ret = os.read(STATIC_FD, len(str1))

	if (ret != str1):
		print("TEST 1 FAILED: Expected successful read, but not same as what was initially written")

TEST_1()
