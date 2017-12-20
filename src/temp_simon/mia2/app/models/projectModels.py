from models.generics import GenericItem
from utils.enums import TagType

class Tag():

    def __init__(self, name, replace, value, origin):
        #GenericItem.__init__(self)
        self.name = name
        self.replace = replace
        self.value = value
        self.origin = origin


class Scan(GenericItem):

    def __init__(self, file_path):
        GenericItem.__init__(self)
        self.file_path = file_path
        self._tags = []
        self._delete_tags = []

    def _get_tags(self):
        return self._tags

    def _get_delete_tags(self):
        return self._delete_tags

    def _get_json_tags(self):
        return self._json_tags

    def _get_nifti_tags(self):
        return self._nifti_tags

    def _get_custom_tags(self):
        return self._custom_tags
    
    def getAllTags(self):
        result = []
        for origin in TagType:
            result.extend(self.getAllTagsByOrigin(origin))
        return result    
   
    def getAllTagsByOrigin(self,origin):
        result = []
        deleteTag = []
        replaceTag = []
        for tag in self._get_delete_tags():
            if tag not in deleteTag and tag.origin == origin:
                deleteTag.append(tag)
                #print('DELETED '+tag.name + ' '+tag.value)
        for tag in self._get_tags():
            #print('INTO GET TAGS '+tag.name + ' '+tag.value)
            if tag not in deleteTag and tag not in result and tag.origin == origin:
                #print('TAG TO BE ADDED '+tag.name + ' '+tag.value)
                if tag.replace != "":
                    result.append(tag)
                    replaceTag.append(tag.replace)
                    for l_tag in result:
                        if l_tag.name == tag.replace:
                            result.remove(l_tag)
                            deleteTag.append(l_tag)
                else:
                    if tag.name in replaceTag:
                        deleteTag.append(tag)
                    else:
                        result.append(tag)
            else:
                pass
        return result
    
    def getAllTagsNames(self):
        result = []
        for origin in TagType:
            result.extend(self.getAllTagsNamesByOrigin(origin))
        return result

    def getAllTagsNamesByOrigin(self, origin):
        result = []
        deleteTag = []
        replaceTag = []
        for tag in self._get_delete_tags():
            if tag.name not in deleteTag and tag.origin == origin:
                deleteTag.append(tag.name)
        for tag in self._get_tags():
            if tag.name not in deleteTag and tag.name not in result and tag.origin == origin:
                if tag.replace != "":
                    result.append(tag.name)
                    replaceTag.append(tag.replace)
                    for l_tag in result:
                        if l_tag == tag.replace:
                            result.remove(l_tag)
                            deleteTag.append(l_tag)
                else:
                    if tag.name in replaceTag:
                        deleteTag.append(tag.name)
                    else:
                        result.append(tag.name)
            else:
                pass
        return result

    def addTag(self, tagtype, tag):
        if (tagtype == TagType.JSON):
            self._get_tags().append(tag)
        if (tagtype == TagType.NIFTI):
            self._get_tags().append(tag)
        if (tagtype == TagType.CUSTOM):
            self._get_tags().append(tag)
        return self

    def addJsonTag(self, tag):
        self.addTag(TagType.JSON, tag)

    def addNiftiTag(self, tag):
        self.addTag(TagType.NIFTI, tag)

    def addCustomTag(self, tag):
        self.addTag(TagType.CUSTOM, tag)

    def delete_tag(self, tag):
        self._get_delete_tags().append(tag)
        
    def updateTagValue(self, tag_name, new_value):
        for n_tag in self._get_tags():
            if n_tag.name == tag_name:
                self._get_tags().append(Tag(n_tag.name, '', new_value, TagType.CUSTOM))
                break
            else:
                pass
        return self
    
    def updateTagName(self, tag_name, new_name):
        for n_tag in self._get_tags():
            if n_tag.name == tag_name:
                self._get_tags().append(Tag(new_name, tag_name, n_tag.value, TagType.CUSTOM))
                break
            else:
                pass
        return self

#ProjectLight is same as a Project but without all data Scan/Tags
#So it can be stored in the db file projects.json to store all existing projects
#Project data are stored in the dedicated Project file (among with the rest)
class ProjectLight(GenericItem):

    def __init__(self, name):
        GenericItem.__init__(self)
        from time import strftime,localtime
        self.name = name
        self.folder = ""
        self.raw_data = ""
        self.processed_data = ""
        self.bdd_file = ""
        self.date = strftime('%d/%m/%y %H:%M', localtime())
        
class Project(ProjectLight):

    def __init__(self, name):
        ProjectLight.__init__(self,name)
        self._scans = []

    def _get_scans(self):
        return self._scans

    def addScan(self, scan):
        self._get_scans().append(scan)
        
    def addScans(self, scans):
        for scan in scans:
            self.addScan(scan)

    def getAllTags(self):
        result = []
        for origin in TagType:
            result.extend(self.getAllTagsByOrigin(origin))
        return result
    
    def getAllTagsByOrigin(self,origin):
        result = []
        if(isinstance(self, Project)):
            for i in self._get_scans():
                for y in i.getAllTagsByOrigin(origin):
                    if y not in result and y.origin == origin.value:
                        result.append(y)
        

    def getAllTagsNames(self):
        result = []
        for origin in TagType:
            result.extend(self.getAllTagsNamesByOrigin(origin))
        return result

    def getAllTagsNamesByOrigin(self, origin):
        result = []
        if(isinstance(self, Project)):
            result = []
            for scan in self._get_scans():
                for tagname in scan.getAllTagsNamesByOrigin(origin):
                    if tagname not in result:
                        result.append(tagname)
        return result

    def addTag(self, tagtype, tag):
        for scan in self._get_scans():
            scan.addTag(tagtype, tag)
        return self

    def deleteTag(self,tag):
        for scan in self._get_scans():
            scan.deleteTag(tag)
        return self

    def updateTagValue(self, tag_name, new_value):
        for scan in self._get_scans():
            scan.updateTagValue(tag_name, new_value)
        return self
    
    def updateTagName(self, tag_name, new_name):
        for scan in self._get_scans():
            scan.updateTagName(tag_name, new_name)
        return self

#The point is get a Project instance from a loaded project 
def castFromProjectLight(project,projectLight):
    project.uid = projectLight.uid
    project.name = projectLight.name
    project.folder = projectLight.folder
    project.raw_data = projectLight.raw_data
    project.processed_data = projectLight.processed_data
    project.bdd_file = projectLight.bdd_file
    project.date = projectLight.date
    return project
        
        