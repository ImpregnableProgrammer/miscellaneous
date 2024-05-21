#include <stdio.h>
#include <stdlib.h>

struct item
{
  int a;
};

int main()
{
  int array2D[][3][4] = {1, 2, 3, 4, 5, 6, 7, 8}; // Huh, interesting, this compiles...
  struct item *i = malloc(sizeof(*i));
  printf("%d\narray2D[0][2] = %d\n", (-6) % 4, array2D[0][0][0]);
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      for (int k = 0; k < 4; k++)
      {
        printf("(%d, %d, %d): %d\n", i, j, k, array2D[i][j][k]);
      }
    }
  }
  int a[4] = {1, 2, 3, 4};
  int *p = a;
  p++;
  printf("p[0] = %d\n", p[0]);
}