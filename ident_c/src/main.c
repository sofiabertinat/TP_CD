#include <stdlib.h>
#include <math.h>
#include "sapi.h"
#include "arm_math.h"
#include "ident.h"
#include "entrada.h"

// Noise signal limits
#define DAC_REFERENCE_VALUE_HIGH   666  // 1023 = 3.3V, 666 = 2.15V
#define DAC_REFERENCE_VALUE_LOW    356  // 1023 = 3.3V, 356 = 1.15V

// adcRead() returns 10 bits integer sample (uint16_t)
// sampleInVolts = (3.3 / 1023.0) * adcSample
#define getVoltsSampleFrom(adc0Channel) 3.3*(float)adcRead((adc0Channel))/1023.0

#define N 200

arm_matrix_instance_f32 Y;
arm_matrix_instance_f32 T;      // Theta -> M_SIZE x 1
arm_matrix_instance_f32 F;      // Phi -> M_SIZE x M_VALUES
arm_matrix_instance_f32 FT;     // Phi' -> M_VALUES x M_SIZE

arm_matrix_instance_f32 aux0;   // aux0 = Phi' Phi -> M_SIZE x M_SIZE
arm_matrix_instance_f32 aux1;   // aux1 = aux0^(-1) -> M_SIZE x M_SIZE
arm_matrix_instance_f32 aux2;   // aux2 = Phi' Y -> M_SIZE x 1
   
t_ILSdata tILS;

void receiveData (float* buffer);
void m_console_print (float* buffer);

int main (void)
{   
   float buffer[2];
   delay_t t_ms;
   
   boardConfig();
   adcInit( ADC_ENABLE );
   dacInit( DAC_ENABLE );
   uartConfig (UART_USB ,460800 );

	// Inicialización de matrices
    /**
    * @brief  Floating-point matrix initialization.
    * @param[in,out] S         points to an instance of the floating-point 
    *                          matrix structure.
    * @param[in]     nRows     number of rows in the matrix.
    * @param[in]     nColumns  number of columns in the matrix.
    * @param[in]     pData     points to the matrix data array.
    */
	arm_mat_init_f32(&Y, N, 1, tILS.buffer_Y);
	arm_mat_init_f32(&T, M_SIZE, 1, tILS.buffer_T);
	arm_mat_init_f32(&F, N, M_SIZE, tILS.buffer_F);
	arm_mat_init_f32(&FT, M_SIZE, N, tILS.buffer_FT);
	arm_mat_init_f32(&aux0, M_SIZE, M_SIZE, tILS.buffer_aux0);
	arm_mat_init_f32(&aux1, M_SIZE, M_SIZE, tILS.buffer_aux1);
	arm_mat_init_f32(&aux2, M_SIZE, 1, tILS.buffer_aux2);

	// Valores iniciales
	tILS.buffer_Y[1] = 0;
	tILS.buffer_Y[0] = 0;
	tILS.buffer_U[1] = 0;
	tILS.buffer_U[0] = 0;
   
   // Inicializo temporizacion   
   delayInit( &t_ms, 25 );
    
   while(TRUE)
   {
         	
      gpioToggle ( LED3 );
      
      // Ejecuto el Identificador
      receiveData(buffer);
      tILS.buffer_U[tILS.i] = buffer[0];
      tILS.buffer_Y[tILS.i] = buffer[1];

      tILS.buffer_F[(tILS.i*5)+0] = tILS.buffer_Y[tILS.i-1];
      tILS.buffer_F[(tILS.i*5)+1] = tILS.buffer_Y[tILS.i-2];
      tILS.buffer_F[(tILS.i*5)+2] = tILS.buffer_U[tILS.i];
      tILS.buffer_F[(tILS.i*5)+3] = tILS.buffer_U[tILS.i-1];
      tILS.buffer_F[(tILS.i*5)+4] = tILS.buffer_U[tILS.i-2];

      if (tILS.i == (N - 1))
      {
         // Cálculo de matrices traspuestas
         arm_mat_trans_f32(&F, &FT);

          // Cálculo de Theta
         arm_mat_mult_f32(&FT, &F, &aux0);
         arm_mat_inverse_f32(&aux0, &aux1);
         arm_mat_mult_f32(&FT, &Y, &aux2);
         arm_mat_mult_f32(&aux1, &aux2, &T);
         tILS.buffer_Y[1] = tILS.buffer_Y[tILS.i];
         tILS.buffer_Y[0] = tILS.buffer_Y[tILS.i-1];
         tILS.buffer_U[1] = tILS.buffer_U[tILS.i];
         tILS.buffer_U[0] = tILS.buffer_U[tILS.i-1];
         tILS.i = 2;
         gpioToggle ( LED2 );
         // Imprimo los parámetros calculados
         m_console_print(tILS.buffer_T);
      }
      else 
      {
         tILS.i++;
      }

		while(!delayRead(&t_ms)) 
         ;
       
   }

    // YOU NEVER REACH HERE
    return 0;
}


// Generación del DAC y captura del ADC
void receiveData (float* buffer)
{
   float Y, U;
   static uint16_t i = 0;
   uint16_t dacValue = 0;
   int16_t y_i = 0;
   int16_t adc = 0;

   if (h[i] > 0)
      dacValue = 1023;
   else 
      dacValue = DAC_REFERENCE_VALUE_LOW;
   
   i++;
   if (i == N)
      i = 0;

   dacWrite( DAC, dacValue );   
    
   // Need at least 2.5 us to uptate DAC.
   delayInaccurateUs(5); 

   // dacSample = (1023.0 / 3.3) * sampleInVolts
   // 1023.0 / 3.3 = 310.0
   U = (float) dacValue * 3.3 / 1023.0;
   adc = adcRead(CH1);
	Y = (float) 3.3*(float)adc/1023.0;
   
   y_i = (int16_t) (((float)adc/1023.0)*100); // multiplicamos por 100 para no perder la parte decimal
   uartWriteByteArray ( UART_USB ,(uint8_t* )(&y_i),sizeof(int16_t));
   gpioToggle ( LED1 );

	buffer[0] = U;
	buffer[1] = Y;
}

// Función para imprimir los parámetros la planta (2do orden)
void m_console_print (float* buffer)
{
	uint32_t i;
	int32_t integer, fraction;
   uint16_t separador = 0xFFFF;

	// Imprimo los parámetros calculados
   uartWriteByteArray ( UART_USB ,(uint8_t* )(&separador),sizeof(uint16_t));
	for (i = 0; i<5; i++)
	{
		// Casteo de float a int
		integer = (int)buffer[i];
		fraction = (int)(((buffer[i] - (float)integer)) * 1000);
      if (fraction<0)
      {
         fraction = (-1)*fraction;
         if (integer==0)	
         {
            integer = -integer;
         }
      }
      uartWriteByteArray ( UART_USB ,(uint8_t* )(&integer),sizeof(int32_t));
      uartWriteByteArray ( UART_USB ,(uint8_t* )(&fraction),sizeof(int32_t));
	}
   uartWriteByteArray ( UART_USB ,(uint8_t* )(&separador),sizeof(uint16_t));   
}