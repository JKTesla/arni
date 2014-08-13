import os
import rospy
import rospkg


from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget

from rqt_gui_py.plugin import Plugin

class OverviewPlugin(Plugin):

    def __init__(self, context):
        super(OverviewPlugin, self).__init__(context)
        self.setObjectName('OverviewPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which is a sibling of this file
        # in this example the .ui and .py file are in the same folder
	rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('rqt_overview'), 'resources', 'OverviewWidget.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        self._widget.setObjectName('OverviewPluginUi')
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instances of your 
        # plugin at once, these lines add number to make it easy to 
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

	self._connect_slots()

    def _connect_slots(self):
	"""Initializes the slots of the OverviewPlugin."""
	self._widget.tab_widget.currentChanged.connect(self._on_current_tab_changed)
	self._widget.range_combo_box.currentIndexChanged.connect(self.on_range_combo_box_index_changed)

    def _on_current_tab_changed(self, tab):
	"""The Plugin wants to get notified when the tab changed so it can e.g. draw the graphs.

	:param tab: the index of the selected tab
	:type tab: int
	"""
	pass

    def on_range_combo_box_index_changed(self, index):
	"""Handels the change of the graph range.
	
	:param index: the index of the selected range
	:type index: int
	"""
	pass	

    def update(self):
	"""Updates the Plugin and draws the graphs if draw_graphs is true."""
	pass

    def update_graphs(sef):
	"""Updates and redraws the graphs"""
	pass

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog

