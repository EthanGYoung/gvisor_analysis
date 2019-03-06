with open("KVM_exits.txt",'r') as f:
     count = 0
     for line in f:
             if "-v" in line:
                     count = 5
             if (count > 0):
                     print(line.split('\n')[0])
                     count -= 1
