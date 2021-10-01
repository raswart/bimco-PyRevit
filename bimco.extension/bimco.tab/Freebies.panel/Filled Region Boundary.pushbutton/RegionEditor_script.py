__doc__ = "Select new Boundary Line Style to be used for all selected Filled Regions in the Active View."
__title__ = "Filled Region\nBoundary"
__author__ = "ruanswart@bimco.ie"

#Dependencies
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from rpw.ui.forms import SelectFromList
from rpw.ui.forms import Alert

#Variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
rgnDict = {}
lineDict = {}
cnt = 0

#Filled Region collector in Active View
filledRegion = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(FilledRegion).ToElements()
for rgn in filledRegion:
    rgnDict[rgn.LookupParameter("Type").AsValueString()] = rgn.GetTypeId()

#Collect Lines
prjctLines = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
lineStyleSubTypes = prjctLines.SubCategories
for lns in lineStyleSubTypes:
    lineDict[lns.Name] = lns.Name

#get user input from SelectFromList input form
if len(rgnDict) > 0:
    selectedRegion = SelectFromList("Select Filled Region",rgnDict,"Select Filled Region Type that needs to be updated",True,True)

#get Line Types input from SelectFromList input form
if len(lineDict) > 0:
    selectedLine = SelectFromList("Select Line Type",lineDict,"Select Line Type to be used",True,True)

grh = FilteredElementCollector(doc).OfClass(GraphicsStyle).ToElements()
for g in grh:
    if g.Name == selectedLine:
        pss = g.Id
        break

#Set the Line Style of the Filled Region Boundary
t = Transaction(doc, __doc__)
t.Start()

for i in filledRegion:
    if selectedRegion == i.GetTypeId():
        try:
            i.SetLineStyleId(pss)
            cnt += 1
        except:
            Alert('Unable to apply selected Line Type.', "Error")

t.Commit()

# Notify End
if cnt == 0:
    Alert('No Filled Regions have been updated.', "Notification")
elif cnt == 1:
    Alert('{} Filled Region has been updated.'.format(cnt),"Notification")
elif cnt > 1:
    Alert('{} Filled Regions have been updated.'.format(cnt), "Notification")