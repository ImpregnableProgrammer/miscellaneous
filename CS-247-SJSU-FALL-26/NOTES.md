# 9-1-26
* RAM->cache mappings (assume 32 bit addresses for RAM, 16 bits for cache):
  * Fully-Associative: entries from memory can go anywhere in cache, with placement dictated by replacement policy for which entries are to be evicted (in full cache) or next available spot (in non-full cache). Address mapping is: TAG section (first several bits) for identifying entry, and block-offset for location in chosen block.
  * Direct-Mapped: Same memory locations (blocks) for multiple entries: TAG used to identify, index bits used to identify block to map to, and offset for location within block
  * N-way set associative: Multiple blocks per set: TAG for identifying, index for set, and place in block that is available or needs to be replaced

# 9-3-26
* Virtual Addresses
  * Pros: Performance since no address translation required for cache access since no TAG but only virtual index sued to obtain entry;
  * Cons: No way to enforce process isolation for memory access since virtual address space shared by all processes; wasteful if writes happen when multiple processes (with different ASID (address space ID, same as PID)) sharing same resource in physical memory
* Physical Addresses
  * Same as first pros & cons of virtual addresses, but reversed
  * Pros: Can enforce process isolation easily across physical address boundaries
  * Cons: Address translation required for TAG usage -> performance hit
