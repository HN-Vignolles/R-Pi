int int_nr = 0;

void setup(){
  pinMode(3, INPUT);
  pinMode(4, OUTPUT);
  pinMode(1, OUTPUT);
  digitalWrite(4, HIGH);
  PCMSK |= bit(PCINT3); // Pin Change Mask Register: PB3, pin 2@dip8
  GIFR |= bit(PCIF); // General Interrupt Flag Register: clear outstanding interrupts
  GIMSK |= bit(PCIE);  // General Interrupt Mask Register: enable pin change interrupts
}

void loop(){
}

ISR(PCINT0_vect){
  int_nr++;
  if(int_nr < 500){
    if(PINB & (1 << PB3)){
      PORTB |= (1 << PB4);
      for(int i = 0; i < 50; i++) __asm__ __volatile__ ("nop\n\t");
      for(int i = 0; i < int_nr; i++) __asm__ __volatile__ ("nop\n\t");
      PORTB &= ~(1 << PB4);
      for(int i = 0; i < 50; i++) __asm__ __volatile__ ("nop\n\t");
    }
  }
  if(int_nr >= 500 && int_nr < 1000){
    if((PINB & (1 << PB3)) == 0){
      PORTB |= (1 << PB1);
      for(int i = 0; i < 50; i++) __asm__ __volatile__ ("nop\n\t");
      for(int i = 0; i < (int_nr - 500); i++) __asm__ __volatile__ ("nop\n\t");
      PORTB &= ~(1 << PB1);
      for(int i = 0; i < 50; i++) __asm__ __volatile__ ("nop\n\t");
    }
  }
  if(int_nr >= 1000 && int_nr < 1500){
    PORTB &= ~(1 << PB4);
    PORTB &= ~(1 << PB1);
  }
  if(int_nr >= 1500){
    int_nr = 0;
  }
}