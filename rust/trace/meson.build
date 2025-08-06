rust = import('rust')

_trace_rs = static_library(
  'trace',             # Library name,
  'src/lib.rs',
  trace_rs_targets,         # List of generated `.rs` custom targets
  override_options: ['rust_std=2021', 'build.rust_std=2021'],
  rust_abi: 'rust',
  dependencies : [libc_rs,qemuutil_rs],        # Add any necessary Rust dependencies if needed
)

trace_rs = declare_dependency(link_with: _trace_rs)
