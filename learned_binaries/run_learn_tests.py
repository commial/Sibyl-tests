import subprocess
import os
import sys
import imp

from elfesteem.elf_init import ELF
from miasm2.analysis.machine import Machine

from sibyl.testlauncher import TestLauncher
from sibyl.abi.x86 import ABI_AMD64
from sibyl.abi.arm import ABI_ARM

from pdb import pm

SHOULD_FAIL = {
    "libc_string.O0_strchr": ['strchr', 'strchr', 'memcmp', 'strchr', 'memcmp', 'strchr', 'memcmp'],
    "libc_string.O0_strrchr": ['strrchr', 'strrchr', 'memcmp', 'strrchr', 'memcmp', 'strrchr', 'memcmp'],
    "libc_string.O0_strcspn": ['strcspn', 'strcspn', 'memcmp', 'strcspn', 'memcmp', 'strcspn', 'memcmp'],
    "libc_string.O0_memcmp": ['memcmp', 'memcmp', 'memcmp'],
    "libc_string.O1_strchr": ['strchr', 'strchr', 'memcmp', 'strchr', 'memcmp', 'strchr', 'memcmp'],
    "libc_string.O1_strrchr": ['strrchr', 'strrchr', 'memcmp', 'strrchr', 'memcmp', 'strrchr', 'memcmp'],
    "libc_string.O1_strcspn": ['strcspn', 'strcspn', 'memcmp', 'strcspn', 'memcmp', 'strcspn', 'memcmp'],
    "libc_string.O1_memcmp": ['memcmp', 'memcmp', 'memcmp'],
    "libc_string.O2_strchr": ['strchr', 'strchr', 'memcmp', 'strchr', 'memcmp', 'strchr', 'memcmp'],
    "libc_string.O2_strrchr": ['strrchr', 'strrchr', 'memcmp', 'strrchr', 'memcmp', 'strrchr', 'memcmp'],
    "libc_string.O2_strcspn": ['strcspn', 'strcspn', 'memcmp', 'strcspn', 'memcmp', 'strcspn', 'memcmp'],
    "libc_string.O2_memcmp": ['memcmp', 'memcmp', 'memcmp'],
    "libc_string.O3_strchr": ['strchr', 'strchr', 'memcmp', 'strchr', 'memcmp', 'strchr', 'memcmp'],
    "libc_string.O3_strrchr": ['strrchr', 'strrchr', 'memcmp', 'strrchr', 'memcmp', 'strrchr', 'memcmp'],
    "libc_string.O3_strcspn": ['strcspn', 'strcspn', 'memcmp', 'strcspn', 'memcmp', 'strcspn', 'memcmp'],
    "libc_string.O3_memcmp": ['memcmp', 'memcmp', 'memcmp'],

    "noret.O0_vec_add": ['vec_add'],
    "noret.O1_vec_add": ['vec_add', 'vec_add', 'vec_add'],
    "noret.O2_vec_add": ['vec_add', 'vec_add', 'vec_add'],
    "noret.O3_vec_add": ['vec_add', 'vec_add', 'vec_add'],
    "noret.arm_vec_add": ['vec_add'],

    "refres1.O0_ret_ref1": [],
    "refres1.O1_ret_ref1": ['ret_ref1', 'ret_ref2', 'ret_ref2'],
    "refres1.O2_ret_ref1": ['ret_ref1', 'ret_ref1'],
    "refres1.O3_ret_ref1": ['ret_ref1', 'ret_ref1'],
    "refres1.arm_ret_ref1": [],

    "refres2.O0_ret_ref2": [],
    "refres2.O1_ret_ref2": ['ret_ref2'],
    "refres2.O2_ret_ref2": ['ret_ref1', 'ret_ref2', 'ret_ref2'],
    "refres2.O3_ret_ref2": ['ret_ref1', 'ret_ref2', 'ret_ref2'],
    "refres2.arm_ret_ref2": [],

    "string.O0_my_strcpy": ['my_strcpy'],
    "string.O1_my_strcpy": ['strcpy', 'strcpy', 'strcpy', 'strcpy', 'my_strcpy', 'my_strcpy', 'my_strcpy', 'my_strcpy'],
    "string.O2_my_strcpy": ['strcpy', 'strcpy', 'strcpy', 'strcpy', 'my_strcpy', 'my_strcpy', 'my_strcpy', 'my_strcpy'],
    "string.O3_my_strcpy": ['strcpy', 'strcpy', 'strcpy', 'strcpy', 'my_strcpy', 'my_strcpy', 'my_strcpy', 'my_strcpy'],
    "string.arm_my_strcpy": ['my_strcpy'],
}

WRONG_MUTANTS = ["mutants/strlen_my_strlen.1mut",
                "mutants/inv_ordre2_inv2.1mut",
                "mutants/inv_ordre2_inv2.2mut",
                "mutants/inv_ordre2_inv2.3mut",
                "mutants/inv_ordre1_inv1.1mut",
                "mutants/inv_ordre1_inv1.2mut",
                "mutants/inv_ordre1_inv1.3mut",
]

