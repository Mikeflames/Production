from django.shortcuts import render
from .test import mainloop1
from django.http import HttpResponse

top_list = []
bottom_list = []
top = ""
bottom = ""

def checker(tlist1,tlist2,tconsultcpe,blist1,blist2,bconsultcpe):
   
    if tlist1:
        top = "Potting"
        top_list = tlist1
    elif tlist2:
        top = "Coating"
        top_list = tlist2
    elif tconsultcpe:
        top = "Consult CPE"
        top_list = tconsultcpe
    else:
        top = "No Parts here"
        top_list = []
    
    # For Bottom
    if blist1:
        bottom = "Potting"
        bottom_list = blist1
    elif blist2:
        bottom = "Coating"
        bottom_list = blist2
    elif bconsultcpe:
        bottom = "Consult CPE"
        bottom_list = bconsultcpe
    else:
        bottom = "No Parts here"
        bottom_list = []

    return top_list, bottom_list, top, bottom
        


def pc(request):
    if request.method == 'GET':
    #     options = ['Wireline board', 'D&M board','Other']
        return render(request, 'upload_xml_1.html')

    if request.method == 'POST':
        xml_file = request.FILES.get('xml_file')
        ptf_file = request.FILES.get('ptf_file')
       
        # ptf_file_content = read_file(ptf_file)
        option = request.POST.get('selected_option')
        # option = request.GET.get('options')
        if xml_file and ptf_file:
            ptf_file_content = ptf_file.readlines()
            uploaded_xml = request.FILES['xml_file'].name
            print("Both files were uploaded successfully")
            # print("option is ",option)
            # print("ptf file content is ",ptf_file_content)
            tlist1,tlist2,tconsultcpe,blist1,blist2,bconsultcpe,outputlist = mainloop1(ptf_file_content,xml_file,option)
            top_list,bottom_list,top,bottom = checker(tlist1,tlist2,tconsultcpe,blist1,blist2,bconsultcpe)
            # print("dcsdcsdcc",tlist2)
            # print(type(tlist2))
            print("Successfully called test file")
            # return render(request, 'pc.html', {'tlist1': tlist1,'tlist2': tlist2,'tconsultcpe': tconsultcpe,'blist1': blist1,'blist2': blist2,'bconsultcpe': bconsultcpe,'outputlist': outputlist})
            result = True
            # return render(request, 'upload_xml_1.html', {'tlist1': tlist1,'tlist2': tlist2,'tconsultcpe': tconsultcpe,'blist1': blist1,'blist2': blist2,'bconsultcpe': bconsultcpe,'outputlist': outputlist,'result': result,
            #                                            'uploaded_xml': uploaded_xml})
            return  render(request, 'upload_xml_1.html', {'result': result,'uploaded_xml': uploaded_xml,'top_list': top_list,'bottom_list': bottom_list,'top': top,'bottom': bottom,'outputlist': outputlist})
        else:
            print("One or both files were not uploaded, handle the error...")
            return HttpResponse("Please Upload Both Files Uploaded Correctly!")

