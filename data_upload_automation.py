# 1. Skicka in alla variabler som behöver för data_upload
# 2. Kör data_uploads scriptet i första foldern (0)
    # 3. När 0 är klar, kör scriptet igen i nästa folder. 
    # 14. repetera scriptet tills det är klart med alla folders.

# Blir förmodligen en ansible-playbook. Behövs egentligen bara 2 saker för att få det att funka: 
# 1. Ett sätt att veta att scriptet är klart med en folder (Ansible bör att någon inbyggt för att märka när en funktion avslutas)
# 2. Error handling - ibland avslutas scriptet innan det är klart. Om det händer ska loopen inte fortsätta utan 
# köra mot samma folder igen tills den faktiskt är klar.

# Så vi måste kunna få 2 olika output - error (scriptet avslutades av någon anledning), och done (scriptet är klart i foldern)