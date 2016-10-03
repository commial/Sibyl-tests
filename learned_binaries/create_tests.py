import os

SIMPLE_TEST_LIST = ["15params.c", "inv_ordre1.c", "refres2.c", "several_traces.c", "strlen.c", "inv_ordre2.c", "noret.c", "sbox_data.c", "test.c", "doublePtr.c", "refres1.c", "sbox_stack.c", "string.c"]

LIBC_TEST_LIST = ["libc_string.c"]

func_names = {}
for test in open("function_names.txt"):
    if test != "\n":
        test = test[:-1].split()
        func_names[test[0][:-2]] = test[1:]

for test in SIMPLE_TEST_LIST:

    test_name = test[:-2]
    
    os.system("gcc -fno-inline-functions -fno-stack-protector -O0 -o %s %s" % (test_name+".O0", test))
    os.system("gcc -fno-inline-functions -fno-stack-protector -O1 -o %s %s" % (test_name+".O1", test))
    os.system("gcc -fno-inline-functions -fno-stack-protector -O2 -o %s %s" % (test_name+".O2", test))
    os.system("gcc -fno-inline-functions -fno-stack-protector -O3 -o %s %s" % (test_name+".O3", test))
    
    os.system("arm-none-eabi-gcc --specs=nosys.specs -o %s %s" % (test_name+".arm", test))

    for func_name in func_names[test_name]:
        os.system("python create_mutant.py -f %s -n %s" % (test, func_name))

os.system("make -k -C mutants")
    
for test in LIBC_TEST_LIST:
    diet_path = "../dietlibc-0.33"

    test_name = test[:-2]
    
    os.system(diet_path + "/bin-x86_64/diet gcc -fno-inline-functions -fno-stack-protector -O0 -o %s %s -static" % (test_name+".O0", test)) 
    os.system(diet_path + "/bin-x86_64/diet gcc -fno-inline-functions -fno-stack-protector -O1 -o %s %s -static" % (test_name+".O1", test)) 
    os.system(diet_path + "/bin-x86_64/diet gcc -fno-inline-functions -fno-stack-protector -O2 -o %s %s -static" % (test_name+".O2", test)) 
    os.system(diet_path + "/bin-x86_64/diet gcc -fno-inline-functions -fno-stack-protector -O3 -o %s %s -static" % (test_name+".O3", test))    
