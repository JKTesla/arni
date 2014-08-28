from rospy.rostime import Duration, Time
from python_qt_binding.QtCore import QObject

from threading import Lock


class AbstractItem:
    """ 
    Provides a unified interface to access the items of the model.
    INTERNAL: WARNING! Whenever the key-values at the beginning are not set right, the oddest things may occur!
    """

    def __init__(self, seuid, parent=None, *args):
        """Initializes the AbstractItem.
        
        :param seuid: the seuid of the AbsractItem
        :type seuid: str
        :param parent: the parent-item
        :type parent: AbstractItem
        :param *args:
        :type *args: 
        """
        #print(str(type(self)) + str(type(seuid)) + str(type(parent)))
        #super(AbstractItem, self).__init__(parent)

        self._data = {}
        self.__rated_data = {}
        self.__child_items = []
        self.__parent = parent
        self.seuid = seuid
        self._type = "type"
        self.__data_attribute = "data"
        self.__state = []
        # WARNING!!! Child classes have to call the append_data_list method, otherwise will not work!!!
        #self._attributes = []
        #self._attributes.extend(args)
        self.__last_update = Time.now()
        self.__creation_time = Time.now()

        self._add_data_list("window_start")
        self._add_data_list("window_stop")
        self._add_rated_data_list("window_start")
        self._add_rated_data_list("window_stop")


    def get_seuid(self):
        """
        Returns the seuid of the Abstractitem.

        :returns: str
        """
        return self.seuid


    def get_state(self):
        """
        Returns the state of the AbstractItem.

        :returns: str
        """
        if self.__state:
            return self.__state[-1]



    def _add_data_list(self, name):
        """
        Adds keys to the data_list.

        :param name: the key to be added
        :type name: str
        """
        #print("added " + name)
        self._data[name] = []


    def _add_rated_data_list(self, name):
        """
        Adds keys to the rated_data_list.

        :param name: the key to be added
        :type name: str
        """
        self.__rated_data[name] = []


    def append_child(self, child):
        """
        Append a child to the list of childs.

        :param child: the child item
        :type child: AbstractItem
        """
        self.__child_items.append(child)


    def append_rated_data_dict(self, data):
        """
        Appends data to the rate_data of the AbstractItem.

        :param data: the data to append in key value from
        :type data: dict
        """
        if "window_stop" not in data:
            data["window_stop"] = Time.now()
        for attribute in self.__rated_data:
            if attribute in data:
                self._data[attribute].append(data[attribute])
            else:
                # todo: is there something better than None in this case? like "" ?
                self._data[attribute].append(None)

        if "state" in data:
            self.__state.append(data["state"])
        else:
            self.__state.append(data["ok"])

        self.__update_current_state()


    def append_data_dict(self, data):
        """
        Appends data to the data of the AbstractItem.

        :param data: the data to append in key value form
        :type data: dict
        """
        if "window_stop" not in data:
            data["window_stop"] = Time.now()
        for attribute in self._data:
            if attribute in data:
                self._data[attribute].append(data[attribute])
            else:
                # todo: is there something better than None in this case? like "" ?

                self._data[attribute].append(None)
        if "state" in data:
            self.__state.append(data["state"])
        else:
            self.__state.append(data["ok"])
        self.__update_current_state()


    def __update_current_state(self):
        """
        This method udates the current state of the AbstractItem.
        """
        length = len(self.__state)
        # print("__update_current_state")
        # for i in range(length - len(
        # (self.get_items_younger_than(self.__last_update, "window_end", "state"))["window_end"]), length):
        #print(length)
        #print(len(self.__data["window_stop"]))
        if self.__state:
            for i in range(length - len((self.get_items_younger_than(Time.now() - Duration(secs=5), ))["window_stop"]),
                           length):
                if self.__state[i] == "error":
                    self.__state[-1] = "warning"
                    break
        self.__last_update = Time.now()


    #TODO append_data or append_data_dict is correct
    def append_data(self, data):
        """
        Appends data to the data of the AbstractItem.

        :param data: the data to append in key value form
        :type data: dict
        """
        for attribute in self._data:
            try:
                self._data[attribute].append(getattr(data, attribute))
            except KeyError:
                print("KeyError occurred when trying to access %s", attribute)
                raise

        self.__state.append("ok")
        self.__update_current_state()


    def update_rated_data(self, data):
        """Appends data to the rated_data of the AbstractItem.

        :param data: the data to append in key value form
        :type data: dict
        :param window_start: the time of window_start
        :type window_start: Time
        :param window_stop: the time of window_stop
        :type window_stop: Time
        """
        # found = False
        # # todo: are these all bad cases?
        # for current in range(0, len(self.__data["window_start"])):
        #     if window_stop < self.__data["window_start"][current]:
        #         continue
        #     if window_start > self.__data["window_stop"][current]:
        #         continue
        #     found = True

        #todo: WHAT HAPPENS TO STATE AND WHY IS IT NEVER USED

        for entry in self.__rated_data:
            try:
                self.__rated_data[entry].append(data[entry])
            except KeyError:
                print("An entry found in the object dictionary of the rated data was not found in the given rated data")
                raise
        if "state" in data:
            if data["state"] is "error":
                if not self.__state:
                    #todo: this is not good... FIX IT
                    self.__state.append(None)
                self.__state[-1] = "error"
        #if found is not True:
        #    raise UserWarning("No matching time window was found. Could not update the AbstractItem")
        self.__update_current_state()


    def child_count(self):
        """
        Returns the number of children from the AbstractItem.

        :returns: int
        """
        return len(self.__child_items)
        # sum = 0
        # for item in self.__child_items:
        #     sum += 1
        #     sum += item.child_count()
        #
        # return sum
        # return len(self.child_items)


    def column_count(self):
        """
        Returns the number of columns.

        :returns: int
        """
        # todo: return !not! a concrete number here ?!?!
        return 4

    def get_childs(self):
        """
        Returns a list with all children.

        :returns: list
        """
        return self.__child_items


    def get_child(self, row):
        """
        Returns the child at the position row.

        :param row: the index of the row
        :type row: int

        :returns: AbstractItem
        """
        return self.__child_items[row]


    def row(self):
        """
        Returns the index of the Item.

        :returns: int
        """
        if self.__parent:
            return self.__parent.get_childs().index(self)

        return 0


    def get_latest_data(self, *kwargs):
        """
        Returns the latest dict of the data_list or the item of the dict with the given key.

        :param kwargs: the keys to the dict
        :type kwargs: str

        :returns: dict or the item
        """
        return_dict = {}
        #return_dict["state"] = "state unknown"
        if kwargs:
            for key in kwargs:
                if key is 'name':
                    return_dict['name'] = self.seuid
                elif key is 'type':
                    return_dict['type'] = self._type
                elif key is 'data':
                    return_dict['data'] = self.get_short_data()
                elif key is 'state':
                    if self.__state:
                        return_dict['state'] = self.__state[-1]
                    else:
                        return_dict["state"] = "state unknown"
                else:
                    if key in self._data:
                        if self._data[key]:
                            return_dict[key] = self._data[key][-1]
                    elif key in self.__rated_data:
                        if self.__rated_data[key]:
                            return_dict[key] = self.__rated_data[key][-1]
                    else:
                        raise KeyError("item " + key + "was not found")
        else:
        # return dict of latest item
            return_dict['name'] = self.seuid
            return_dict['type'] = self._type
            return_dict['data'] = self.get_short_data()
            for entry in self._data:
                if self._data[entry]:
                    return_dict[entry] = self._data[entry][-1]
                else:
                    return_dict[entry] = "Currently no value avaiable"
            for entry in self.__rated_data:
                if self.__rated_data[entry]:
                    return_dict[entry] = self.__rated_data[entry][-1]
                else:
                    return_dict[entry] = "Currently no value avaiable"
            if self.__state:
                return_dict['state'] = self.__state[-1]
            else:
                return_dict['state'] = "state unknown"
        #print("return_dict")
        #print(return_dict)
        return return_dict


    def parent(self):
        """
        Returns the parent of this or None if there is no parent.

        :returns: AbstractItem
        """
        return self.__parent


    # todo: what are the following 3 methods for and how can they be done better?
    #todo: UPDATE!!!! CURRENTLY NOT WORKING
    def get_items_older_than(self, time, *args):
        """
        Returns all items which are older than time.

        :param time: the upper bound in seconds
        :type time: rospy.Time
        :param kwargs: the keys to the dict
        :type kwargs: str

        :returns: dict of lists
        """
        # todo: method assumes the data comes in sorted by time. if this is not the case, this method will not work!
        #print("info" + " AbstractItem" + " duration of time:" + str(int(str(Time.now() - time))/1000000) + " milliseconds")
        #now = Time.now()
        return_values = {}
        #todo: adapt to args
        if args is not None:
            for key in args:
                return_values[key] = []
            if "window_stop" not in args:
                return_values["window_stop"] = []
        else:
            for key in self._data:
                return_values[key] = []
        breakpoint = 0

        list_of_time = self._data["window_stop"]
        #print(len(list_of_time))
        #print("first time: " + tm.strftime("%d.%m-%H:%M:%S", tm.localtime((int(str(list_of_time[0]))/1000000000))))
        #print("last time: " + tm.strftime("%d.%m-%H:%M:%S", tm.localtime((int(str(time))/1000000000))))
        #print("for")

        if list_of_time[len(list_of_time)-1] < time:
            #print("here")
            for key in return_values:
                return_values[key] = self._data[key]
        else:
            for i in range(0, len(list_of_time), -1):
                #print(i)
                #print(len(list_of_time))
                #print(int(str(list_of_time[i]))-int(str(time)))
                if list_of_time[i] > time:
                    breakpoint = i - 1
                    # i + 1 was the first hit
                    #print("entered")
                    #if args is None:
                    for key in return_values:
                        try:
                            return_values[key] = self._data[key][0:breakpoint]
                            print("i is " + str(i) +"length: " + str(len(return_values[key])) + " complete length: " + str(len(list_of_time)))
                        except IndexError:
                            print("IndexError! length of the list %s, accessed index %s. length of data at given point"
                                  " %s, key is %s", len(list_of_time), i, len(self._data[key]), key)
                            raise
                    break

            # now shrink the time itself
            # print("length time: " + str(len(return_values["window_end"])) + " length state: " + str(len(return_values["state"])))
        #print("length return values: " + str(len(return_values["window_end"])))
        return return_values

        # return_values = []
        # for key in self.__data:
        #     return_values[key] = []
        #
        # list_of_time = self.__data["window_stop"]
        # for i in range(0, len(list_of_time)):
        #     # check timestamp
        #     #end_time = Time.now() - Duration(nsecs=time)
        #     if list_of_time[i] < time:
        #         #return_values.append()
        #         for key in self.__data:
        #             return_values[key].append(self.__data[key][i])
        # return return_values


    def delete_items_older_than(self, time):
        """
        Deletes all items which are older than time.

        :param time: the upper bound
        :type time: rospy.Time
        """
        list_of_time = self._data["window_stop"]
        while list_of_time[0] < time:
            for key in self._data:
                del self._data[key][0]

                # for i in range(0, len(list_of_time)):
                # # check timestamp
                #     #end_time = Time.now() - Duration(nsecs=time)
                #     if list_of_time[i] < time:
                #         #return_values.append()
                #         for key in self.__data:
                #             del self.__data[key][i]


    def get_items_younger_than(self, time, *args):
        """
        Returns all items which are younger than time.

        :param time: the lower bound in seconds
        :type time: rospy.Time

        :returns: dict of lists
        """
        #  todo: method assumes the data comes in sorted by time. if this is not the case, this method will not work!
        #print("info" + " AbstractItem" + " duration of time:" + str(int(str(Time.now() - time))/1000000) + " milliseconds")
        #now = Time.now()
        return_values = {}
        #todo: adapt to args
        if args:
            for key in args:
                return_values[key] = []
            if "window_stop" not in args:
                return_values["window_stop"] = []
        else:
            for key in self._data:
                #print("younger " + key)
                return_values[key] = []
        breakpoint = 0

        list_of_time = None
        try:
            list_of_time = self._data["window_stop"]
        except KeyError:
            print(str(type(self)) + str(self._type) + " " + self.get_seuid() + " window_stop not found")
        length = len(list_of_time)
        #print(len(list_of_time))
        #print("first time: " + tm.strftime("%d.%m-%H:%M:%S", tm.localtime((int(str(self.__data["window_end"][0]))/1000000000))))
        #print("last time: " + tm.strftime("%d.%m-%H:%M:%S", tm.localtime((int(str(self.__data["window_end"][-1]))/1000000000))))
        #print("for"
        if length is not 0:
            if list_of_time[0] >= time:
                for key in return_values:
                    return_values[key] = self._data[key]
            else:
                for i in range(length - 1, -1, -1):
                    #print(i)
                    #print(len(list_of_time))
                    #print(int(str(list_of_time[i]))-int(str(time)))
                    if list_of_time[i] < time:
                        breakpoint = i + 1
                        # i + 1 was the first hit
                        #print("entered")
                        #if args is None:
                        for key in return_values:
                            if key in self._data:
                                return_values[key] = self._data[key][breakpoint:length]
                                #print("i is " + str(i) +"length: " + str(len(return_values[key])) + " complete length: " + str(len(list_of_time)))
                            elif key in self.__rated_data:
                                return_values[key] = self.__rated_data[key][breakpoint:length]
                            elif key is "state":
                                return_values[key] = self.__state[breakpoint:length]
                            else:
                                print(self._data.keys())
                                raise IndexError("IndexError! length of the list %s, accessed index %s. length of data at given point %s, key is %s",
                                    length, i, len(self._data[key]), key)
                    # else:
                    #     for entry in args:
                    #         try:
                    #             #todo [i:len(list_of_time)] is this the right window?
                    #             return_values[entry] = self.__data[entry][breakpoint:len(list_of_time)]
                    #             #print("i is " + str(i) + "key: " + entry + " length: " + str(len(return_values[entry])) + " complete length: " + str(len(list_of_time)))
                    #         except IndexError:
                    #             print(
                    #                 "IndexError! length of the list %s, accessed index %s. length of data at given point %s, key is %s",
                    #                 len(list_of_time), i, len(self.__data[entry]), entry)
                    #             raise
                        break

                # now shrink the time itself

                # print("length time: " + str(len(return_values["window_end"])) + " length state: " + str(len(return_values["state"])))

        #print("length return values: " + str(len(return_values["window_end"])))
        #print("returnvalues")
        #for item in return_values:
        #    print return_values
        return return_values

    # check timestamp
    #start_time = Time.now() - Duration(nsecs=time)
    # if list_of_time[i] > time:
    #     for key in self.__data:
    #         try:
    #             return_values[key].append(self.__data[key][i])
    #         except IndexError:
    #             print("IndexError! length of the list %s,assert(len(return_values) == len(return_values[""])) accessed index %s. length of data at given point %s, key is %s",
    #                   len(list_of_time), i, len(self.__data[key]), key)
    #             raise
    #print("info" + " AbstractItem" + " get_items_younger_than took: " + str(int(str(Time.now() - now))/1000000) + " milliseconds")

    # list_of_time = self.__data["window_stop"]
    # for i in range(0, len(list_of_time) - 1):
    #     # check timestamp
    #     #start_time = Time.now() - Duration(nsecs=time)
    #     if list_of_time[i] > time:
    #         for key in self.__data:
    #             try:
    #                 return_values[key].append(self.__data[key][i])
    #             except IndexError:
    #                 print("IndexError! length of the list %s, accessed index %s. length of data at given point %s, key is %s",
    #                       len(list_of_time), i, len(self.__data[key]), key)
    #                 raise
    # return return_values


    def execute_action(self, action):
        """
        Executes a action on the current item like stop or restart. Calls to this method should be
        redirected to the remote host on executed there.

        :param acion: the action which should be executed
        :type action: RemoteAction
        """
        pass


    def get_detailed_data(self):
        """
        Returns detailed description of current state as html text.

        :return: str
        """
        raise NotImplemented()


    def get_plotable_items(self):
        raise NotImplemented()

    def get_erroneous_entries(self):
        return_values = {}
        #todo: USE SOMETHING BETTER THAN SELF.ATTRIBUTES!!!!!
        for entry in self._attributes:
            if self.__rated_data[entry + ".state"]:
                #todo: is it guaranteed that __data and __rated_data is synced?
                if self.__rated_data[entry + ".state"][-1] is not "ok":
                    return_values[entry] = entry
                    return_values[entry + ".actual_value"] = self.__rated_data[entry + ".actual_value"]
                    return_values[entry + ".expected_value"] = self.__rated_data[entry + ".expected_value"]
                    return_values[entry + ".state"] = self.__rated_data[entry + ".state"]

        return return_values



self.delete_old_entries()
    # delete all entries older than 10 minutes

    # for all element that are older than 1 minute:
    # if an element has an error state keep this and the first entry who no longer has an error state