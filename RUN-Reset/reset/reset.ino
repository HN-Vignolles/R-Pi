int int_nr = 0;

void setup(){
  pinMode(3, INPUT);
  pinMode(4, OUTPUT);
  pinMode(1, OUTPUT);
  digitalWrite(4, LOW);
  PCMSK |= bit(PCINT3); // Pin Change Mask Register: PB3, pin 2@dip8
  GIFR |= bit(PCIF); // General Interrupt Flag Register: clear outstanding interrupts
  GIMSK |= bit(PCIE);  // General Interrupt Mask Register: enable pin change interrupts
}

void loop(){
}

ISR(PCINT0_vect){
  GIMSK &= ~bit(PCIE);
  if(PINB & (1 << PB3)){
    int_nr++;
    for(int i = 0; i < int_nr; i++) __asm__ __volatile__ ("nop\n\t");
    PORTB |= (1 << PB4);
    for(int i = 0; i < 400; i++) __asm__ __volatile__ ("nop\n\t");
    PORTB &= ~(1 << PB4);
    if(int_nr >= 1800){
      int_nr = 0;
    }
  }
  GIMSK |= bit(PCIE);
}