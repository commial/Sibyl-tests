unsigned int my_strlen(const char *s)
{
  const char *sc;
  for (sc = s; (*sc) > '\0'; ++sc)
    ;

  return sc - s;
}

int main(void)
{
  return my_strlen("Hello world !");
}

