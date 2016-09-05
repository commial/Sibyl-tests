import argparse
import random
import copy
from pycparser import c_parser, parse_file, c_ast, c_generator

MAX_MUTANT = 100

class ParentNodeVisitor(c_ast.NodeVisitor):
    def __init__(self):
        super(ParentNodeVisitor, self).__init__()
        self.current_parent = None
    
    def generic_visit(self, node):
        oldparent = self.current_parent
        self.current_parent = node
        for c_name, c in node.children():
            self.visit(c)
        self.current_parent = oldparent

comOpList = ["==", "!=","<", ">","<=",">="]
arithOpList = ["+", "-", "*", "/", "%"]
boolOpList = ["&&","||"]
bitOpList = ["&","|","^","<<",">>"]
def binaryOpTrick(op):
    if op in comOpList:
        print 
	return filter(lambda x: x!=op , comOpList)[random.randint(0,len(comOpList)-2)]
    elif op in arithOpList:
        return filter(lambda x: x!=op , arithOpList)[random.randint(0,len(arithOpList)-2)]
    elif op in boolOpList:
        return filter(lambda x: x!=op , boolOpList)[random.randint(0,len(boolOpList)-2)]
    elif op in bitOpList:
        return filter(lambda x: x!=op , bitOpList)[random.randint(0,len(bitOpList)-2)]
    raise ValueError("binary operator unknown :"+op)

incrOpList = ["++", "--"]
def UnaryOpTrick(op):
    return filter(lambda x: x!=op , incrOpList)[random.randint(0,len(incrOpList)-2)]
        
class OperationFlip(c_ast.NodeVisitor):
    def visit_UnaryOp(self, node):
        global global_trick_counter
        trick = UnaryOpTrick(node.op[-2:])        
        if node.op[-2:] in incrOpList:
            if global_do_trick:
                global_trick_counter -= 1
                if global_trick_counter == 0:
                    node.op = node.op[:-2] + UnaryOpTrick(node.op[-2:])
            else:
                global_trick_counter+= 1;
        self.generic_visit(node)

    def visit_BinaryOp(self, node):
        global global_trick_counter
        if global_do_trick:
            global_trick_counter -= 1
            if global_trick_counter == 0:
                node.op = binaryOpTrick(node.op)
        else:
            global_trick_counter+= 1;        
        self.generic_visit(node)

class ConstantReset(c_ast.NodeVisitor):
    def visit_Constant(self, node):
        global global_trick_counter
        if node.type == 'int':
            if global_do_trick:
                global_trick_counter -= 1
                if global_trick_counter == 0:
                    node.value = "1337"
            else:
                global_trick_counter+= 1;
        elif node.type == 'char':
            if global_do_trick:
                global_trick_counter -= 1
                if global_trick_counter == 0:
                    if node.value[0] == '"':
                        node.value = '\x00'
                    else:
                        node.value = '"1337"'
            else:
                global_trick_counter+= 1;

class IfWhileSwitch(ParentNodeVisitor):
    def visit_While(self, node):
        global global_trick_counter
        if isinstance(self.current_parent, c_ast.Compound):
            for i in xrange(len(self.current_parent.block_items)):
                if self.current_parent.block_items[i] == node:
                    if global_do_trick:
                        global_trick_counter -= 1
                        if global_trick_counter == 0:
                            self.current_parent.block_items[i] = c_ast.If(node.cond, node.stmt, None, node.coord)
                    else:
                        global_trick_counter+= 1;
                    
    def visit_If(self, node):
        global global_trick_counter
        if isinstance(self.current_parent, c_ast.Compound):
            for i in xrange(len(self.current_parent.block_items)):
                if self.current_parent.block_items[i] == node:
                    if global_do_trick:
                        global_trick_counter -= 1
                        if global_trick_counter == 0:
                            self.current_parent.block_items[i] = c_ast.While(node.cond, node.iftrue, node.coord)
                    else:
                        global_trick_counter+= 1;
        
class SearchFunction(c_ast.NodeVisitor):
    def __init__(self, functionName):
        super(SearchFunction, self).__init__()
        self.functionName = functionName
    
    def visit_FuncDef(self, node):
        if node.decl.name == self.functionName:
            # We do not use constant modification because it implies to many false negative test cases
            # ConstantReset().visit(node)        
            OperationFlip().visit(node)  
            IfWhileSwitch().visit(node)     

            
def create_mutants(file, prefFile, prefOut, name, stdin=False, lib=r'-Itests/fake_libc_include', changeName=True):
    
    global global_do_trick
    global global_trick_counter

    global_do_trick = False
    global_trick_counter = 0


# We want reproductible pseudo-random numbers generator
    random.seed(0)

    parser = c_parser.CParser()
    ast = parse_file(prefFile + file, use_cpp=True, cpp_path='clang', cpp_args=['-E', lib]) # We use clang to avoid gcc "__attribute__"
    savedAst = copy.deepcopy(ast)
    
    SearchFunction(name).visit(ast)
    generator = c_generator.CGenerator()

    nbTrickToDo = min(global_trick_counter, MAX_MUTANT)
    global_do_trick = True
    
    # Draw without replacement (tirage sans remise)
    tricksToDo = []
    tricks = range(1, global_trick_counter+1)
    for i in xrange(nbTrickToDo):
        n = random.randint(1,global_trick_counter)
        tricksToDo += [tricks[n-1]]
        (tricks[n-1], tricks[global_trick_counter-1]) = (tricks[global_trick_counter-1], tricks[n-1])
        global_trick_counter -= 1

    generator = c_generator.CGenerator()
    for trick in tricksToDo:
        global_trick_counter = trick
        ast = copy.deepcopy(savedAst)
        SearchFunction(name).visit(ast)
        if not stdin:
            if changeName:
                open(prefOut+file[:-2]+"_"+name+"."+str(trick)+"mut.c", "w").write(generator.visit(ast))
            else:
                open(prefOut+file[:-2]+"."+str(trick), "w").write(generator.visit(ast))
        else:
            print generator.visit(ast)
            print "-------------------------------------------"


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="C source mutator")
    parser.add_argument("-f", "--file", help="absolute filename", required=True)
    parser.add_argument("-n", "--name", help="function name", required=True)
    parser.add_argument("-s", "--stdin", help="use stdin instead of files", action="store_true", default=False)
    parser.add_argument("-po", "--prefout", help="output prefix file")
    parser.add_argument("-pi", "--prefin", help="input prefix file")
    parser.add_argument("-c", "--changeName", help="add function name and \"mut\" to the end of the new source file", action="store_false", default=True)
    args = parser.parse_args()

    args.prefout = "mutants/" if args.prefout is None else args.prefout
    args.prefin = "" if args.prefin is None else args.prefin

    create_mutants(args.file, args.prefin, args.prefout, args.name, args.stdin, r'-Ifake_libc_include', args.changeName)
