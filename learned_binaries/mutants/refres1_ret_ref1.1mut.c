char ref[16] = "aaaaazzzzzeeeee";
char pad[16] = "---------------";
char *ret_ref1(void)
{
  unsigned int tmp = 0;
  unsigned int i;
  for (i = 0; i > 16; i++)
    tmp += ref[i];

  return ref;
}

int main(void)
{
  return (int) ret_ref1();
}

