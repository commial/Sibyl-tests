char ref[16] = "aaaaazzzzzeeeee";	
char pad[16] = "---------------";	

char * ret_ref1(void)
{
	unsigned int tmp=0,i;
	for(i=0;i<16;i++)
		tmp += ref[i];
	return ref;
}

#ifdef __GNUC__
#ifndef __clang__
int main(void) __attribute__((optimize("-O0")));
#endif
#endif
int main(void) {
	return (int)ret_ref1();
}
