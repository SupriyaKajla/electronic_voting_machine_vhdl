from tkinter import *
from tkinter import ttk
import os
import subprocess
from subprocess import check_output
import tksheet

#name of the file where application and profile names are to be stored
valueFilePath = "guiValues.txt"

ws = Tk()
ws.title('FRIENDLY LSM GUI')
ws.geometry('800x700')
ws.config(bg='#597678')

proglistPrefix = "const char * proglist[] = {"
proglistSuffix = "//proglist"

ProgList = set()
ProgListMain = []

proglistprofPrefix = "const char * proglistdprfiles[] = {"
proglistprofSuffix = "}; //progsettingslist"

ProgProfList = set()
ProgProfListMain = []

Asettings = []
Wsettings = []
Ssettings = []

AsettingsPrefix = "const char * a_settings[] = {"
WsettingsPrefix = "const char * w_settings[] = {"
SsettingsPrefix = "const char * a_settings[] = {"

Asettingssuffix = "}; //wsettingslist"
Wsettingssuffix = "}; //ssettingslist"
Ssettingssuffix = "}; //asettingslist"


with open('settings.txt') as logf:
    datafile = logf.readlines()
    for line in datafile:
        if '//proglist' in line:
            print(line)
            line = line.strip(proglistPrefix)
            line = line[:-14]
            print(line)
            tmp = line.split(',')

            for i in tmp:
                ProgList.add(i.strip('"').rstrip('"').lstrip('"'))
                ProgListMain.append(i.strip('"').rstrip('"').lstrip('"'))

    for line in datafile:
        if '//progsettingslist' in line:
            print(line)
            line = line.strip(proglistprofPrefix)
            line = line[:-22]
            print(line)
            tmp = line.split(',')

            for i in tmp:
                ProgProfList.add(i.strip('"').rstrip('"').lstrip('"'))
                ProgProfListMain.append(i.strip('"').rstrip('"').lstrip('"'))
                
    for line in datafile:
        if '//asettingslist' in line:
            print(line)
            line = line.strip(AsettingsPrefix)
            line = line[:-19]
            print(line)
            tmp = line.split(',')

            for i in tmp:
                #Asettings.add(i.strip('"').rstrip('"').lstrip('"'))
                Asettings.append(i.strip('"').rstrip('"').lstrip('"'))

    for line in datafile:
        if '//wsettingslist' in line:
            print(line)
            line = line.strip(WsettingsPrefix)
            line = line[:-19]
            print(line)
            tmp = line.split(',')

            for i in tmp:
                #Asettings.add(i.strip('"').rstrip('"').lstrip('"'))
                Wsettings.append(i.strip('"').rstrip('"').lstrip('"'))

    for line in datafile:
        if '//ssettingslist' in line:
            print(line)
            line = line.strip(SsettingsPrefix)
            line = line[:-19]
            print(line)
            tmp = line.split(',')

            for i in tmp:
                #Asettings.add(i.strip('"').rstrip('"').lstrip('"'))
                Ssettings.append(i.strip('"').rstrip('"').lstrip('"'))



ProgMsg = []
i = 0
while (i < len(ProgListMain)):
	ProgMsg.append(ProgListMain[i] + " - Profile : " + ProgProfListMain[i])
	i = i + 1
	
	
var4 = StringVar()
label4 = Label( ws, textvariable=var4, relief=RAISED )
label4.place(x=10, y=80)
var4.set("Current Settings : ")

msgAreaset = Text(ws, height=8)

count = 1
for i in ProgMsg:
	
	msgAreaset.insert(str(count)+'0.1', i+ '\n')
