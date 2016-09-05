int tab_a[10] = {1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000};
unsigned int tab_b[10] = {1, 3, 3, 7, 4, 2, 1, 3, 3, 7};
int inv1(unsigned int x)
{
  unsigned int i;
  unsigned int t;
  for (i = 0; i < 10; i++)
    t = tab_a[i] * tab_b[i];

  return tab_a[tab_b[x]];
}

int main(void)
{
  return inv1(3);
}

