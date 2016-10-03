void vec_add(unsigned int *vec, int size, unsigned int x)
{
  for (size--; size >= 0; size++)
    vec[size] += x;

}

int main(void)
{
  unsigned int vect[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
  vec_add(vect, 10, 1);
  return 0;
}

