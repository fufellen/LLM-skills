# Robust per-testbench ModelSim .do template (ModelSim ASE 10.5b).
# Usage examples:
#   vsim.exe -batch -logfile logs/tb.log -do "do run_tb.do; quit -f"
#   vsim.exe -c -do "do run_tb.do"            ;# interactive console
#   GUI Transcript: do run_tb.do              ;# waves loaded via wave.do
# Parameters come from the environment (set in PowerShell):
#   $env:TB_FILE  - path to the testbench .sv
#   $env:RUN_FOR  - run duration, e.g. "9 ms" (default: -all)

# --- error handling: MUST precede any run command --------------------------
onerror {quit -code 1}
onElabError {quit -code 12}
onbreak {resume}

# --- parameters ------------------------------------------------------------
if {[info exists env(TB_FILE)]} {
    set path_file_tb $env(TB_FILE)
} else {
    set path_file_tb C:/workspace/verilog/src/<...>/<tb_name>.sv
}
set module_name_tb [file rootname [file tail $path_file_tb]]

# --- fresh work library ----------------------------------------------------
if {[file exists work]} {
    vdel -lib work -all
}
vlib work
vmap work work

# --- compile (add -incr when passing a stable multi-file list) -------------
vlog -sv -incr $path_file_tb

# --- elaborate -------------------------------------------------------------
vsim -t 1ns -voptargs="+acc" $module_name_tb

# --- log everything for post-mortem debugging ------------------------------
# Memories/large arrays are excluded by default; adjust WildcardFilter if needed.
add log -r /*

# --- GUI-only part ---------------------------------------------------------
if {![batch_mode]} {
    if {[file exists wave.do]} { do wave.do }
}

# --- run -------------------------------------------------------------------
if {[info exists env(RUN_FOR)]} {
    run $env(RUN_FOR)
} else {
    run -all
}

# In batch runs the caller appends "; quit -f"; in GUI the session stays open.
