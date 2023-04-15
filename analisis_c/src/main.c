#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"
#include "entrada.h"

#define N   1000
#define FS  100

int main (void) 
{
   uint16_t i = 0;
   uint16_t dacValue = 0;
   int16_t y [N];

   boardConfig ( );
   uartConfig (UART_USB ,460800 );
   adcConfig (ADC_ENABLE);
   dacConfig (DAC_ENABLE);
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) 
   {
      for (int i=0;i<N;i++) 
      {
         if (h[i] > 0)
            dacValue = 1023;
         else 
            dacValue = 0;
         
         dacWrite( DAC, dacValue );
         
         // Need at least 2.5 us to uptate DAC.
         delayInaccurateUs(5); 
         
         y[i] = (int16_t) (((float)adcRead(CH1)/1023.0)*100); // multiplicamos por 100 para no perder la parte decimal
         
         uartWriteByteArray ( UART_USB ,(uint8_t* )(&y[i]),sizeof(int16_t));
         
         gpioToggle ( LED1 );// este led blinkea a fs/2
         while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/FS) // el clk de la CIAA es 204000000
         ;
         
      }
      
      gpioToggle ( LED2 );       
      
   }
}
