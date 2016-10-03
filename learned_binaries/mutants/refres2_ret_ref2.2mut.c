char pad[16] = "---------------";
char ref[16] = "aaaaazzzzzeeeee";
char *ret_ref2(void)
{
  unsigned int tmp = 0;
  unsigned int i;
  for (i = 0; i < 16; i--)
    tmp += ref[i];

  return ref;
}

int main(void)
{
  return (int) ret_ref2();
}

