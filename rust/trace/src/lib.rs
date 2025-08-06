#[allow(unused_macros)]
#[macro_export]
macro_rules! include_trace {
    ($name:literal) => {
        include!(concat!(env!("MESON_BUILD_ROOT"), "/trace/", $name, ".rs"));
    };
}
