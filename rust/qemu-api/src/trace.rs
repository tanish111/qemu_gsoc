use std::ffi::c_char;

#[repr(C)]
pub struct TraceEvent {
    pub id: u32,
    pub name: *const c_char, 
    pub sstate: bool,        
    pub dstate: u16,
}

extern "C" {
    static _TRACE_PARALLEL_IOPORT_READ_EVENT: TraceEvent;
    static _TRACE_PARALLEL_IOPORT_READ_DSTATE: u16;
    static _TRACE_PARALLEL_IOPORT_READ_ENABLED: bool;
    static trace_events_enabled_count: u32;
}

const TRACE_PARALLEL_IOPORT_READ_ENABLED: bool = true;

fn main(){

}