* Memory types
  * SRAM (static random access memory): Volatile (loses data upon power loss) & more expensive, but FAST (6 transisters per bit, NO CAPACITORS (hence volatile)); can be periodically refreshed (i.e. read + rewrite to prevent corruption due to current leakage from capacitors in flip-flop) although can be avoided as long as powered (due to gated transistor structure arising from greater transistor usage, which increases cost and hence limits capacity/dollar)
  * DRAM (dynamic random access memory): Volatile but cheaper, but SLOWER (1 transister + capactor per bit in FLOP); must be periodically refreshed (to prevent capacitor state loss from current leakage, so must read + rewrite data periodically, and fewer transistors 
  * SDRAM (synchronous dynamic random access memory) -> synchronized with system clock
* Flash Memory
  * Non-volatility implemented using gated transister with dielectric that can maintain charge for LOOOONG time (on scale of 14k years) that must be broken with high voltage (12V typically), and once cell has dielectric broken, different cell with dielectric must be used (which is what limits durability of flash memory, i.e. limited reads and writes, and flash memory is gone once all cells depleted this way)

# 9-8-26
* Cache victim buffer - buffer where successive cache access results are written to, and then buffer fluished once certain limit reached. Helps reduce latency since programs don't have to wait for successive access results sequentially - increases asyncronicity.
* Cache write buffer - Successive write requests written to this and then all flushed and completed at once once a certain limit is reached.
* For non-blocking caches, can use Miss Status Holding Register (MSHR)
* Critical word first on cache request - makes sense only with early restart, but early restart can be implemented without critical word first

# 9-10-26
* Virtual memory -- works by translating virtual addresses to physical addresses using page table stored at known physical address in RAM (thus every logical memory access is actually TWO real memory accesses - one for page table to get physical address translation, then another to get data from physical address (either in RAM (cache for hard disk) or on the hard disk which has MAX latency/miss penalty)). TLB (translation lookaside buffer) stores commonly translated addresses in smaller but faster-to-access space to save one RAM access in cases where there's a hit.
  * Virtual memory helps by having memory isolation between processes with page boundaries that limit one process from access another process's physical memory pool.
  * Also allows process to see more memory availability than it might actually have (64 bit virtual memory address -> 2^64 memory entries. Parts used for offset, others for virtual memory number) since memory shared in one place between caches, HBM (high-bandwidth memory -> basically like L4 cache), RAM and hard disk
  * Won't use ALL 64 bits even though that many bits are available - more like 48 out of 64
* Virtual Machines - two types: one where hypervisor runs as separate application on top of host OS in the user space, another where hypervisor runs directly on top of the hardware (as the host OS essentially) and controls several guest OS's
  * Multiple modes in modern architecture - application/user mode, supervisor mode, hypervisor mode, and machine (hardware) modes
  * Virtual Machine Monitor handles emulation/fundamental processes/address translations and flushing TLB (which could hold incorrect translations for same virtual addresses shared by different processes/OS's) as guest OS's are swapped between
  * Shadow page table used for virtual machine virtual address translations

# 9-15-26 (MISSED CLASS :'( )

# 9-17-26
* For out-of-order (OOO) execution using Tomasulo's algorithm to handle WAW and WAR (Write-after-write and Read-after-Write) hazards, instructions are each given a data spot in the FIFO ReOrder Buffer (ROB) and until its operands (inputs) are ready, and are given a Reservation Station number (RS#) and spot in the RS for each operand/pipeline stage and the Common Data Bus (CDB) is monitored by RS for the RS# to appear letting system know corresponding operand is ready. Limited number of spots per RS with instructions beyond corresponding RS's capacity being blocked until one instruction in RS completes.
  * Each operand station (pipeline stage/unit, such as ALU) has its own RS
  * Once operands are ready as signaled by RS# and the data value pairs for the instruction, instructions are executed from RS's in the order data values are ready (either from other instructions or source registers) with instructions being able to bypass each pther as needed (but loads not bypassing stores and vice-versa for load/store stage with one RS)
  * OOO different from in-order pipeline execution since only ways to compensate for hazards in in-order pipelines is by stalling, which stalls WHOLE pipeline!!
  * Each destination/spource register (such as x1, f1, x2, f2, etc) will contain RS station number until operation for it finished and committed to ROB

# 9-22-26
* TOMASULO'S ALGORITHM: For ROB, space for instructions allocated in order of instructions, results written as instructions complete and bypass one another, but then results committed/written to register files and taken up by dependent entries in RS's from ROB in order of instructions during commit step to avoid instructional hazards in out-of-order execution
  * ROB holds result of instruction between completion and commit, then results committed to register files in order of instructions. ROB has 4 fields: Instruction type (branch, store, or write to register -- to know what action to take at commit time), destination field (register number), oputput value, ready field (whether execution completed for instruction), and busy field (whether ROB entry is taken/still waiting on result)
  * RS stores for each instruction -- Optype, and for each operand: whether it's ready, and its value
  * Results then written to Reservation Station (RS) instruction entries that are potentially waiting on it as an operand 
    * Until instruction complete, dependent entries in RS store decoded instruction along with ROB entry #'s for operands needed that aren't available yet -- then when data comes along with matching ROB # on CDB, value written to RS entry as operand, and once all operands available, instruction in RS entry executes
* Issue (Allocate RS and ROB entries for instruction -- separate RS with multiple spots per operaation "station"), Execute (begin execution from RS once operands are available), Write result (write result and ROB # (or tag) to ROB), and Commit (once entry reaches head of FIFO ROB, send data on CDB, or flush all entries if instruction is result of misprediction now resolved)
  * On branch misprediction, speculative entries in ROB are flushed
  * Register and memory values NOT written until commit step!
  * Once instruction reaches head of ROB for commit step, result written to register file AND dependent RS entry(ies) as necessary (using comparator at RS level to see whether missing operand is on CDB). Data is NOT read from ROB only since entries "removed" from ROB once they reach the head
* To show Tomasulo's algorithm execution state in any one state of instructions in pipeline, need 3 tables: One for ROB state & entries, one for RS stations and entries (each RS station denoted by OP + #, e.g. ADD1, ADD2, MULT1, MULT2), and one for register file & entries
* To achieve CPI < 1, need to complete multiple instructions per clock (multiple issue)
  * Solutions: statically scheduled superscaler processors, VLIW (very long instruction word) processors, or Dynamically scheduled superscaler processors

# 9-24-26
* MAC instructions used heavily in multiple issue -- "A Multiply-Accumulate (MAC) instruction in digital signal processing (DSP) computes the product of two numbers and adds that result to an accumulator register in a single clock cycle (A = A + x × y)."
*
