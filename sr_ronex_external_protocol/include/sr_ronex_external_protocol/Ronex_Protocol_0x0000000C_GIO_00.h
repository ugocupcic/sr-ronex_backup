//! EtherCAT protocol for RoNeX General I/O stacker, 01.
//! Works on Node revision 01


#include "typedefs_shadow.h"

#define RONEX_COMMAND_0000000C_MASTER_CLOCK_SPEED_HZ        64000000
#define RONEX_COMMAND_0000000C_ADC_SAMPLE_RATE_HZ               1000


// For RC Servos, set Clock Speed = 2MHz, and PWM period to 39999. This gives 20ms period.
typedef enum
{
    RONEX_COMMAND_0000000C_CLOCK_SPEED_64_MHZ   =    1,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_32_MHZ   =    2,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_16_MHZ   =    4,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_08_MHZ   =    8,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_04_MHZ   =   16,,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_02_MHZ   =   32,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_01_MHZ   =   64,

    RONEX_COMMAND_0000000C_CLOCK_SPEED_500_KHZ  =  128,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_250_KHZ  =  256,
    RONEX_COMMAND_0000000C_CLOCK_SPEED_125_KHZ  =  512,
}RONEX_COMMAND_0000000C_CLOCK_SPEED;

typedef enum
{
    RONEX_COMMAND_0000000C_ADC_INPUT_GAIN_1     = 1,
    RONEX_COMMAND_0000000C_ADC_INPUT_GAIN_2     = 2,
    RONEX_COMMAND_0000000C_ADC_INPUT_GAIN_4     = 4,
}RONEX_COMMAND_0000000C_ADC_INPUT_GAIN;


typedef struct
{
    int16u  pwm_period;
    int16u  pwm_on_time_0;
    int16u  pwm_on_time_1;
}RONEX_COMMAND_0000000C_PWM;




//! Status Structure
typedef struct
{
    int16u  analogue_in[12];
    int16u  digital_in;                                             //!< Bit n: Status of digital pin n.
}RONEX_STATUS_0000000C;


//! Command structure
typedef struct
{
    RONEX_COMMAND_0000000C_PWM              pwm_module[6];
    int32u                                  digital_out;            //!< Bit 0: Direction of digital pin 0, 0=Output, 1=Input
                                                                    //!< Bit 1: Drive     of digital pin 0, 0=Low,    1=High
                                                                    //!< Bit 2: Direction of digital pin 1, 0=Output, 1=Input
                                                                    //!< Bit 3: Drive     of digital pin 1, 0=Low,    1=High
                                                                    //!< etc ..
    RONEX_COMMAND_0000000C_CLOCK_SPEED      pwm_clock_speed;
    RONEX_COMMAND_0000000C_ADC_INPUT_GAIN   adc_input_gain;
}RONEX_COMMAND_0000000C;

