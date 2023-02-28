import xml.etree.cElementTree as ET

# File for the potting_coating module
bgaqf=["'SMT_QFN'","'SMT_CHIP_MELF'","'SMT_BGA'"]
global outputlist
outputlist=[]
msglist =[]
errlist=[]

WL_board=True
D_and_M_board=True
gull_wing="yes"
#mainlySMT="yes"
hoodwithpropersealing="no"
global dict1,dict2
dict1={}
dict2={}


def read_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for i in root[4][1][-1]:#.findall("Component"):
        if i.tag=="{http://webstds.ipc.org/2581}Component":
            #print(i.attrib["refDes"])
            #try:
            if i.attrib["layerRef"]=="TOP" and i.attrib["part"]!="":
                # print("refdes is   ",i.attrib["refDes"],"      part number is    ",i.attrib["part"])
                dict1[i.attrib["refDes"]]=i.attrib["part"].split(",")[0].split("-")[1]
                
            if i.attrib["layerRef"]=="BOTTOM" and i.attrib["part"]!="":
                # print("refdes is   ",i.attrib["refDes"],"      part number is    ",i.attrib["part"])
                dict2[i.attrib["refDes"]]=i.attrib["part"].split(",")[0].split("-")[1]
    
    return dict1,dict2

# def read_csv(csv_file):
#     headr=["pn","loc","side"]
#     csv=pd.read_csv(csv_file,names=headr)
#     tdf=csv[csv["side"]=="top"]
#     bdf=csv[csv["side"]=="bottom"]
    
#     tdf=tdf.applymap(str)
#     bdf=bdf.applymap(str)
    
#     dict1=dict(zip(tdf["loc"], tdf["pn"]))
#     dict2=dict(zip(bdf["loc"], bdf["pn"]))

#     return dict1,dict2

def smt_(pn):
    a=findkeyword(pn)
    if "SMT" in a["DFA_DEV_CLASS"]:
        return 1
    else:
        return 0
    
def mainlysmtfunc(part_list,ptf_file_content):
    smtcount=0
    ## file=open('part_table.ptf',"r")
    ## data=file.readlines()
    
    data=ptf_file_content
    
    # print(type(data))
    if data == None:
        print("ptf file not found")
        print("Please check the path of ptf file")
    #count=0
    linerecord=[]
    
    for x in part_list.keys():
        # print(type(x))
        for i in data:
            i = i.decode('utf-8','ascii')
            #print(i)
            # print("x and i are: ",x," ",i)
            if x in i and "SMT" in i:
                smtcount=smtcount+1
                break
    print("smtcount is : ",smtcount)
    if smtcount > len(part_list.keys())/2:
        outputlist.append("\n mainly smt \n")
        return 1
    else:
        outputlist.append("\n not mainly smt \n")
        return 0

# Create a Function which takes input from option available and returns the value
def menu_select(option):
    ## menu = input("Please select the board type: ")
    menu = option
    if menu == "1":
        menu = "Wireline board"
    elif menu == "2":
        menu = "D&M board"
    elif menu == "3":
        menu = "Other board"
    else:
        print("Invalid option selected")
        ## menu_select()
    return menu


def pottingcoating(dict1,mainlysmtornot,option):
    
    if menu_select(option)=="Wireline board":
        outputlist.append("Wireline board")
        #print("Bare PWA")
        return 3
    elif menu_select(option)!= "D&M board":
        #print("Consult CPE")
        outputlist.append("Consult CPE\n")
        return 4
        
        
    elif mainlysmtornot==0:
        #outputlist.append("\n not mainly smt \n")
        
        #print("potting on desginated areas with large and heavy parts (such as soft leaded toroides ) Conformal coating (auto spray preferred) on remaining area. ")
        return 1
       
        
    elif hoodwithpropersealing=="yes":
        outputlist.append("hoodwithpropersealing")
        return 2
        #print("Bare PWA")
        
        
    else:
        outputlist.append("coating")
        return 0

        #print("Conformal coating with auto spray method")


