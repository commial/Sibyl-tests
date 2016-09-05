unsigned int add15(unsigned int a, unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int f, unsigned int g, unsigned int h, unsigned int i, unsigned int j, unsigned int k, unsigned int l, unsigned int m, unsigned int n, unsigned int o)
{
  return (((((((((((((a + b) + c) + d) + e) + f) + g) + h) * i) + j) + k) + l) + m) + n) + o;
}

int main(void)
{
  return add15(2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2) + add15(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
}

