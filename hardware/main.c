#include "variable.h"
#include "delay.h"
#include "UART.h"
#include "IC_w_r.h"

#define uint unsigned int
#define uchar unsigned char

// ������ƵƵĶ˿�
#define LED1 P1_0
#define LED2 P1_1

uchar Recdata[3] = "000";
uchar RXTXflag = 1;
uchar temp;
uint datanumber = 0;
uint stringlen;

void InitIO()
{
    CLKCONCMD &= ~0x40; // ����ϵͳʱ��ԴΪ32MHZ����
    while (CLKCONSTA & 0x40)
        ;               // �ȴ������ȶ�Ϊ32M
    CLKCONCMD &= ~0x47; // ����ϵͳ��ʱ��Ƶ��Ϊ32MHZ
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
��ʼ��LED IO��
*****************************************/
void Init_LED_IO(void)
{
    P1DIR = 0x03; // P10 P11 Ϊ���
    LED1 = 1;
    LED2 = 1; // ��LED
}

void IC_test()
{
  uchar ucTagType[4];
  uchar find=0xaa;
  uchar ret;
  
  while(1)
  {
    //16����תASC��
    //UartSend_String("1",1); 
    char i;  
    char Card_Id[8]; //���32λ����
    uchar asc_16[16]={'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
  
    ret = PcdRequest(0x52,ucTagType);//Ѱ��
    if(ret != 0x26)
      ret = PcdRequest(0x52,ucTagType);
    if(ret != 0x26)
      find = 0xaa;
    if((ret == 0x26)&&(find == 0xaa))
    {
      if(PcdAnticoll(ucTagType) == 0x26);//����ײ
      {
        
        //16����תASC��
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
    M500PcdConfigISOType('A'); // ���ù�����ʽ
    while (1)
    {
        // IC_test();              //���IC��
        if (RXTXflag == 1) // ����״̬
        {
            if (temp != 0) /// datanumber = 0
            {
                if ((temp != '#') && (datanumber < 30))
                { // ������������Ϊ�����ַ�
                    // ����ܽ���3���ַ�
                    Recdata[datanumber++] = temp;
                }
                else
                {
                    RXTXflag = 3; // ����ı�С�Ƶĳ���
                }
                if (datanumber == 3)
                    RXTXflag = 3;
                temp = 0;
            }
        }
        if (RXTXflag == 3)
        {
            // ����LED1�Ƶ�ָ��
            if (Recdata[0] == 'R')
            {

                if (Recdata[1] == '0')
                {
                    LED1 = 1; // R0# ��D1
                }
                else if (Recdata[1] == '1')
                {
                    LED1 = 0; // R1# ��D1
                }
            }
            else if (Recdata[0] == 'G')
            {
                if (Recdata[1] == '0')
                    LED2 = 1; // G0# ��D2
                else if (Recdata[1] == '1')
                    LED2 = 0; // G1# ��D2
            }
            else if (Recdata[0] == 'A')
            {
                if (Recdata[1] == '0')
                {
                    LED1 = 1;
                    LED2 = 1; // A0# ������LED
                }
                else if (Recdata[1] == '1')
                {
                    LED1 = 0;
                    LED2 = 0; // A1# ������LED
                }
            }
            // ����RFID��ָ��
            else if (Recdata[0] == 'I')
            {

                if (Recdata[1] == 'C')
                {
                    IC_test();
                }
            }
            RXTXflag = 1;
            memset(Recdata, 0, sizeof(Recdata)); // ����ղŵ�����
            datanumber = 0;       // ָ���0=
        }
    }
}

/****************************************************************
���ڽ���һ���ַ�:һ�������ݴӴ��ڴ���CC2530,������жϣ������յ������ݸ�ֵ������temp.
****************************************************************/
#pragma vector = URX0_VECTOR
__interrupt void UART0_ISR(void)
{
    URX0IF = 0; // ���жϱ�־
    temp = U0DBUF;
}