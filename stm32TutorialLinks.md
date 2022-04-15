





# printf重定向：
```c++
#ifdef __GNUC__
/* With GCC, small printf (option LD Linker->Libraries->Small printf
   set to 'Yes') calls __io_putchar() */
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif /* __GNUC__ */

/**
  * @brief  Retargets the C library printf function to the USART.
  * @param  None
  * @retval None
  */
PUTCHAR_PROTOTYPE
{
    /* Place your implementation of fputc here */
    /* e.g. write a character to the USART3 and Loop until the end of transmission */
    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);

    return ch;
}
```

# 解决浮点问题：

在CMAKELIST.txt中添加在    此处最后加上-u _printf_float

https://blog.csdn.net/qq_43715171/article/details/117776784

# 测试代码：
```C++
printf("Characters: %c %c\n", 'a', 65);
printf("Decimals: %d %ld\n", 1977, 650000L);
printf("Preceding with blanks: %10d\n", 1977);
printf("Preceding with zeros: %010d\n", 1977);
printf("Some different radices: %d %x %o %#x %#o\n", 100, 100, 100, 100, 100);
printf("floats: %4.2f %+.0e %E\n", 3.1416, 3.1416, 3.1416);
printf("Width trick: %*d\n", 5, 10);
printf("%s\n", "A string");
```
https://forum.digikey.com/t/easily-use-printf-on-stm32/20157
