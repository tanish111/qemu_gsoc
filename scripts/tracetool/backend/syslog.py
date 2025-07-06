# -*- coding: utf-8 -*-

"""
Syslog built-in backend.
"""

__author__     = "Paul Durrant <paul.durrant@citrix.com>"
__copyright__  = "Copyright 2016, Citrix Systems Inc."
__license__    = "GPL version 2 or (at your option) any later version"

__maintainer__ = "Stefan Hajnoczi"
__email__      = "stefanha@redhat.com"


<<<<<<< HEAD
=======
import os.path
import re
>>>>>>> d28aa5e4b5 (Syslog Support)
from tracetool import out


PUBLIC = True

rust_to_ffi_type_map = {
    # Signed integers
    "int": "c_int",                 # i32
    "short": "c_short",             # i16
    "long": "c_long",               # platform-dependent (i32/i64)
    "long long": "c_longlong",      # i64

    # Unsigned integers
    "unsigned int": "c_uint",             # u32
    "unsigned short": "c_ushort",         # u16
    "unsigned long": "c_ulong",           # platform-dependent
    "unsigned long long": "c_ulonglong",  # u64

    # Fixed-width types
    "int8_t": "c_schar",   # i8 (not variadic-safe, will promote)
    "uint8_t": "c_uchar",  # u8 (not variadic-safe, will promote)
    "int16_t": "c_short",  
    "uint16_t": "c_ushort",
    "int32_t": "c_int",    
    "uint32_t": "c_uint",  
    "int64_t": "c_longlong",
    "uint64_t": "c_ulonglong",

    # Floating-point
    "float": "c_float",
    "double": "c_double",

    # Boolean (C99)
    "bool": "c_int",  # Usually _Bool

    # Character
    "char": "c_char",               # signed or unsigned platform-dependent
    "const char *": "*const c_char",
    "char *": "*mut c_char",

    # Void pointers
    "void *": "*mut c_void",
    "const void *": "*const c_void",

    # Size type
    "size_t": "size_t",

    # Unsigned shorthand
    "unsigned": "c_uint"
}
def convert_rust_args_to_ffi(arg_str):
    args = [a.strip() for a in arg_str.split(",")]
    converted = []

    for arg in args:
        if not arg:
            continue
        name, rust_type = [x.strip() for x in arg.split(":")]
        ffi_type = rust_to_ffi_type_map.get(rust_type)
        if not ffi_type:
            ffi_type = rust_type
        converted.append(f"{name} as {ffi_type}")
    return ", ".join(converted)

def generate_h_begin(events, group):
    out('#include <syslog.h>',
        '')


def generate_h(event, group):
    argnames = ", ".join(event.args.names())
    if len(event.args) > 0:
        argnames = ", " + argnames

    cond = "trace_event_get_state(%s)" % ("TRACE_" + event.name.upper())

    out('    if (%(cond)s) {',
        '#line %(event_lineno)d "%(event_filename)s"',
        '        syslog(LOG_INFO, "%(name)s " %(fmt)s %(argnames)s);',
        '#line %(out_next_lineno)d "%(out_filename)s"',
        '    }',
        cond=cond,
        event_lineno=event.lineno,
        event_filename=event.filename,
        name=event.name,
        fmt=event.fmt.rstrip("\n"),
        argnames=argnames)

def generate_rs(event, group):
    out('let format_string = c"%(fmt)s"',
        fmt=event.rust_format_string(event.fmt.rstrip("\n")))
    out('unsafe {syslog(LOG_INFO, format_string.as_ptr() as *const c_char, %(args)s);}',
            args=convert_rust_args_to_ffi(event.rust_args))

def generate_h_backend_dstate(event, group):
    out('    trace_event_get_state_dynamic_by_id(%(event_id)s) || \\',
        event_id="TRACE_" + event.name.upper())
