
'''
MIA data viewer implementation based on `Anatomist <http://brainvisa.info/anatomist/user_doc/index.html>`_
'''

from __future__ import print_function
from __future__ import absolute_import
import anatomist.direct.api as ana

from soma.qt_gui.qt_backend import Qt
from ..data_viewer import DataViewer
from ..anasimpleviewer2 import AnaSimpleViewer
from populse_mia.user_interface.data_viewer import resources
from populse_mia.user_interface.data_browser.data_browser \
    import TableDataBrowser
from populse_mia.data_manager.project import TAG_FILENAME, COLLECTION_CURRENT
import os


class MiaViewer(Qt.QWidget, DataViewer):
    '''
    :class:`MIA data viewer <populse_mia.user_interface.data_viewer.data_viewer.DataViewer>`
    implementation based on `PyAnatomist <http://brainvisa.info/pyanatomist/sphinx/index.html>`_
    '''

    def __init__(self):

        super(MiaViewer, self).__init__()

        self.anaviewer = AnaSimpleViewer()

        findChild = lambda x, y: Qt.QObject.findChild(x, Qt.QObject, y)

        awidget = self.anaviewer.awidget

        #Filter action Icon (find images from the browser)
        filter_action = findChild(awidget, 'filterAction')
        filter_action.triggered.connect(self.filter_documents)

        layout = Qt.QVBoxLayout()
        self.setLayout(layout)
        self.anaviewer.awidget.setSizePolicy(Qt.QSizePolicy.Expanding,
                                          Qt.QSizePolicy.Expanding)
        layout.addWidget(self.anaviewer.awidget)

        #comments were for when I tried to display both viewers (must be added as arguments is init too)
        #self.project = project
        #self.documents = docs
        self.project = None
        self.documents = []
        self.displayed = []

    def setGridLayout(self):
        a = ana.Anatomist('-b')
        #a.deleteObjects(self.awindows)
        print('length displayed', len(self.displayed))
        print('2', self.displayed)
        print('3', len(self.documents))
        print('4', self.documents)
        #a.removeObjects(self.displayed, self.anaviewer.awidget, False)
        self.anaviewer.loadObject(self.displayed[0], grid=True)
        #for i in range(len(self.awindows)):
            #self.viewgridlay.removeWidget(self.awindows[i].getInternalRep())
        #self.anaviewer.createTotalWindow(["Coronal", "Axial", "Sagittal", "3D"], True)

    def display_files(self, files):
        self.displayed += files
        for filename in files:
            self.anaviewer.loadObject(filename)

    def displayed_files(self):
        return self.displayed

    def remove_files(self, files):
        self.anaviewer.deleteObjectsFromFiles(files)
        self.files = [doc for doc in self.displayed
                      if doc not in files]

    def set_documents(self, project, documents):
        if self.project is not project:
            self.clear()
        self.project = project
        self.documents = documents

    def filter_documents(self):
        dialog = Qt.QDialog()
        layout = Qt.QVBoxLayout()
        dialog.setLayout(layout)
        table_data = TableDataBrowser(
            self.project, self, self.project.session.get_shown_tags(), False,
            True, link_viewer=False)
        layout.addWidget(table_data)
        hlay = Qt.QHBoxLayout()
        layout.addLayout(hlay)
        ok = Qt.QPushButton('Import')
        hlay.addWidget(ok)
        ok.clicked.connect(dialog.accept)
        ok.setDefault(True)
        cancel = Qt.QPushButton('Cancel')
        hlay.addWidget(cancel)
        cancel.clicked.connect(dialog.reject)
        hlay.addStretch(1)

        # Reducing the list of scans to selection
        all_scans = table_data.scans_to_visualize
        table_data.scans_to_visualize = self.documents
        table_data.scans_to_search = self.documents
        table_data.update_visualized_rows(all_scans)

        res = dialog.exec_()
        if res == Qt.QDialog.Accepted:
            points = table_data.selectedIndexes()
            result_names = []
            for point in points:
                row = point.row()
                # We get the FileName of the scan from the first row
                scan_name = table_data.item(row, 0).text()
                value = self.project.session.get_value(COLLECTION_CURRENT,
                                                       scan_name, TAG_FILENAME)
                value = os.path.abspath(os.path.join(self.project.folder,
                                                     value))
                result_names.append(value)
            self.display_files(result_names)