msgAreaset.place(x=10,y=100)
	
            
p = subprocess.Popen("dmesg | grep Friendly > dmsg.txt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

msg_list = []	
##ReadFromDmesg
with open('dmsg.txt') as logf:
    ##log = logf.read()
    datafile = logf.readlines()
    for line in datafile:
    	msg_list.append(line)
    	
var3 = StringVar()
label3 = Label( ws, textvariable=var3, relief=RAISED )
label3.place(x=10, y=480)
var3.set("Friendly LSM Audit Log : ")

msgArea = Text(ws, height=8)

count = 1
for i in msg_list:
	
	msgArea.insert(str(count)+'0.1', i+ '\n')
msgArea.place(x=10,y=500)

#printing and dumping the latest value of application
def appVal(*args, dumpFile = valueFilePath):
    print(f"the profile has changed to '{categoryApp.get()}'")
    appDump = open(dumpFile, 'a')
    appDump.write('App: ' + str({categoryApp.get()}) + '\n')
    appDump.close()

#printing and dumping the latest value of profile
def profileVal(*args, dumpFile = valueFilePath):
    print(f"the profile has changed to '{categoryProfile.get()}'")
    profileDump = open(dumpFile, 'a')
    profileDump.write('Profile: ' + str({categoryProfile.get()}) + '\n')
    profileDump.close()

categoryApp = StringVar()
categoryApp.trace('w', appVal)
categoryProfile = StringVar()
categoryProfile.trace('w', profileVal)

applications = {"Firefox", "Calculator", "Node", "Chrome"}
profiles = {"Audit", "Warn", "Restrict"}
categoryApp.set("Apps")
categoryProfile.set("Profiles")

##Section 1
# Separator object
separator = ttk.Separator(ws, orient='horizontal')
separator.place(relx=0, rely=0.4, relwidth=1, relheight=0.005)
 
separator2 = ttk.Separator(ws, orient='horizontal')
separator2.place(relx=0, rely=0.6, relwidth=1, relheight=0.005)

cmbApps = OptionMenu(ws, categoryApp, *ProgList).place(x=100, y=40)
# positioning widget
#popupMenu.pack(expand=True)
cmbAprofile = OptionMenu(ws, categoryProfile, *profiles).place(x=410, y=40)
#popupMenu2.pack(expand=True)

var = StringVar()
label = Label( ws, textvariable=var, relief=RAISED )
label.place(x=10, y=45)

var.set("App Name : ")

var2 = StringVar()
label2 = Label( ws, textvariable=var2, relief=RAISED )
label2.place(x=295, y=45)

var2.set("Profile Name : ")

var6 = StringVar()
label6 = Label( ws, textvariable=var6, relief=RAISED )
label6.place(x=10, y=10)

var6.set("App Profile Settings : ")

var7 = StringVar()
label7 = Label( ws, textvariable=var7, relief=RAISED )
label7.place(x=10, y=315)

var7.set("Profile Settings : ")


##button save
def SaveProfileForApp():
   if (categoryApp.get() != "Apps"):
   	if (categoryProfile.get() != "Profiles"):
   		print(categoryApp.get())
   		print(categoryProfile.get())
   		replace(categoryApp.get(),categoryProfile.get())

def replace(app,prof):
	pos = ProgListMain.index(app)
	cur = "A"
	if (prof == "Audit"):
		ProgProfListMain[pos] = "A"
	elif (prof == "Warn"):
		ProgProfListMain[pos] = "W"
	else:
		ProgProfListMain[pos] = "S"
		
	print(ProgListMain[pos])
	print(ProgProfListMain[pos])
	
	ProgMsg = []
	msgAreaset.delete('1.0', END)
	i = 0
	while (i < len(ProgListMain)):
		ProgMsg.append(ProgListMain[i] + " - Profile : " + ProgProfListMain[i])
		i = i + 1	
	
	count = 1
	for i in ProgMsg:
	
		msgAreaset.insert(str(count)+'0.1', i+ '\n')

def onCategoryprofChang(*args, dumpFile = valueFilePath):
    if (categoryProfile2.get() == 'Audit'):
    	print("hr 1")
    	if (Asettings[0] == "0"):
    		chkAudit.set(0)
    	if (Asettings[0] == "1"):
    		chkAudit.set(1)
    		
    	if (Asettings[1] == "0"):
    		chkWarn.set(0)
    	if (Asettings[1] == "1"):
    		chkWarn.set(1)
    		
    	if (Asettings[2] == "0"):
    		ckhRestrict.set(0)
    	if (Asettings[2] == "1"):
    		ckhRestrict.set(1)
    		
    elif (categoryProfile2.get() == 'Warn'):
    	print("hr 2")
    	print (Wsettings[0] + Wsettings[1] + Wsettings[2])
    	if (Wsettings[0] == "0"):
    		chkAudit.set(0)
    	if (Wsettings[0] == "1"):
    		chkAudit.set(1)
    		
    	if (Wsettings[1] == "0"):
    		chkWarn.set(0)
    	if (Wsettings[1] == "1"):
    		chkWarn.set(1)
    		
    	if (Wsettings[2] == "0"):
    		ckhRestrict.set(0)
    	if (Wsettings[2] == "1"):
    		ckhRestrict.set(1)
    		
    else:
    	print("hr 3")
    	if (Ssettings[0] == "0"):
    		chkAudit.set(0)
    	if (Ssettings[0] == "1"):
    		chkAudit.set(1)
    		
    	if (Ssettings[1] == "0"):
    		chkWarn.set(0)
    	if (Ssettings[1] == "1"):
    		chkWarn.set(1)
    		
    	if (Ssettings[2] == "0"):
    		ckhRestrict.set(0)
    	if (Ssettings[2] == "1"):
    		ckhRestrict.set(1)
    
def print_selection():
	print("Checked Changed")
	
def SaveProfileSettings():
	if (categoryProfile2.get() == 'Audit'):
		if (chkAudit.get() == 1):
    			Asettings[0] = "1"
		if (chkAudit.get() == 0):
    			Asettings[0] = "0"
			
		if (chkWarn.get() == 1):
    			Asettings[1] = "1"
		if (chkWarn.get() == 0):
    			Asettings[1] = "0"
			
		if (ckhRestrict.get() == 1):
    			Asettings[2] = "1"
		if (ckhRestrict.get() == 0):
    			Asettings[2] = "0"
    			
	elif (categoryProfile2.get() == 'Warn'):
		if (chkAudit.get() == 1):
    			Wsettings[0] = "1"
		if (chkAudit.get() == 0):
    			Wsettings[0] = "0"
			
		if (chkWarn.get() == 1):
    			Wsettings[1] = "1"
		if (chkWarn.get() == 0):
    			Wsettings[1] = "0"
			
		if (ckhRestrict.get() == 1):
    			Wsettings[2] = "1"
		if (ckhRestrict.get() == 0):
    			Wsettings[2] = "0"
    			
	else:
		if (chkAudit.get() == 1):
    			Ssettings[0] = "1"
		if (chkAudit.get() == 0):
    			Ssettings[0] = "0"
			
		if (chkWarn.get() == 1):
    			Ssettings[1] = "1"
		if (chkWarn.get() == 0):
    			Ssettings[1] = "0"
			
		if (ckhRestrict.get() == 1):
    			Ssettings[2] = "1"
		if (ckhRestrict.get() == 0):
    			Ssettings[2] = "0"
    
categoryProfile2 = StringVar()
categoryProfile2.set("Profiles")
categoryProfile2.trace('w', onCategoryprofChang)

ckhRestrict =  IntVar()
chkWarn =  IntVar()
chkAudit =  IntVar()

Checkbutton(ws, text='Audit',variable=chkAudit, onvalue=1, offvalue=0, command=print_selection).place(x=110, y=345)
Checkbutton(ws, text='Warn',variable=chkWarn, onvalue=1, offvalue=0, command=print_selection).place(x=210, y=345)
Checkbutton(ws, text='Restrict',variable=ckhRestrict, onvalue=1, offvalue=0, command=print_selection).place(x=310, y=345)
btnSaveProfile = Button(ws, text ="  Save Profile Settings", command = SaveProfileSettings).place(x=410, y=345)

cmbAprofile2 = OptionMenu(ws, categoryProfile2, *profiles).place(x=10, y=340)		
		
def GenerateSettings():
	print("generating")
	f = open("settings.txt", "w")
	f.write("//Start Hard Data from GUI"+"\n")
	f.write("int count = 5; //count"+"\n")
	f.write(""+"\n")
	f.write('const char * proglist[] = {"node","gnome-calculato","gedit","gnome-screenshot","other"}; //proglist'+"\n")
	f.write("const char * proglistdprfiles[] = {"+'"'+ProgProfListMain[0]+'","'+ProgProfListMain[1]+'","'+ProgProfListMain[2]+'","'+ProgProfListMain[3]+'","'+ProgProfListMain[4]+'"'+'}; //progsettingslist'+"\n")
	f.write(""+"\n")
	f.write("const char * w_settings[] = {"+'"'+Wsettings[0]+'","'+Wsettings[1]+'","'+Wsettings[2]+'"'+'}; //wsettingslist'+"\n")
	f.write("const char * s_settings[] = {"+'"'+Ssettings[0]+'","'+Ssettings[1]+'","'+Ssettings[2]+'"'+'}; //ssettingslist'+"\n")
	f.write("const char * a_settings[] = {"+'"'+Asettings[0]+'","'+Asettings[1]+'","'+Asettings[2]+'"'+'}; //asettingslist'+"\n")
	f.write(""+"\n")
	f.write("int s_allow_userscount = 2;"+"\n")
	f.write('const char * s_allow_users[] = { "1", "0" };'+"\n")
	f.write(""+"\n")
	f.write("int s_rest_userscount = 1;"+"\n")
	f.write('const char * s_rest_users[] = { "1000"};'+"\n")
	f.write(""+"\n")
	f.write("int w_allow_userscount = 2;"+"\n")
	f.write('const char * w_allow_users[] = { "1", "0" };'+"\n")
	f.write(""+"\n")
	f.write("int w_restric_userscount = 1;"+"\n")
	f.write('const char * w_restric_users[] = { "1000"};'+"\n")
	f.write(""+"\n")
	f.write(""+"\n")
	f.write(""+"\n")
	f.write(""+"\n")
	f.write("//settings index 0 - audit, 1- give warning , 2- restrict-access,"+"\n")
	f.write(""+"\n")
	f.write("//A -- Audit --  only Audit"+"\n")
	f.write("//W -- Warning -- only audit and log complain"+"\n")
	f.write("//S -- Strict -- Stop execution, audit"+"\n")
	f.write(""+"\n")
	f.write("//End Hard Data from GUI"+"\n")
	f.write(""+"\n")
	f.close()
	
	data1 = data2 = data3 = ""
	
	with open('header.txt') as fp:
		data1 = fp.read()
		
	with open('settings.txt') as fp:
		data2 = fp.read()

	with open('code.txt') as fp:
    		data3 = fp.read()
  

	data1 += "\n"
	data1 += data2
	data1 += "\n"
	data1 += data3
  
	with open ('flsm_main.c', 'w') as fp:
    		fp.write(data1)
    	
    	


btnSaveProfile = Button(ws, text ="  Save Profile  ", command = SaveProfileForApp).place(x=520, y=40)

btnGenerateSettings = Button(ws, text ="  Generate Settings  ", command = GenerateSettings).place(x=420, y=650)

# infinite loop 
ws.mainloop()

