'''Created on Oct 20, 2015
@author: gaulth30'''
import copy,logging
from numpy import ndarray
#from types import NoneType
SET_EXTERNALLY = 0
CACHED = 1
LOG = logging.getLogger('IPCORE')
NoneType=type(None)
"""This file contains almost every object related to the raising of errors. These
objects are 'RestrictedClassError', 'DataTypeError', 'LowerBoundError', 
'UpperBoundError', 'ReadOnlyError', 'ElementUpperBoundError', 
'ElementLowerBoundError', 'ElementValueError', 'ElementTypeError', 
'DataValueError' and 'tst'."""
class RestrictedClassError(Exception):
    """Generic exception for FrozenClass."""
    def __init__(self, args):
        #constructor.
        #print "Stack trace within exception", traceback.extract_tb(sys.exc_info()[2])
        msg = args[0] % args[1]
        #call the constructor of the 'Exception' library.
        Exception.__init__(self, msg)
    #def __str__(self):
        #This method allows to return the error code and its explanation.
     #   return 'Error %d'%self.code + " - " + self.message
    #def __repr__(self):
        #This method allows to return the error code and its explanation.
     #   return "%s: %d - %s" % (self.__class__, self.code, self.message)
class DataTypeError(RestrictedClassError):
    """Wrong data type of value assigned to class attribute.
    Arguments:
        -arguments: a tuple with the following elements:
            -name of the class attribute.
            -type of the value that is being assigned.
            -(list of) allowed data type(s) for the attribute."""
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Wrong data type of value assigned to property %s. ",
               "Data type given: %s, data type(s) allowed: %s")
        self.code = 1001
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(DataTypeError, self).__init__((''.join(msg), args)) 
class LowerBoundError(RestrictedClassError):
    """Data value assigned to class attribute is below lower bound.
    Arguments:
        -arguments: a tuple with the following elements:
            -name of the class attribute.
            -value that is being assigned.
            -lower bound value for the attribute."""
    def __init__(self, args):
        #constructor
        # Call the base class constructor with the parameters it needs
        msg = ("Value assigned to property %s is below lower bound. ",
               "Value given: %s, Lower bound: %s")
        self.code = 1005
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(LowerBoundError, self).__init__((''.join(msg), args))
class UpperBoundError(RestrictedClassError):
    """Data value assigned to class attribute is beyond upper bound.
    Arguments:
        -arguments: a tuple with the following elements:
            -name of the class attribute.
            -value that is being assigned.
            -upper bound value for the attribute."""            
    def __init__(self, args):
        #constructor
        # Call the base class constructor with the parameters it needs
        msg = ("Value assigned to property %s is beyond upper bound. ",
               "Value given: %s, Upper bound: %s")
        self.code = 1006
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(UpperBoundError, self).__init__((''.join(msg), args))
class ReadOnlyError(RestrictedClassError):
    """Trying to assign to a read-only class attribute.
    Arguments:
        -arguments: a tuple with the following elements:
            -name of the class attribute."""
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Trying to assign to read-only property %s.")
        self.code = 1009
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(ReadOnlyError, self).__init__((''.join(msg), args))
class ElementUpperBoundError(RestrictedClassError):
    """The value of an element in an assignment to an iterable class attribute 
    is beyond the upper bound.
    Arguments:
        -arguments: a tuple with the following elements:
            -index of the element in the iterable.
            -name of the class attribute.
            -value that is being assigned.
            -upper bound value for elements in the attribute. """
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Value of element with index %d in iterable value assigned to ",
               "property %s is beyond upper bound. Value given: %s, upper ",
               "bound: %s.")
        self.code = 1008
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(ElementUpperBoundError, self).__init__((''.join(msg), args))
class ElementLowerBoundError(RestrictedClassError):
    """The value of an element in an assignment to an iterable class attribute 
    is below the lower bound.
    Arguments:
        -arguments: a tuple with the following elements:
            -index of the element in the iterable.
            -name of the class attribute.
            -value of the element in the iterable object.
            -lower bound value for elements in the attribute."""
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Value of element with index %d in iterable value assigned to ",
               "property %s is below lower bound. Value given: %s, lower ",
               "bound: %s.")
        self.code = 1007
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(ElementLowerBoundError, self).__init__((''.join(msg), args))
class ElementValueError(RestrictedClassError):
    """Wrong value of an element in an assignment to iterable class attribute.
    Arguments:
        -arguments: a tuple with the following elements:
            -index of the element in the iterable.
            -name of the class attribute.
            -type of the value that is being assigned.
            -allowed data type(s) for the attribute."""
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Wrong value of element with index %d in iterable value ",
               "assigned to property %s. Value given: %s, value(s) allowed: %s") 
        self.code = 1004
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(ElementValueError, self).__init__((''.join(msg), args))
class ElementTypeError(RestrictedClassError):
    """Wrong data type of an element in an assignment to iterable class
     attribute.
    Arguments:
        -arguments: a tuple with the following elements:
            -index of the element in the iterable.
            -name of the class attribute.
            -type of the element in the iterable that is being assigned.
            -(list of) allowed data type(s) for the elements in the iterable 
            attribute. """
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Wrong data type of element with index %d in iterable value ",
               "assigned to property %s. Data type given: %s, data type(s) ",
               "allowed: %s")
        self.code = 1003
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(ElementTypeError, self).__init__((''.join(msg), args))
class DataValueError(RestrictedClassError):
    """Wrong data value assigned to class attribute.
    Arguments:
        -arguments: a tuple with the following elements:
            -name of the class attribute.
            -value that is being assigned.
            -(list of) allowed value(s) for the attribute. """
    def __init__(self, args):
        #constructor.
        # Call the base class constructor with the parameters it needs
        msg = ("Wrong value assigned to property %s. ",
               "Value given: %s, value(s) allowed: %s")
        self.code = 1002
        #This line means that this class is a child of the 'RestrictedClassError' 
        #object so we can return correctly the error.
        super(DataValueError, self).__init__((''.join(msg), args))