EQUIVALENT_FUNCTIONS=[("sbox_stack","sbox_data"),("inv1","inv2"),("ret_ref1","ret_ref1"),("my_strcpy","strcpy")]

def equivalent_func(func):
    ret = [func]
    for (f1, f2) in EQUIVALENT_FUNCTIONS:
        if f1 == func:
            ret += [f2]
        elif f2 == func:
            ret += [f1]
    return ret

def find_func_by_name(elf, func):
    try:
        for name, symb in elf.getsectionbyname(".symtab").symbols.iteritems():
            if name == func:
                return symb.value
    except:
        return -1


devnull = open(os.devnull, "w")
old_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", 0)

def close_stderr():
    os.close(sys.stderr.fileno())
    sys.stderr = os.fdopen(os.dup(devnull.fileno()), "w", 0)

def reopen_stderr():
    sys.stderr = os.fdopen(os.dup(old_stderr.fileno()), "w", 0)


func_names = {}

for test in open("function_names.txt"):
    if test != "\n":
        test = test[:-1].split()
        func_names[test[0][:-2]] = test[1:]


machineX86 = Machine("x86_64")
machineARM = Machine("arml")

list_class = []


print "Learning all functions"

c_files = []
for cur_dir, sub_dir, files in os.walk("."):
    c_files += [x for x in files if x.endswith((".O0",".O1",".O2",".O3"))]
c_files.sort()
stdout = ""
for c_file in c_files:
    for func_name in func_names["".join(c_file.split('.')[:-1])]:

        print "\tlearning "+func_name+" on "+c_file

        with open(c_file) as fdesc:
            elf = ELF(fdesc.read())

        main_addr = find_func_by_name(elf, "main")
        func_addr = find_func_by_name(elf, func_name)

        cmd = "sibyl learn -t miasm -a %s -m %s %s %s" % (hex(func_addr),
                                                          hex(main_addr),
                                                          func_name+"_"+c_file.split('.')[-1:][0],
                                                          c_file)
        sibyl = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tmp_stdout, stderr = sibyl.communicate()

        stdout += tmp_stdout

mod = imp.new_module("testclass")
exec stdout in mod.__dict__

for c_file in c_files:
    for func_name in func_names["".join(c_file.split('.')[:-1])]:
        classTest = getattr(mod, "Test"+func_name+"_"+c_file.split('.')[-1:][0]
        )
        list_class += [classTest]


print "Replaying created tests on all functions"


c_files = []
for cur_dir, sub_dir, files in os.walk("."):
    c_files += [x for x in files if x.endswith((".O0",".O1",".O2",".O3",".arm"))]
c_files.sort()

for c_file in c_files:
    for func_name in func_names["".join(c_file.split('.')[:-1])]:

        with open(c_file) as fdesc:
            elf = ELF(fdesc.read())
        func_addr = find_func_by_name(elf, func_name)

        abi = ABI_AMD64
        machine = machineX86
        if c_file.endswith(".arm"):
            machine = machineARM
            abi = ABI_ARM

        print "\treplay for "+func_name+" on "+c_file,

        tl = TestLauncher(c_file, machine, abi, list_class, "gcc")

        close_stderr()
        possible_funcs = tl.run(func_addr)
        reopen_stderr()

        possible_funcs = ["_".join(possible_func.split('_')[:-1]) for possible_func in possible_funcs]

        eq_names = equivalent_func(func_name)

        try:
            isTestOK = len(possible_funcs)-4*len(eq_names)==0 and len([func for func in possible_funcs if func not in eq_names])==0
            if c_file+"_"+func_name in SHOULD_FAIL:
                assert sorted(possible_funcs) == sorted(SHOULD_FAIL[c_file+"_"+func_name])
            else:
                assert isTestOK
        except AssertionError as e:
            print c_file, func_name, possible_funcs
            raise e

        print " is OK !",
        sys.stderr.write("\n")

print "Replaying created tests on mutated functions"

c_files = []
for cur_dir, sub_dir, files in os.walk("."):
    c_files += [x for x in files if x.endswith((".O0"))]

mut_files = []
for cur_dir, sub_dir, files in os.walk("mutants"):
    mut_files += ["mutants/"+x for x in files if x.endswith("mut")]

for c_file in c_files:
    for func_name in func_names["".join(c_file.split('.')[:-1])]:
        for mut in mut_files:
            if os.path.basename(mut).startswith(c_file[:-3]+"_"+func_name):

                with open(mut) as fdesc:
                    elf = ELF(fdesc.read())
                func_addr = find_func_by_name(elf, func_name)

                print "\treplay for "+func_name,

                tl = TestLauncher(mut, machineX86, ABI_AMD64, list_class, "gcc")

                close_stderr()
                possible_funcs = tl.run(func_addr)
                reopen_stderr()

                eq_names = equivalent_func(func_name)

                try:
                    if mut not in WRONG_MUTANTS:
                        assert len([f for f in possible_funcs if f in func_name]) == 0
                except:
                    print mut, func_name, eq_names, possible_funcs

                print " is OK !",
                sys.stderr.write("\n")


