# -*- coding: utf-8 -*-

"""
Ftrace built-in backend.
"""

__author__     = "Eiichi Tsukata <eiichi.tsukata.xh@hitachi.com>"
__copyright__  = "Copyright (C) 2013 Hitachi, Ltd."
__license__    = "GPL version 2 or (at your option) any later version"

__maintainer__ = "Stefan Hajnoczi"
__email__      = "stefanha@redhat.com"


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
    out('#include "trace/ftrace.h"',
        '')


def generate_h(event, group):
    argnames = ", ".join(event.args.names())
    if len(event.args) > 0:
        argnames = ", " + argnames

    out('    if (trace_event_get_state(%(event_id)s)) {',
        '        ftrace_write("%(name)s " %(fmt)s "\\n" %(argnames)s);',
        '    }',
        name=event.name,
        event_id="TRACE_" + event.name.upper(),
        fmt=event.fmt.rstrip("\n"),
        argnames=argnames)


def generate_h_backend_dstate(event, group):
    out('    trace_event_get_state_dynamic_by_id(%(event_id)s) || \\',
        event_id="TRACE_" + event.name.upper())


def generate_rs(event, group):
    out('        let format_string = c"%(fmt)s";',
        fmt=event.rust_format_string(event.fmt.rstrip("\n")))
    out('        unsafe {ftrace_write(format_string.as_ptr() as *const c_char, %(args)s);}',
            args=convert_rust_args_to_ffi(event.rust_args))