def findkeyword(keyword,ptf_file_content,option):
    ## f=open('part_table.ptf',"r")
    ## data=f.readlines()
    data  = ptf_file_content
    
    #count=0
    linerecord=[]
    # print("keyword is:",keyword)
    for i in data:
        i = i.decode('utf-8')
        # print(i)
        if i[0]=="'" or i[0]==':':
            if i[0]==':':
                linerecord=[]
            linerecord.append(i)
            # print(i)
            
            if keyword in str(i):
                # print("keyword found in i:",i)
                a=linerecord[0].split('|')
                b=i.split('|')
                result=dict(zip(a,b))
                # print(result.keys())
                # print("result is:",result)
                
                sumresult={}
                sumresult["Part Number"],sumresult["Mission profile"],sumresult["DFA_DEV_CLASS"], sumresult["PINCOUNT"]=result[":SLB_PN(OPT='Unknown')"],menu_select(option),result["DFA_DEV_CLASS"],result["PINCOUNT;\r\n"]
                outputlist.append(str(sumresult))
                # print("For each i its Result is: ",i,result)
                return result
                
                
                #mainlysmt(result)


def potted_pin(dictionary,output):
    # print("Package is : ",dictionary["DFA_DEV_CLASS"])
    # print("PINCOUNT IS", int( dictionary['PINCOUNT;\r\n'].strip("' \r\n")),"Output is : ",output)
    if output==1 or output==0 :

        if dictionary is not None and "DFA_DEV_CLASS" in dictionary and "SMT" in dictionary["DFA_DEV_CLASS"]:
            if dictionary["DFA_DEV_CLASS"] in bgaqf:  #gull_wing=="no":
                outputlist.append("\nsmt package\n")
                
                if dictionary["DFA_DEV_CLASS"] == bgaqf[2]: #"BGA" in dictionary["QUALIF_ID(OPT='0')=PACKAGE"]:
                    outputlist.append("\nbga\n")
                    if output==1:
                        return "potting","underfill"
                    else:
                        return "coating", "underfill"
                elif dictionary["DFA_DEV_CLASS"]=="'SMT_QFN'" or dictionary["DFA_DEV_CLASS"]==bgaqf[1]:
                    outputlist.append("\n smt passive and qfn \n")
                    if output==1:
                        return "potting","No underfill"
                    else:
                        return "coating", "No underfill"
            else:
                if output==1:
                    outputlist.append("\nsmt package\n")
                    # print("PINCOUNT IS" ,int(dictionary['PINCOUNT;\r\n'].strip()))
                    if int(dictionary['PINCOUNT;\r\n'].strip().replace("'", "", 2))>=8:
                        # print("Package is : ",dictionary["DFA_DEV_CLASS"],"Needs ","underfill potting")
                        # print("underfill potting")
                        outputlist.append("pintcount >=8 ")
                        
                        return "potting","underfill"
                        
                    else:
                        # print("Package is : ",dictionary["DFA_DEV_CLASS"],"Needs ","NO Underfill potting")
                        # print("No underfill potting")
                        outputlist.append("pin count < 8")
                        return "potting","No underfill"
                elif output==0:
                    outputlist.append("\nsmt package\n")    
                    if int(dictionary['PINCOUNT;\r\n'].strip().replace("'", "", 2))>=28:
                        outputlist.append("pin count >=28")
                        # print("Package is : ",dictionary["DFA_DEV_CLASS"],"Needs ","underfill coating")
                        # print("underfill coating")
                        return "coating","underfill"
                        
                    else:
                        # print("Package is : ",dictionary["DFA_DEV_CLASS"],"Needs ","No Underfill Coating")
                        # print("No underfill coating")
                        outputlist.append("pin count <28")
                        return "coating","No underfill"

        else:
            outputlist.append("not smt \n")
            if output==1:
                return "potting","No underfill"
            else:
                return "coating", "No underfill"
    if output==2 or output==3:
        outputlist.append("bare pwd")
        return "Bare","PWA"
    
    if output==4:
        outputlist.append("Consult cpe")
        return "consult","CPE"
    
