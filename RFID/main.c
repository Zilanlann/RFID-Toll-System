#include "variable.h"
#include "delay.h"
#include "UART.h"
#include "IC_w_r.h"

#define uint unsigned int
#define uchar unsigned char

// 定义控制灯的端口
#define LED1 P1_0
#define LED2 P1_1

uchar Recdata[3] = "000";
uchar RXTXflag = 1;
uchar temp;
uint datanumber = 0;
uint stringlen;

void InitIO()
{
    CLKCONCMD &= ~0x40; // 设置系统时钟源为32MHZ晶振
    while (CLKCONSTA & 0x40)
        ;               // 等待晶振稳定为32M
    CLKCONCMD &= ~0x47; // 设置系统主时钟频率为32MHZ
    UartInitial();

    // IC_SDA P2_0
    P2DIR |= 1 << 0;
    P2INP |= 1 << 0;
    P2SEL &= ~(1 << 0);

    // IC_SCK  P0_7
    P0DIR |= 1 << 7;
    P0INP |= 1 << 7;
    P0SEL &= ~(1 << 7);

    // IC_MOSI P0_6
    P0DIR |= 1 << 6;
    P0INP |= 1 << 6;
    P0SEL &= ~(1 << 6);

    // IC_MISO P0_5
    P0DIR |= 1 << 5;
    P0INP |= 1 << 5;
    P0SEL &= ~(1 << 5);

    // IC_RST P0_4
    P0DIR &= ~(1 << 4);
    P0INP &= ~(1 << 4);
    P0SEL &= ~(1 << 4);

    IC_SCK = 1;
    IC_SDA = 1;
}

/*****************************************
初始化LED IO口
*****************************************/
void Init_LED_IO(void)
{
    P1DIR = 0x03; // P10 P11 为输出
    LED1 = 1;
    LED2 = 1; // 灭LED
}

void IC_test()
{
  uchar ucTagType[4];
  uchar find=0xaa;
  uchar ret;
  
  while(1)
  {
    //16进制转ASC码
    //UartSend_String("1",1); 
    char i;  
    char Card_Id[8]; //存放32位卡号
    uchar asc_16[16]={'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
  
    ret = PcdRequest(0x52,ucTagType);//寻卡
    if(ret != 0x26)
      ret = PcdRequest(0x52,ucTagType);
    if(ret != 0x26)
      find = 0xaa;
    if((ret == 0x26)&&(find == 0xaa))
    {
      if(PcdAnticoll(ucTagType) == 0x26);//防冲撞
      {
        
        //16进制转ASC码
        for(i=0;i<4;i++)
        {
          Card_Id[i*2]=asc_16[ucTagType[i]/16];
          Card_Id[i*2+1]=asc_16[ucTagType[i]%16];        
        }  
        UartSend_String(Card_Id,8); 
        find = 0x00;
        break;
      }
    }
  }
}

void main()
{
    uchar i;
    InitIO();
    Init_LED_IO();
    PcdReset();
    M500PcdConfigISOType('A'); // 设置工作方式
    while (1)
    {
        // IC_test();              //检测IC卡
        if (RXTXflag == 1) // 接收状态
        {
            if (temp != 0) /// datanumber = 0
            {
                if ((temp != '#') && (datanumber < 30))
                { // ’＃‘被定义为结束字符
                    // 最多能接收3个字符
                    Recdata[datanumber++] = temp;
                }
                else
                {
                    RXTXflag = 3; // 进入改变小灯的程序
                }
                if (datanumber == 3)
                    RXTXflag = 3;
                temp = 0;
            }
        }
        if (RXTXflag == 3)
        {
            // 控制LED1灯的指令
            if (Recdata[0] == 'R')
            {

                if (Recdata[1] == '0')
                {
                    LED1 = 1; // R0# 关D1
                }
                else if (Recdata[1] == '1')
                {
                    LED1 = 0; // R1# 开D1
                }
            }
            else if (Recdata[0] == 'G')
            {
                if (Recdata[1] == '0')
                    LED2 = 1; // G0# 关D2
                else if (Recdata[1] == '1')
                    LED2 = 0; // G1# 开D2
            }
            else if (Recdata[0] == 'A')
            {
                if (Recdata[1] == '0')
                {
                    LED1 = 1;
                    LED2 = 1; // A0# 关所有LED
                }
                else if (Recdata[1] == '1')
                {
                    LED1 = 0;
                    LED2 = 0; // A1# 开所有LED
                }
            }
            // 控制RFID的指令
            else if (Recdata[0] == 'I')
            {

                if (Recdata[1] == 'C')
                {
                    IC_test();
                }
            }
            RXTXflag = 1;
            memset(Recdata, 0, sizeof(Recdata)); // 清除刚才的命令
            datanumber = 0;       // 指针归0=
        }
    }
}

/****************************************************************
串口接收一个字符:一旦有数据从串口传至CC2530,则进入中断，将接收到的数据赋值给变量temp.
****************************************************************/
#pragma vector = URX0_VECTOR
__interrupt void UART0_ISR(void)
{
    URX0IF = 0; // 清中断标志
    temp = U0DBUF;
}