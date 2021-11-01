__doc__ = "Shows who worked on a selected element."
__title__ = "Who Did\nThat?"
__author__ = "ruanswart@bimco.ie"

import clr

#Import the Revit API
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from rpw.ui.forms import Alert


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

alertMessage = ''

if not doc.IsWorkshared:
	Alert('This is not a workshared model', 'Worksharing')
else:
# Select an Element
	sel = uidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)

# Alert Tooltip Info
	alertMessage += 'Model Update Status : '+(WorksharingUtils.GetModelUpdatesStatus(doc, sel.ElementId)).ToString().split("@",1)[0]+'\n'
	alertMessage += 'Check Out Status : '+(WorksharingUtils.GetCheckoutStatus(doc, sel.ElementId)).ToString().split("@",1)[0]+'\n'
	alertMessage += '\n'
	alertMessage += 'Creator : '+(WorksharingUtils.GetWorksharingTooltipInfo(doc, sel.ElementId).Creator).ToString().split("@",1)[0]+'\n'
	alertMessage += 'Owner : '+(WorksharingUtils.GetWorksharingTooltipInfo(doc, sel.ElementId).Owner).ToString().split("@",1)[0]+'\n'
	alertMessage += 'Last Changed By : '+(WorksharingUtils.GetWorksharingTooltipInfo(doc, sel.ElementId).LastChangedBy).ToString().split("@",1)[0]

	Alert(alertMessage, 'Element Info')