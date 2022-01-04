__doc__ = "Remove Image Links That have 0 Instances Placed."
__title__ = "Remove Image\nLinks"
__author__ = "ruanswart@bimco.ie"

from Autodesk.Revit.DB import *
from rpw.ui.forms import Alert

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
imgType = {}
typeID = {}
toDel = []
delImg = 0

# Creating collector instance and collect all image types in the document
col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RasterImages).WhereElementIsElementType()
# Creating dict from Types and set count to 0
for c in col:
	imgType[c.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()] = 0
	typeID[c.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()] = c.Id

# update count to placed instances
iCol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RasterImages).WhereElementIsNotElementType()
for i in iCol:
	if i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString() in imgType:
		imgType[i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()] += 1

# Find elements that have no placed instances and delete

t = Transaction(doc)
t.Start(__title__)

for x, y in imgType.items():
	for x1, y1 in typeID.items():
		if y == 0:
			if x == x1:
				toDel.append(y1)

for d in toDel:
	doc.Delete(d)
	delImg += 1

t.Commit()

# Notify End
if delImg == 0:
	Alert("No Image Links have been removed.", "Notification")
elif delImg > 0:
	Alert("{} Image Link(s) have been removed.".format(delImg), "Notification")