# Edison

With the advent of the Internet of Things concept, there is an increasing interest regarding 
to connectivity among different electronic devices, as well as to data analysis of
interchanged information among them, taking advantage of the increased processing capacity
and cheaper embedded system devices. Cars are included into this list of connectable devices, 
whose internal networks generates tremendous amounts of data every moment, but that are 
directed only to electronic and mechanic control, or even to comfort and safety features. 
The most used protocol for internal communication in vehicles is called CAN, which is mainly used
for automotive and industrial applications. For this reason, a system has been developed to 
analyze a CAN network aiming at identifying and alerting about the driver’s behavior, which 
may harm the vehicle mechanically, as well as classifying driver’s driving using an algorithm of 
artificial intelligence. This information is recorded using an Arduino board connected to the 
vehicle and processed and sent through an Intel Edison board, via Internet, to a web server, which 
provides formatted data to the user. The experiment was realized into a Renault Sandero (2015) 
accessing information such as current speed, rotations per minute and accelerator pedal position, 
which were processed aiming at delivering statistics about breaking and gear changing conducted by the driver.
