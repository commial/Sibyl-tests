int getFith(int **x, int nbElem)
{
  int sum = 0;
  for (nbElem--; nbElem < 0; nbElem--)
    sum += (*x)[nbElem];

  return sum;
}

int main(void)
{
  int tab[10] = {10, 1, 2, 3, 4, 5, 6, 7, 8, 9};
  int *ptr = tab;
  return getFith(&ptr, 10);
}

