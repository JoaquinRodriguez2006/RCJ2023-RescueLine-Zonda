# Welcome to Team Zonda's Repo!
Hi there! We are Joaquín Rodríguez and Joaquín Argañaraz, from team Zonda IITA Salta, and we are excited to share our project with you! We are taking part in RCJ2023-RescueLine, and decided to create a robot that would push the limits by improving our Lego Spike Prime robot as much as possible. To do this, we developed a communication protocol between the Lego Spike and an Arduino Nano, which controls four Time-of-Flight sensors used to detect obstacles and walls, as well as some servos that operate the claw we use to pick the victims up! For further details, check out our Team Description Paper down below:

TDP Zonda: [tdp_zonda.pdf](https://github.com/JoaquinRodriguez2006/RCJ2023-RescueLine-Zonda/files/11843032/tdp_zonda.pdf)

or, to see the whole development process, feel free to look for anything you might need in our Engineering Journal!

Engineering Journal Zonda: [ZondaTeam.EngineeringJournal.pdf](https://github.com/JoaquinRodriguez2006/RCJ2023-RescueLine-Zonda/files/11843184/ZondaTeam.EngineeringJournal.pdf)

From codes to custom boards, everything in this project is open source and we hope you can feel inspired by it and contribute or replicate it and improve it on your own!! We would love to see this project and the innovations it features implemented in your robots!! Keep in mind, however, that this repo is under an MIT License, which gives you access to everything, yet asks you to give credits to the creators.

## Components
In order to make this possible, we are using electronic components, 3D-designed pieces and a Lego Spike robotics kit.

### Electronic Components
- Arduino Nano
- 4 Time-of-Flight sensors
- Standard Servo
- Mini Digital Servo
- Custom board for Arduino Nano
- 2 custom boards for Time-of-Flight sensors (can hold up to 3 of them each, though we are only 2 on each side)

### 3D Pieces
- Standard Servo Support
- MiniServo Support
- Claw (Left part & Right part)
- Adaptor Lego stick - servo
- Battery mount
- Claw Gears (Left & Right)

(You can check the .stl files here: ```3D Designs``` )

### Lego Spike Prime
- Lego Spike Prime educational robotics kit

## Codes
As we are using two different boards, two different codes are needed. The Lego Spike is coded in Python, while the Arduino uses C++. If you want to see the explanation of each code, function by funtion, feel free to check it out here: ```Documentation/Zonda IITA Salta. Codes/explanation.txt```
### Lego Spike Code
Uses Python and controls color sensors, motors and sends instructions to the Arduino, specifying what to do.
### Arduino Nano Code
Uses C++ and controls Time-of-Flight sensors and the servos operating the claw.

## PID Controller

## Communication Protocol