class MixinIngredient(object):
    pass
class MetaMixinBowl(type):
    def mixin_first(self, mixin_class):
        if not mixin_class in self.__bases__:
            if self.__bases__ == (object,):
                self.__bases__ = (mixin_class,)
            else:
                self.__bases__ = (mixin_class,) + self.__bases__
    def mixin_last(self, mixin_class):
        if not mixin_class in self.__bases__:
            if self.__bases__ == (object,):
                self.__bases__ = (mixin_class,)
            else:
                self.__bases__ = self.__bases__ + (mixin_class,)
    #def mixin(self, mixin_class, first=True):
     #   if first:
      #      self.mixin_first(mixin_class)
       # else:
        #    self.mixin_last(mixin_class)
class MixinBowl(object):
    __metaclass__ = MetaMixinBowl
    pass
class RestrictionError(ValueError):
    def __init__(self, arg0):
        #constructor.
        ValueError.__init__(self, arg0)
class __PropertyRestriction__(MixinBowl):
    """ abstract base class for restrictions on property values """
    def __init__(self):
        #constructor.
        pass
    def __and__(self, other):
        if isinstance(other, __PropertyRestriction__):
            return __PropertyRestrictionAnd__(self, other)
        elif other is None:
            return self
        else:
            raise TypeError("Cannot AND __PropertyRestriction__ with %s" % type(other))
    def __iand__(self, other):
        C = self.__and__(other)
        self = C
        return self
    def __or__(self, other):
        if isinstance(other, __PropertyRestriction__):
            return __PropertyRestrictionOr__(self, other)
        elif other is None:
            return self
        else:
            raise TypeError("Cannot OR __PropertyRestriction__ with %s" % type(other))
    def __ior__(self, other):
        C = self.__and__(other)
        self = C
        return self
    def __invert__(self):
        return __PropertyRestrictionNot__(self)
    def __call__(self, value, obj=None):
        return self.validate(value, obj)
    def validate(self, value, obj=None):
        """ returns True if the value passes the restriction """
        return True
    def __repr__(self):
        return "Generic Restriction"
class __PropertyRestrictionAnd__(__PropertyRestriction__):
    def __init__(self, restriction1, restriction2):
        #constructor.
        self.restriction1 = restriction1
        self.restriction2 = restriction2
    def validate(self, value, obj=None):
        return self.restriction1(value, obj) and self.restriction2(value, obj)
    def __repr__(self):
        return "(%s and %s)" % (self.restriction1, self.restriction2)
