Change
===

* MyPlugin: added a PluginClass which holds the Widgets tree and selection
* TreeWidget: changed the param type from **..check_box_state_changed from bool to int**
* OverviewPlugin: added missing method **on_range_combo_box_index_changed(index)**

## Configuration files
* Now uses seuid where possible
=> specifications now take **seuid**: {} instead of **type: name**: {} (see arni_processing/resources/testconfig.yaml)
* Now uses list of dictionaries against UserErrors from invalid parameter names

* /arni/aggregation_window (3) Length of time to aggregate topics

## MetadataStorage
* automatic cleanup now depends on the rosparameters /arni/storage/auto_cleanup (True) and /arni/storage/cleanup_timer (30)[seconds]


* AbstractItem needs a new method: get_identifier() --> this is needed in LogFilterProxy to determine the name of this element (at least I think so)
* getInstance no longer needed in ROSModel (add additional classes), the singleton effect is implemented with metaclasses
* *convert some functions from CamelCase to lower_case --> ROSModel.headerData (header_data), ROSModel.columnCount (column_count), ROSModel.rowCount to row_count* --> !!!ERROR!!! These are Qt functions and should not be renamed!!!!
* todo: network diagram is still missing in the design, also in the final versions --> add!
* found solution to method overloading in one case --> 4 new methods __add_rated_statistics_item(..), the old will be removed, are changed to *private* cause only needed internally --> 4 locks are needed, names adapated
* in ROSModel: Thread not longer needed --> Timer replaced its functionality, therefore also start() can deleted, only update_model is stillt needed as callback for the timer
* update_model in ROSModel no longer public
* AbstractItem needed some more methods to match the qt interfaces --> child_count, column_count, row, 
* constructor/ __init__ from ROSModel should only get a parent item, nothing more --> data is no longer a parameter
* new private item in ROSModel: __mapping
* AbstractItem constructor changed to def __init__(self, parent_item=None, identifier, type, can_execute_actions) --> constructor of the subclasses have been changed accordingly
*  **IMPORTANT**: should rethink the naming conventions in the gui part because of qt and python mixing the convetions can be fulfilled on the python/ros side...
* the transform_data method has been deleted, 4 other methods have taken its place **docu still missing**
* the names of the services now are /get_statistic_history and /execute_node_reaction
* name change from add_log_item to add_log_entry
* new class **ErrorDelegate** for painting the log model with color
* get_detailed_data 
* extract the painting part from get_detailed_data to the widgets
* get_erroneous_entries in abstractItem
* overview.ui from log_tab_tree_widget to log_tab_tree_view.

##Big TODOS:
* interpolate the data with flowcharts?
* enter tr() everywhere for internationalisation
* the units in the overview are missing (maybe also some color if someone is too high --> not our )
* scrolling does not work because of the permanent updates...--> solution: if no data has changed, simply get_detailed_data simply returns None --> or not calling the update so often, every minute should suffice

* DAS LOGGEN GEHT AUCH NOCH GAR NICHT!!! Funktioniert vermutlich, es werden aber noch kein daten gepusht.

* SelectionWidget: Services definieren und überprüfen

WiP
* on close of one widget in detail gui, close the other!
* TreeWidget: close methoden sync überprüfen --> nicht möglich?!?
* RUNTIME_ERROR BECAUSE ELEMENT HAS BEEN DELETED --> Timer Fehler oder so... Schwer/nicht behebbar
* why are sometimes empty values given to the axis? --> for no plausible reason

Done
* lock updateGraphs --> non reentrant functions, otherwise segmentation faults occur!
* locking the updateModel from modifying the data while plotting the data in the gui --> shape errors
* state wird noch nicht regelmäßig im richtigen zeitfesnter aufgerufen!!! führt sicher zu fehlen, muss aber vermtulich allgemein im rahmen der rated datas angepasst werden. 
* make sure there are no more dict["time"] calls, they are invalid
* reformat the ROSModel to use the seuid helper class --> Helper class returns None values --> no longer using!!!
* execute_action not implemented
* why are there runtimeerrors when closing the gui. and why are there these threading errors(might it be the timers?)
* GUI WANTS TO RECEIVE ITEMS THE TOPIC DOES NOT PROVIDE!!!
* gibt immer noch index-fehler, falls ein element abgefragt wird, das keine daten hat!!!
* reason for wrong return values: *args is never None, so if args is not None will always enter even though args might be empty!!!

=======
* selection.ui from log_tab_tree_widget to log_tab_tree_view.
* arni_gui_detail: moved __on_item_in_item_tree_view_double_clicked(self, item): from tree_widget to arni_gui_detail to handle the content change of the selection_widget
* indexerror in ros_model...