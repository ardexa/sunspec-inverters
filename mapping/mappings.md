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
