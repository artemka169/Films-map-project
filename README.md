# Films-map-project
UCU CS lab 1.2, 1st year

This program analizes films database with adresses, and creates a folium map with closest films to the coordinates.
![image](https://user-images.githubusercontent.com/93625455/153248780-4020455c-238c-4eca-8f1f-a7c0f095db54.png)

Input from argparse : year, latitude, longitude.

To analise database, you shold change direction of file in the first line of main body of program.

There is a 30.000 lines limit in database, because more info causes browser crash when you try to open the map.
![image](https://user-images.githubusercontent.com/93625455/153249476-667b4187-78a9-4fda-bec7-0758ec008b2b.png)
This map consists of 25.088 labels, but browser can't open it properly :( 

Program uses geopy, argparse, haversine, and folium libraries.