class __PropertyRestrictionOr__(__PropertyRestriction__):
    def __init__(self, restriction1, restriction2):
        #constructor
        self.restriction1 = restriction1
        self.restriction2 = restriction2
    def validate(self, value, obj=None):
        return self.restriction1(value, obj) or self.restriction2(value, obj)
    def __repr__(self):
        return "(%s or %s)" % (self.restriction1, self.restriction2)
class __PropertyRestrictionNot__(__PropertyRestriction__):
    def __init__(self, restriction):
        #constructor
        self.restriction = restriction
    def validate(self, value, obj=None):
        return not self.restriction(value, obj)
    def __repr__(self):
        return "(not %s)" % (self.restriction)
class RestrictType(__PropertyRestriction__):
    """ restrict the type or types the argument can have. Pass a type or tuple of types """
    def __init__(self, allowed_types):
        #constructor
        self.allowed_types = ()
        self .__types_set = False
        self.__add_type__(allowed_types)
        if not self.__types_set:
            raise ValueError("allowed_typed of Type Restriction should be set on initialization")
    def __add_type__(self, type_type):
        if isinstance(type_type, type):
            self.allowed_types += (type_type,)
            self .__types_set = True
        elif isinstance(type_type, (tuple, list)):
            for T in type_type:
                self.__add_type__(T)
        else:
            raise TypeError("Restrict type should have a 'type' or 'tuple' of types as argument")
    def validate(self, value, obj=None):
        return isinstance(value, self.allowed_types)
    def __repr__(self):
        return "Type Restriction:" + ",".join([T.__name__ for T in self.allowed_types])
RESTRICT_STRING = RestrictType(str)
class IpcoreException(Exception):
    def __init__(self, Msg):
        #constructor
        super(IpcoreException, self).__init__(Msg)
class IpcoreAttributeException(IpcoreException):
    """Exception with attributes """
    def __init__(self, Msg):
        #constructor
        super(IpcoreAttributeException, self).__init__(Msg)
class IpcorePropertyDescriptorException(IpcoreAttributeException):
    """General Exception with property descriptors"""
    def __init__(self, Msg):
        #construction
        super(IpcorePropertyDescriptorException, self).__init__(Msg)
class __BasePropertyDescriptor__(object):
    """ base class for property descriptors """
    __allowed_keyword_arguments__ = ["required"]
    def __init__(self, **kwargs):
        #constructor
        self.required = False
        self.__allowed_keyword_arguments__.append("doc")
        if "doc" in kwargs:
            self.__doc__ = kwargs["doc"]
            kwargs.pop("doc")
        else:
            self.__doc__ = ""
        for (k, v) in kwargs.items():
            if k in self.__allowed_keyword_arguments__:
                object.__setattr__(self, k, v)
            else:
                raise IpcorePropertyDescriptorException("Argument '%s' is not valid for %s" % (k, self))
    def bind_to_class(self, cls, name):
        pass
    def validate_on_binding(self, host_cls, name):
        return True
class ProcessorException(IpcoreException):
    pass
class PropertyProcessor(object):
    """ processes a value before it is passed as a property """
    def __init__(self):
        #constructor
        pass
    def __add__(self, other):
        if isinstance(other, PropertyProcessor):
            return __CompoundPropertyProcessor__([self, other])
        elif other is None:
            return self
        else:
            raise ProcessorException("Cannot add %s to PropertyProcessor " \
                                     % type(other))
    def __iadd__(self, other):
        C = self.__add__(other)
        self = C
        return self
    def __call__(self, value, obj=None):
        return self.process(value, obj)
    def process(self, value, obj=None):
        return value
    def __repr__(self):
        return "<Property Processor >"
class __CompoundPropertyProcessor__(PropertyProcessor):
    """ compound property processor class """
    def __init__(self, processors=[]):
        #constructor
        self.__sub_processors = processors
    def __add__(self, other):
        if isinstance(other, __CompoundPropertyProcessor__):
            return __CompoundPropertyProcessor__(self.__sub_processors + other.__sub_processors)
        elif isinstance(other, PropertyProcessor):
            return __CompoundPropertyProcessor__(self.__sub_processors + [other])
        else:
            raise ProcessorException("Cannot add %s to PropertyProcessor" % type(other))
    def __iadd__(self, other):
        if isinstance(other, __CompoundPropertyProcessor__):
            self.__sub_processors += other.__sub_processors
            return self
        elif isinstance(other, PropertyProcessor):
            self.__sub_processors += [other]
            return self
        else:
            raise ProcessorException("Cannot add %s to PropertyProcessor" % type(other))
    def process(self, value, obj=None):
        """ processes the value """
        v = value
        for R in self.__sub_processors:
            v = R.process(self, value, obj)
        return v
    def __repr__(self):
        S = "< Compound Property Processor:"
        for i in self.__sub_processors:
            S += "   %s" % i.__repr__()
        S += ">"
        return S
