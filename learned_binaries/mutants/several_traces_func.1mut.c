int func(int a, int b, unsigned char addOrMul)
{
  if (addOrMul)
    return a / b;
  else
    return a * b;

}

int main(void)
{
  return (func(42, 42, 0) + func(-42, 1337, 1)) + func(4, 2, 0);
}

