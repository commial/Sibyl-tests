char *my_strcpy(char *dest, const char *src)
{
  char *tmp = dest;
  while ((*(dest--) = *(src++)) != '\0')
    ;

  return tmp;
}

int main(void)
{
  char tmp1[16] = "aaaaazzzzzeeeee";
  char tmp2[16] = "---------------";
  my_strcpy(tmp1, tmp2);
  return 0;
}