class RestrictNothing(__PropertyRestriction__):
    """ no restriction on the property value """
    def __add__(self, other):
        if isinstance(other, __PropertyRestriction__):
            return copy.copy(other)
        else:
            raise TypeError("Cannot add %s to __PropertyRestriction__" % type(other))
    def __iadd__(self, other):
        self = copy.copy(other)
        return self
    def __repr__(self):
        return "No Restriction"
class DefinitionProperty(__BasePropertyDescriptor__):
    __allowed_keyword_arguments__ = ["required", "default", "locked", 
                                     "preprocess", "allow_none", 
                                     "fdef_name", "restriction"]
    def __init__(self, internal_member_name=None, **kwargs):
        #constructor
        self.__name__ = internal_member_name
        self.name = internal_member_name
        # initialize with default values
        self.locked = False
        self.allow_none = False
        self.preprocess = PropertyProcessor()
        self.restriction = RestrictNothing()
        __BasePropertyDescriptor__.__init__(self, **kwargs)
        if ("fdef_name" not in kwargs):
            if ("default" not in kwargs):
                if ((("allow_none" not in kwargs) or (not kwargs["allow_none"]))
                    and (("required" in kwargs) and (not kwargs["required"]))):
                        raise IpcorePropertyDescriptorException("Property is \
                        specified as required='False', but should then have \
                        either a 'default' OR an 'fdef_name' OR be set to \
                        'allow_none'")
            else:
                if (("required" in kwargs) and (kwargs["required"])):
                    raise IpcorePropertyDescriptorException("Property is \
                    specified as both required='True' and having a default : \
                    this is not allowed !")
            self.fdef_name = None
        else:
            if ("default" in kwargs):
                raise IpcorePropertyDescriptorException("Property has both a \
                'default' specified and an 'fdef_name' : this is not allowed !")
            if ("required" in kwargs) and (kwargs["required"]):
                raise IpcorePropertyDescriptorException("Property is both \
                specified as 'required' and having an 'fdef_name' : this is not\
                 allowed !")
    #def __get_default__(self):
     #   import inspect
      #  if inspect.isroutine(self.default):
       #     return self.default()
        #else:
         #   return self.default
    def __externally_set_property_value_on_object__(self, obj, value):  
        # FIXME : add subscribe new value / unsubscribe old value
        clear_cached_values_in_store = True
        if self.__value_was_stored__(obj):
            old_value = obj.__store__[self.__name__][0]
            try:
                clear_cached_values_in_store = (type(old_value) != type(value)) or (old_value != value)
                if type(clear_cached_values_in_store) == ndarray:
                    clear_cached_values_in_store = clear_cached_values_in_store.all()
            except ValueError:  
                ''' precaution... if exceptionally this would occur because the 
                comparison between old_value and value cannot be done, then 
                clear caches anyway...'''
                clear_cached_values_in_store = True
        obj.__store__[self.__name__] = (value, SET_EXTERNALLY)
        if not(obj.flag_busy_initializing):
            obj.__do_validation__()
            if (clear_cached_values_in_store):
                obj.__clear_cached_values_in_store__()
    def __get_property_value_origin__(self, obj):
        (value, origin) = obj.__store__[self.__name__]
        return origin
    def __get_property_value_of_object__(self, obj):
        return obj.__store__[self.__name__][0]
    def __value_was_stored__(self, obj):
        return (self.__name__ in obj.__store__)
    def __get__(self, obj, type=None):
        '''Check if a value was set by the user : in that case, return the 
        value, otherwise invoke the getter function to retrieve the value'''
        if obj is None:
            return self
        #check if a value was set by the user
        if (not self.__value_was_stored__(obj)):
            '''no value was set in the store by the user, return the value 
            calculated by the getter-function
            if there a getter-method ?'''
            f = self.__get_getter_function__(obj)
            if (f is None):
                #is there a default ?
                if hasattr(self, "default"):
                    value = self.preprocess(self.__get_default__(), obj)
                else:
                    #no default and no getter method
                    value = None
            else:
                #there is a getter method and no locally stored value
                value = self.__call_getter_function__(obj)
            #check if the value is compatible with the property's restriction
            if (not self.restriction(value, obj)):
                if (value is None):
                    if (not self.allow_none):
                        raise IpcorePropertyDescriptorException("Cannot set \
                        property '%s' of '%s' to None." % (self.name, 
                                                        obj.__class__.__name__))
                else:
                    raise IpcorePropertyDescriptorException("Cannot set value \
                    '%s' to property '%s' of '%s' because it is incompatible \
                    with the restriction %s of the property." % (str(value), 
                    self.name, obj.__class__.__name__, str(self.restriction)))
            return value
        else:
            stored_value = self.__get_property_value_of_object__(obj)
            return stored_value
    def __get_getter_function__(self, obj):
        if (self.fdef_name is None):
            if hasattr(self, "autogenerated_fdef_name") and hasattr(obj, 
                                            self.autogenerated_fdef_name):
                result = getattr(obj, self.autogenerated_fdef_name)
                return result
            else:
                return None
        else:
            return getattr(obj, self.fdef_name)
    def __check_restriction__(self, obj, value):
            #check if the value is compatible with the restriction
            if self.restriction(value, obj) or (self.allow_none and value is None):
                return True
            else:
                raise IpcorePropertyDescriptorException("Invalid assignment for\
                 Property '%s' of '%s' with value %s: not compatible with \
                 restriction %s." % (self.name, obj.__class__.__name__, 
                                     str(value), str(self.restriction)))
    def __cache_property_value_on_object__(self, obj, value):
        if (type(obj) != NoneType):
            new_value = self.preprocess(value, obj)
            self.__check_restriction__(obj, new_value)
            obj.__store__[self.__name__] = (new_value, CACHED)
            return new_value
        else:
            return value
    def __call_getter_function__(self, obj):
        f = self.__get_getter_function__(obj)
        value = f()
        new_value = self.__cache_property_value_on_object__(obj, value)
        return new_value
    #def __set__(self, obj, value):
     #   if self.locked:
      #      raise IpcorePropertyDescriptorException("Cannot assign to locked \
       #     property '%s' of '%s'" % (self.name, type(obj).__name__))
        #if (self.preprocess != None):
         #   try:
          #      new_value = self.preprocess(value, obj)
           # except ProcessorException,e:
            #    LOG.info("RestrictedProperty::__set__ : an error was raised on \
             #   self.preprocess : %s" % str(e))
              #  if (value is None) and not self.allow_none:
               #     raise IpcorePropertyDescriptorException("Invalid assignment \
                #    for property '%s' of '%s' with value %s" % (self.name, 
                 #               type(obj).__name__, str(value)))
                #new_value = value
