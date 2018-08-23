# Mapping
- This is an example of the mapping from reading a Sunspec inverter (type 103 or 101) using this plugin

CSV Name                    Ardexa Name             Type        Units
-----------------------------------------------------------------------
Datetime                    Datetime                Date
AC Current                  AC Current              Decimal     A
AC Current 1                AC Current 1            Decimal     A
AC Current 2                AC Current 2            Decimal     A
AC Current 3                AC Current 3            Decimal     A
AC Voltage 12               AC Voltage 12           Decimal     V
AC Voltage 23               AC Voltage 23           Decimal     V
AC Voltage 31               AC Voltage 31           Decimal     V
AC Voltage 1                AC Voltage 1            Decimal     V
AC Voltage 2                AC Voltage 2            Decimal     V
AC Voltage 3                AC Voltage 3            Decimal     V
AC Power                    AC Power                Decimal     W
Grid Freq                   Grid Freq               Decimal     Hz
Cos Phi                     Cos Phi                 keyword
Total Energy                Total Energy            Decimal     Wh
DC Current 1                DC Current 1            Decimal     A
DC Voltage 1                DC Voltage 1            Decimal     V
DC Power                    DC Power                Decimal     W
Cabinet Temp                Cabinet Temp            Decimal     °C
Temperature                 Temperature             Decimal     °C
Transformer Temp            Transformer Temp        Decimal     °C
Other Temp                  Other Temp              Decimal     °C
Operating State             Status                  keyword
Vendor Operating State      Vendor Status           keyword
Event                       Event                   keyword




- This is an example of the mapping from reading a Sunspec storage device (type 124) using this plugin

CSV Name                    Ardexa Name             Type        Units
-----------------------------------------------------------------------
Datetime                    Datetime                Date
SetPt Max Charge            SetPt Max Charge        Decimal     W
Storage Mode                Storage Mode            keyword
State of Charge             State of Charge         Decimal     %
Battery Voltage             Battery Voltage         Decimal     V
Charge Status               Charge Status           keyword
Discharge Rate              Discharge Rate          Decimal     %
Charge Rate                 Charge Rate             Decimal     %
Available Energy            Available Energy        Decimal     AH



- A Device of Type 160 (Which is a strings module, or MPPT Inverter Extension), will have a repeating block.
- So parts of the following may repeat based on how many strings module are part of the inverter
- Mostly, there may be 2, so we have included 2 as part of this mapping
- In Ardexa, usually this data goes into the `strings` table

CSV Name                    Ardexa Name             Type        Units
-----------------------------------------------------------------------
Datetime                    Datetime                Date
Global Events               Global Events           keyword
Number of Modules           Modules                 Integer
Module ID                   Module 1                Integer
DC Current 1                DC Current 1            Decimal     A
DC Voltage 1                DC Voltage 1            Decimal     V
DC Power 1                  DC Power 1              Decimal     W
Temperature                 Temperature 1           Decimal     °C
Operating State             Status 1                keyword
Module Events               Module Events 1         keyword
Module ID                   Module 2                Integer
DC Current 1                DC Current 2            Decimal     A
DC Voltage 1                DC Voltage 2            Decimal     V
DC Power 1                  DC Power 2              Decimal     W
Temperature                 Temperature 2           Decimal     °C
Operating State             Status 2                keyword
Module Events               Module Events 2         keyword