## Text1 = ""
Text1 = []
def finalrun(partdict,topdown,smtornot,ptf_file_content,option): 
    list1=[]
    list2=[]
    potting=[]
    coatingl=[]
    consultcpe=[]
    barepwa=[]
    finaloutput=[]
    # runs = 0
    for i in partdict.keys():
        # if runs == 21:
        #     break
        # runs += 1
        outputlist.append("\t\n")
        outputlist.append(i)
        outputlist.append("\t\n")
        # print("For i in partdict.keys: ",i)            
        #result1=
        # print("partdict[i] for i is :",partdict[i],"\t",i)
        data=findkeyword(partdict[i],ptf_file_content,option)
        # print("data",data)
        # print(data.keys())
        flag=pottingcoating(data,smtornot,option)
        # print("flag",flag)
        # print("data[DFA_DEV_CLASS] for key is : ",data["DFA_DEV_CLASS"]," ",data.)
        a,b=potted_pin(data,flag)
        # print("a,b",a,b)
        if a=="potting":
            if b=="underfill":
                list1.append(i)
            if b=="No underfill":
                potting.append(i)
        # TESTING
        # if i == 'U26':
        #     print("patdict[i] : ",partdict[i])
        #     print("smtornot is : ",smtornot)
        #     print("data is : ",data)
        #     print("flag is : ",flag)
        #     print("a,b is : ",a,b)
                
                
        if a=="coating":
            if b=="underfill":
                list2.append(i)
            if b=="No underfill":
                coatingl.append(i)
                
        if a=="consult" and b=="CPE":
            consultcpe.append(i)
        if a=="Bare" and b=="PWA":
            barepwa.append(i)
    
    print(topdown+"\n----------------------------------------------------------------------------\n")
    print("potting and underfill\n",list1,"\ncoating and underfill\n",list2,"\n","\nConsult CPE:\n",consultcpe)
    

    
    line=f"\n{topdown} "#"\n------------------------------------------------------------------------------\n"
    # Text1.insert(END, line)
    Text1.append(line)
    
    if list1:
       
        finaloutput.append("Potting")
        #line=f"Potting & Underfill : {list1} \n"
        # Text1.insert(END, finaloutput)
        Text1.append(finaloutput)
        line=f"\n\nUNDERFILLED PART: {list1} \n"
        # Text1.insert(END, line)
        Text1.append(line)
        
        
    elif potting:
        finaloutput.append("Potting")
        
        # Text1.insert(END, finaloutput)
        Text1.append(finaloutput)
        line=f"\n\nUNDERFILLED PART: None \n"
        # Text1.insert(END, line)
        Text1.append(line)
        
    if list2:
        
        finaloutput.append("Coating")
        
        # Text1.insert(END, finaloutput)
        Text1.append(finaloutput)
        line=f"\n\nUNDERFILLED PART: {list2} \n"
        # Text1.insert(END, line)
        Text1.append(line)
        
    elif coatingl:
        finaloutput.append("Coating")
        
        # Text1.insert(END, finaloutput)
        Text1.append(finaloutput)
        line=f"\n\nUNDERFILLED PART: None \n"
        # Text1.insert(END, line)
        Text1.append(line)
        
    
        
    if consultcpe:
       
        finaloutput.append("Consult CPE")
        # Text1.insert(END, finaloutput)
        Text1.append(finaloutput)
        line=f"\n\nUNDERFILLED PART: None \n"
        # Text1.insert(END, line)
        Text1.append(line)
        #global dict1
        '''if len(partdict)==len(consultcpe):
            line="\nConsult CPE\n"
            Text1.insert(END, line)
        else:
            line=f"\nConsult CPE for: {consultcpe} \n"
            Text1.insert(END, line)'''
    
    if not list1 and not list2  and not consultcpe and not potting and not coatingl:
        finaloutput.append("NO POTTING/NO COATING")
        # Text1.insert(END, finaloutput)
        Text1.append(finaloutput)
        line=f"\n\nUNDERFILLED PART: None \n"
        # Text1.insert(END, line)
        Text1.append(line)
        #line="\nNo potting, No coating, No underfill\n"
        #Text1.insert(END, line)
    
    #return list1,list2,consultcpe,potting,coatingl,barepwa
    line="\n-----------------------------------------------------------------------------------------------\n"
    # Text1.insert(END, line)
    Text1.append(line)
    return list1,list2,consultcpe