#        else:
 #           new_value = value
  #      self.__check_restriction__(obj, new_value)
   #     self.__externally_set_property_value_on_object__(obj, new_value)
    def bind_to_class(self, cls, name):
        self.name = name
        if (not hasattr(self, "__name__")) or (self.__name__ is None):
            self.__name__ = "__prop_%s__" % name
    def validate_on_binding(self, host_cls, name):
        # autogenerate the name of the fdef-function if it was not set
        if (self.fdef_name is None):
            self.autogenerated_fdef_name = "define_" + name
        #derive "required" automatically
        if (not hasattr(self, "default")) and ((self.fdef_name is None) and \
                        (not hasattr(host_cls, self.autogenerated_fdef_name))):
            if (not hasattr(self, "allow_none")) or (not self.allow_none):
                if (not self.locked):
                    self.required = True
        #if (hasattr(self, "default")) and (self.default is None) and \
        #(not hasattr(self, "allow_none") or not self.allow_none):
         #   self.allow_none = True
class PropertyDescriptor(DefinitionProperty):
    pass
    # now just a placeholder for backwards compatibility
class RestrictedProperty(PropertyDescriptor):
    pass
    #now just a placeholder for backwards compatibility
def StringProperty(internal_member_name=None, restriction=None, **kwargs):
    R = RESTRICT_STRING & restriction
    return RestrictedProperty(internal_member_name, restriction=R, **kwargs)