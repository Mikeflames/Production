from django.shortcuts import render
from .test import mainloop1
from django.http import HttpResponse


def pc(request):
    if request.method == 'GET':
    #     options = ['Wireline board', 'D&M board','Other']
        return render(request, 'upload_xml.html')

    if request.method == 'POST':
        xml_file = request.FILES.get('xml_file')
        ptf_file = request.FILES.get('ptf_file')
        ptf_file_content = ptf_file.readlines()
        uploaded_xml = request.FILES['xml_file'].name

        # ptf_file_content = read_file(ptf_file)
        option = request.POST.get('selected_option')
        # option = request.GET.get('options')
        if xml_file and ptf_file:
            print("Both files were uploaded successfully")
            print("option is ",option)
            # print("ptf file content is ",ptf_file_content)
            tlist1,tlist2,tconsultcpe,blist1,blist2,bconsultcpe,outputlist = mainloop1(ptf_file_content,xml_file,option)
            # print("dcsdcsdcc",tlist2)
            # print(type(tlist2))
            print("Successfully called test file")
            # return render(request, 'pc.html', {'tlist1': tlist1,'tlist2': tlist2,'tconsultcpe': tconsultcpe,'blist1': blist1,'blist2': blist2,'bconsultcpe': bconsultcpe,'outputlist': outputlist})
            result = True
            return render(request, 'upload_xml.html', {'tlist1': tlist1,'tlist2': tlist2,'tconsultcpe': tconsultcpe,'blist1': blist1,'blist2': blist2,'bconsultcpe': bconsultcpe,'outputlist': outputlist,'result': result,
                                                       'uploaded_xml': uploaded_xml})
        else:
            print("One or both files were not uploaded, handle the error...")
            return HttpResponse("Hello, World Files Not Uploaded Correctly!")