def dest_lbls():
    # Text1.delete("1.0", "end")
    for msg in msglist:
        #msg.after(100, msg.destroy())
        msg.destroy()
    for er in errlist:
        er.destroy()
    global outputlist
    outputlist=[]


def mainloop1(ptf_file_content,xml_file,option):
    dest_lbls()
    try:
        ## outputlist.append("\n--------------------------------------------\n")
        
        #f=open(filepath.get())
        #data=json.load(f)
        #dict1=data["top"]
        #dict2=data["bottom"]  
        global dict1, dict2
        ## dict1,dict2=run_func_with_loading_popup_new(lambda: readinput(), "Reading inputs", window_title, bounc_speed, pb_length, App)
        dict1,dict2=read_xml(xml_file)
        # print("dict1",dict1)
        # print("dict2",dict2)
        
        if not dict1:
            raise IOError("Could not find top side components")
        '''if not dict2:
            raise IOError("Could not find bottom top side components")'''
        
            #print(csv)
        
        print("Checking for mainly SMT Top")
        mainlySMTtop = mainlysmtfunc(dict1,ptf_file_content)
        # print("mainlySMTtop",mainlySMTtop)
        print("Checking for mainly SMT Bottom")
        mainlySMTbottom = mainlysmtfunc(dict2,ptf_file_content)
        # print("mainlySMTbottom",mainlySMTbottom)
        print("Final Run Top -> Filtering Top side components")
        tlist1,tlist2,tconsultcpe = finalrun(dict1,"TOP SIDE:",mainlySMTtop,ptf_file_content,option)
        print("Final Run Bottom -> Filtering Bottom side components")
        blist1,blist2,bconsultcpe = finalrun(dict2, "BOTTOM SIDE:",mainlySMTbottom,ptf_file_content,option)

        print("Successfully completed")
        return  tlist1,tlist2,tconsultcpe,blist1,blist2,bconsultcpe,outputlist
        # for line in outputlist:
        #     print(line)

    
    
    ##   mainlySMTtop=run_func_with_loading_popup_new(lambda: mainlysmtfunc(dict1), "Checking for mainly SMT", window_title, bounc_speed, pb_length, App)   
    ##   mainlySMTbottom=run_func_with_loading_popup_new(lambda: mainlysmtfunc(dict2), "Checking for mainly SMT", window_title, bounc_speed, pb_length, App)
        #list1,list2,list3=finalrun(dict1,"TOP SIDE:",mainlySMTtop)
    ##    run_func_with_loading_popup_new(lambda: finalrun(dict1,"TOP SIDE:",mainlySMTtop), "filtering Top side components", window_title, bounc_speed, pb_length, App)
        #list1,list2,list3=finalrun(dict2, "BOTTOM SIDE:",mainlySMTbottom)
    ##run_func_with_loading_popup_new(lambda: finalrun(dict2,"BOTTOM SIDE:",mainlySMTbottom), "filtering Bottom side components", window_title, bounc_speed, pb_length, App)
            
    except FileNotFoundError as e:
        print("No such file available")
        ##errmsg = Label(App, text=e, background='white', foreground='red')
        ##errmsg.grid(row=6, column=0, sticky = 'w', columnspan=3)
        ##errlist.append(errmsg)
        errlist.append(e)
         
    
    except IOError as e:
        print(e)
        ##messagebox.showerror('Error',e)
        
    except NameError as ne:
        print(ne)
        ##messagebox.showerror('Error',"No such file or directorye")
    '''for i in outputlist:
        outputfile.write(i)'''
    




