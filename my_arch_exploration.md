# Arch Linux Exploration

- [Arch Linux Exploration](#arch-linux-exploration)
  - [Rootless Docker setup](#rootless-docker-setup)
  - [Zram and Zswap](#zram-and-zswap)
  - [Linux swappiness](#linux-swappiness)
  - [Disk partitioning and memory swap setup](#disk-partitioning-and-memory-swap-setup)
  - [Setting up hibernation in Arch](#setting-up-hibernation-in-arch)
  - [Kernel parameters and Disk/filesystem stats](#kernel-parameters-and-diskfilesystem-stats)
  - [Block/character special files](#blockcharacter-special-files)
  - [Disk encryption](#disk-encryption)
  - [Git commit signing using `gpg` and how key pairs work](#git-commit-signing-using-gpg-and-how-key-pairs-work)
  - [Modifying `sudo` and `PAM` behavior](#modifying-sudo-and-pam-behavior)
  - [Using the Arch User Repository (AUR)](#using-the-arch-user-repository-aur)
  - [Querying GPU/CPU stats](#querying-gpucpu-stats)

## Rootless Docker setup
Set up `rootless` Docker on Linux (so each user can have their own instance of the Docker daemon running, which provides better container isolation): https://docs.docker.com/engine/security/rootless/ \
This utilizes Docker contexts, which basically allows for switching the active docker daemon using `docker context`: https://docs.docker.com/engine/context/working-with-contexts/ \
Make sure to follow https://docs.docker.com/engine/security/rootless/#limiting-resources in order to set up proper Linux cgroup (control group: https://docs.docker.com/config/containers/runmetrics/) resource limiting and `docker stats` tracking!

## Zram and Zswap
Looking for all `zram` related files - results of `find / -iregex .*zram.* 2>/dev/null`\
(`zram` is basically a zlib compressed, in-RAM storage space that can be used for swap or extra storage space. Look up `zram` on the Arch wiki for more information)
```
/home/rohan/.local/share/docker/overlay2/44f1a6f044052f6b992504d9067770cc74daaae1555de49041fec1e01e763793/diff/usr/sbin/zramctl
/home/rohan/.local/share/docker/overlay2/44f1a6f044052f6b992504d9067770cc74daaae1555de49041fec1e01e763793/diff/usr/share/bash-completion/completions/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/ubuntu12_64/steam-runtime-sniper/sniper_platform_0.20240307.80401/files/sbin/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/ubuntu12_64/steam-runtime-sniper/sniper_platform_0.20240307.80401/files/share/bash-completion/completions/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/ubuntu12_64/steam-runtime-sniper/var/tmp-B436L2/usr/sbin/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/ubuntu12_64/steam-runtime-sniper/var/tmp-B436L2/usr/share/bash-completion/completions/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/sniper_platform_0.20240307.80401/files/sbin/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/sniper_platform_0.20240307.80401/files/share/bash-completion/completions/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/var/tmp-0GA8L2/usr/sbin/zramctl
/home/rohan/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/var/tmp-0GA8L2/usr/share/bash-completion/completions/zramctl
/home/rohan/zram_file_search
/var/cache/pacman/pkg/zram-generator-1.1.2-1-x86_64.pkg.tar.zst
/var/cache/pacman/pkg/zram-generator-1.1.2-1-x86_64.pkg.tar.zst.sig
/var/lib/pacman/local/zram-generator-1.1.2-1
/var/lib/pacman/local/zram-generator-1.1.2-1/mtree
/var/lib/pacman/local/zram-generator-1.1.2-1/desc
/var/lib/pacman/local/zram-generator-1.1.2-1/files
/var/lib/flatpak/runtime/org.freedesktop.Platform/x86_64/23.08/8d036b0bd06ae893ffab1149b2fa036b8d0a6c3947906de00e6859f681bd16b0/files/bin/zramctl
/var/lib/flatpak/runtime/org.freedesktop.Platform/x86_64/23.08/8d036b0bd06ae893ffab1149b2fa036b8d0a6c3947906de00e6859f681bd16b0/files/share/bash-completion/completions/zramctl
/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/46/b6d2adc1f5a0a7ee4900120df526a4496449e9a798062b23cbedd28372d6d094/files/bin/zramctl
/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/46/b6d2adc1f5a0a7ee4900120df526a4496449e9a798062b23cbedd28372d6d094/files/share/bash-completion/completions/zramctl
/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/44/03d58bd67a3f2f54f02fb04cf46543e820d1b4b4c0ceb44271edd4224d3bad2a/files/bin/zramctl
/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/44/03d58bd67a3f2f54f02fb04cf46543e820d1b4b4c0ceb44271edd4224d3bad2a/files/share/bash-completion/completions/zramctl
/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/45/e66d066758b2a7b50a1cac032041fc1569c428f7cff988dcba554b3c035a191d/files/bin/zramctl
/var/lib/flatpak/runtime/org.gnome.Platform/x86_64/45/e66d066758b2a7b50a1cac032041fc1569c428f7cff988dcba554b3c035a191d/files/share/bash-completion/completions/zramctl
/var/lib/flatpak/runtime/org.kde.Platform/x86_64/6.6/d9a07ad16df6b5858f924014ae6bc0803035276bd317da79e4a36bae2f68790b/files/bin/zramctl
/var/lib/flatpak/runtime/org.kde.Platform/x86_64/6.6/d9a07ad16df6b5858f924014ae6bc0803035276bd317da79e4a36bae2f68790b/files/share/bash-completion/completions/zramctl
/var/lib/flatpak/runtime/org.freedesktop.Sdk/x86_64/22.08/5e230002750b20fbb628d1154b95aba1a4ede0c08f36e71cbca19ae6452be500/files/bin/zramctl
/var/lib/flatpak/runtime/org.freedesktop.Sdk/x86_64/22.08/5e230002750b20fbb628d1154b95aba1a4ede0c08f36e71cbca19ae6452be500/files/share/bash-completion/completions/zramctl
/var/lib/flatpak/.removed/org.freedesktop.Platform-a27ac639f80307e4b70c135012b7e2f1e74b17a4bb11b1ae7e15aae7d24f1879/files/bin/zramctl
/var/lib/flatpak/.removed/org.freedesktop.Platform-a27ac639f80307e4b70c135012b7e2f1e74b17a4bb11b1ae7e15aae7d24f1879/files/share/bash-completion/completions/zramctl
/dev/zram0
/run/udev/data/+module:zram
/run/systemd/units/invocation:systemd-zram-setup@zram0.service
/run/systemd/units/invocation:dev-zram0.swap
/run/systemd/generator/systemd-zram-setup@zram0.service.d
/run/systemd/generator/systemd-zram-setup@zram0.service.d/bindings.conf
/run/systemd/generator/dev-zram0.swap
/run/systemd/generator/swap.target.wants/dev-zram0.swap
/etc/systemd/zram-generator.conf
/sys/kernel/btf/zram
/sys/kernel/debug/zram
/sys/kernel/debug/zram/zram0
/sys/kernel/debug/zram/zram0/block_state
/sys/kernel/debug/shrinker/mm-zspool:zram0-43
/sys/kernel/debug/shrinker/mm-zspool:zram0-43/scan
/sys/kernel/debug/shrinker/mm-zspool:zram0-43/count
/sys/kernel/debug/zsmalloc/zram0
/sys/kernel/debug/zsmalloc/zram0/classes
/sys/kernel/debug/block/zram0
/sys/kernel/debug/printk/index/zram
/sys/class/block/zram0
/sys/class/zram-control
/sys/class/zram-control/hot_remove
/sys/class/zram-control/hot_add
/sys/devices/virtual/block/zram0
/sys/devices/virtual/block/zram0/uevent
/sys/devices/virtual/block/zram0/ext_range
/sys/devices/virtual/block/zram0/mm_stat
/sys/devices/virtual/block/zram0/range
/sys/devices/virtual/block/zram0/recompress
/sys/devices/virtual/block/zram0/backing_dev
/sys/devices/virtual/block/zram0/alignment_offset
/sys/devices/virtual/block/zram0/diskseq
/sys/devices/virtual/block/zram0/writeback_limit_enable
/sys/devices/virtual/block/zram0/power
/sys/devices/virtual/block/zram0/power/runtime_active_time
/sys/devices/virtual/block/zram0/power/runtime_status
/sys/devices/virtual/block/zram0/power/autosuspend_delay_ms
/sys/devices/virtual/block/zram0/power/runtime_suspended_time
/sys/devices/virtual/block/zram0/power/control
/sys/devices/virtual/block/zram0/reset
/sys/devices/virtual/block/zram0/mem_limit
/sys/devices/virtual/block/zram0/comp_algorithm
/sys/devices/virtual/block/zram0/dev
/sys/devices/virtual/block/zram0/holders
/sys/devices/virtual/block/zram0/bd_stat
/sys/devices/virtual/block/zram0/ro
/sys/devices/virtual/block/zram0/mem_used_max
/sys/devices/virtual/block/zram0/stat
/sys/devices/virtual/block/zram0/events_poll_msecs
/sys/devices/virtual/block/zram0/writeback
/sys/devices/virtual/block/zram0/writeback_limit
/sys/devices/virtual/block/zram0/events_async
/sys/devices/virtual/block/zram0/compact
/sys/devices/virtual/block/zram0/queue
/sys/devices/virtual/block/zram0/queue/io_poll_delay
/sys/devices/virtual/block/zram0/queue/max_integrity_segments
/sys/devices/virtual/block/zram0/queue/zoned
/sys/devices/virtual/block/zram0/queue/throttle_sample_time
/sys/devices/virtual/block/zram0/queue/io_poll
/sys/devices/virtual/block/zram0/queue/discard_zeroes_data
/sys/devices/virtual/block/zram0/queue/minimum_io_size
/sys/devices/virtual/block/zram0/queue/nr_zones
/sys/devices/virtual/block/zram0/queue/write_same_max_bytes
/sys/devices/virtual/block/zram0/queue/max_segments
/sys/devices/virtual/block/zram0/queue/dax
/sys/devices/virtual/block/zram0/queue/dma_alignment
/sys/devices/virtual/block/zram0/queue/physical_block_size
/sys/devices/virtual/block/zram0/queue/logical_block_size
/sys/devices/virtual/block/zram0/queue/virt_boundary_mask
/sys/devices/virtual/block/zram0/queue/zone_append_max_bytes
/sys/devices/virtual/block/zram0/queue/write_cache
/sys/devices/virtual/block/zram0/queue/stable_writes
/sys/devices/virtual/block/zram0/queue/max_segment_size
/sys/devices/virtual/block/zram0/queue/rotational
/sys/devices/virtual/block/zram0/queue/discard_max_bytes
/sys/devices/virtual/block/zram0/queue/add_random
/sys/devices/virtual/block/zram0/queue/discard_max_hw_bytes
/sys/devices/virtual/block/zram0/queue/optimal_io_size
/sys/devices/virtual/block/zram0/queue/chunk_sectors
/sys/devices/virtual/block/zram0/queue/read_ahead_kb
/sys/devices/virtual/block/zram0/queue/max_discard_segments
/sys/devices/virtual/block/zram0/queue/write_zeroes_max_bytes
/sys/devices/virtual/block/zram0/queue/nomerges
/sys/devices/virtual/block/zram0/queue/zone_write_granularity
/sys/devices/virtual/block/zram0/queue/fua
/sys/devices/virtual/block/zram0/queue/discard_granularity
/sys/devices/virtual/block/zram0/queue/max_sectors_kb
/sys/devices/virtual/block/zram0/queue/hw_sector_size
/sys/devices/virtual/block/zram0/queue/max_hw_sectors_kb
/sys/devices/virtual/block/zram0/queue/iostats
/sys/devices/virtual/block/zram0/size
/sys/devices/virtual/block/zram0/disksize
/sys/devices/virtual/block/zram0/integrity
/sys/devices/virtual/block/zram0/integrity/write_generate
/sys/devices/virtual/block/zram0/integrity/format
/sys/devices/virtual/block/zram0/integrity/read_verify
/sys/devices/virtual/block/zram0/integrity/tag_size
/sys/devices/virtual/block/zram0/integrity/protection_interval_bytes
/sys/devices/virtual/block/zram0/integrity/device_is_integrity_capable
/sys/devices/virtual/block/zram0/discard_alignment
/sys/devices/virtual/block/zram0/subsystem
/sys/devices/virtual/block/zram0/trace
/sys/devices/virtual/block/zram0/trace/end_lba
/sys/devices/virtual/block/zram0/trace/act_mask
/sys/devices/virtual/block/zram0/trace/start_lba
/sys/devices/virtual/block/zram0/trace/enable
/sys/devices/virtual/block/zram0/trace/pid
/sys/devices/virtual/block/zram0/io_stat
/sys/devices/virtual/block/zram0/max_comp_streams
/sys/devices/virtual/block/zram0/recomp_algorithm
/sys/devices/virtual/block/zram0/capability
/sys/devices/virtual/block/zram0/bdi
/sys/devices/virtual/block/zram0/hidden
/sys/devices/virtual/block/zram0/debug_stat
/sys/devices/virtual/block/zram0/removable
/sys/devices/virtual/block/zram0/idle
/sys/devices/virtual/block/zram0/initstate
/sys/devices/virtual/block/zram0/events
/sys/devices/virtual/block/zram0/inflight
/sys/devices/virtual/block/zram0/slaves
/sys/fs/cgroup/system.slice/dev-zram0.swap
/sys/fs/cgroup/system.slice/dev-zram0.swap/misc.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.latency
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.prio.class
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.pressure
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.cpus.exclusive.effective
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.procs
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.events.local
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.swap.peak
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.swap.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/misc.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.cpus.exclusive
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.swap.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.zswap.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.weight
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.swap.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.max.descendants
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.weight.nice
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.pressure
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/pids.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/pids.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.low
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.pressure
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.type
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.bfq.weight
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.events.local
/sys/fs/cgroup/system.slice/dev-zram0.swap/rdma.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.swap.high
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.low
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.rsvd.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.idle
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.stat.local
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.rsvd.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/rdma.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.threads
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.numa_stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.kill
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.rsvd.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.peak
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.cpus.partition
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.cpus.effective
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.freeze
/sys/fs/cgroup/system.slice/dev-zram0.swap/irq.pressure
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.numa_stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.min
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.max.burst
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.controllers
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.numa_stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.events.local
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.oom.group
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.zswap.writeback
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.uclamp.min
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.mems
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.high
/sys/fs/cgroup/system.slice/dev-zram0.swap/pids.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.zswap.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/misc.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.mems.effective
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.subtree_control
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.events
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.1GB.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.rsvd.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.weight
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpuset.cpus
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.reclaim
/sys/fs/cgroup/system.slice/dev-zram0.swap/pids.peak
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.max.depth
/sys/fs/cgroup/system.slice/dev-zram0.swap/cgroup.pressure
/sys/fs/cgroup/system.slice/dev-zram0.swap/io.stat
/sys/fs/cgroup/system.slice/dev-zram0.swap/cpu.uclamp.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/hugetlb.2MB.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/misc.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.latency
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.prio.class
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.pressure
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.cpus.exclusive.effective
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.procs
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.events.local
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.swap.peak
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.swap.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/misc.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.cpus.exclusive
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.swap.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.weight
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.swap.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.max.descendants
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.weight.nice
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.pressure
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/pids.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/pids.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.low
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.pressure
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.type
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.bfq.weight
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.events.local
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/rdma.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.swap.high
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.low
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.rsvd.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.idle
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.stat.local
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.rsvd.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/rdma.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.threads
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.numa_stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.kill
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.rsvd.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.peak
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.cpus.partition
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.cpus.effective
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.freeze
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/irq.pressure
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.numa_stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.min
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.max.burst
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.controllers
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.numa_stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.events.local
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.oom.group
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.uclamp.min
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.mems
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.high
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/pids.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/misc.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.mems.effective
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.subtree_control
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.events
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.1GB.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.rsvd.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.weight
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpuset.cpus
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.reclaim
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/pids.peak
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.max.depth
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cgroup.pressure
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/io.stat
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/cpu.uclamp.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/hugetlb.2MB.max
/sys/block/zram0
/sys/module/zram
/sys/module/zram/initsize
/sys/module/zram/uevent
/sys/module/zram/notes
/sys/module/zram/notes/.note.Linux
/sys/module/zram/notes/.note.gnu.build-id
/sys/module/zram/notes/.note.gnu.property
/sys/module/zram/taint
/sys/module/zram/srcversion
/sys/module/zram/holders
/sys/module/zram/refcnt
/sys/module/zram/coresize
/sys/module/zram/initstate
/sys/module/zram/sections
/sys/module/zram/sections/__patchable_function_entries
/sys/module/zram/sections/.orc_unwind
/sys/module/zram/sections/__param
/sys/module/zram/sections/.ibt_endbr_seal
/sys/module/zram/sections/.printk_index
/sys/module/zram/sections/.note.Linux
/sys/module/zram/sections/.static_call_sites
/sys/module/zram/sections/.strtab
/sys/module/zram/sections/__mcount_loc
/sys/module/zram/sections/.exit.text
/sys/module/zram/sections/.exit.data
/sys/module/zram/sections/.bss
/sys/module/zram/sections/.orc_unwind_ip
/sys/module/zram/sections/.return_sites
/sys/module/zram/sections/.gnu.linkonce.this_module
/sys/module/zram/sections/.symtab
/sys/module/zram/sections/.rodata
/sys/module/zram/sections/.init.text
/sys/module/zram/sections/.note.gnu.build-id
/sys/module/zram/sections/.text
/sys/module/zram/sections/.init.data
/sys/module/zram/sections/.call_sites
/sys/module/zram/sections/.data
/sys/module/zram/sections/.smp_locks
/sys/module/zram/sections/__bug_table
/sys/module/zram/sections/.rodata.str1.1
/sys/module/zram/sections/.note.gnu.property
/sys/module/zram/sections/.orc_header
/sys/module/zram/sections/.rodata.str1.8
/usr/share/licenses/zram-generator
/usr/share/licenses/zram-generator/LICENSE
/usr/share/man/man5/zram-generator.conf.5.gz
/usr/share/man/man8/zramctl.8.gz
/usr/share/man/man8/zram-generator.8.gz
/usr/share/doc/zram-generator
/usr/share/doc/zram-generator/zram-generator.conf.example
/usr/share/bash-completion/completions/zramctl
/usr/bin/zramctl
/usr/lib/systemd/system/systemd-zram-setup@.service
/usr/lib/systemd/system-generators/zram-generator
/usr/lib/modules/6.8.4-arch1-1/kernel/drivers/block/zram
/usr/lib/modules/6.8.4-arch1-1/kernel/drivers/block/zram/zram.ko.zst
/usr/lib/modules/6.8.4-arch1-1/build/drivers/block/zram
/usr/lib/modules/6.8.4-arch1-1/build/drivers/block/zram/Kconfig
```
Also looking for `zswap` files (look it up on the Arch wiki...) in a similar way to configure that:
```
/sys/fs/cgroup/sys-fs-fuse-connections.mount/memory.zswap.current
/sys/fs/cgroup/sys-fs-fuse-connections.mount/memory.zswap.writeback
/sys/fs/cgroup/sys-fs-fuse-connections.mount/memory.zswap.max
/sys/fs/cgroup/sys-kernel-config.mount/memory.zswap.current
/sys/fs/cgroup/sys-kernel-config.mount/memory.zswap.writeback
/sys/fs/cgroup/sys-kernel-config.mount/memory.zswap.max
/sys/fs/cgroup/sys-kernel-debug.mount/memory.zswap.current
/sys/fs/cgroup/sys-kernel-debug.mount/memory.zswap.writeback
/sys/fs/cgroup/sys-kernel-debug.mount/memory.zswap.max
/sys/fs/cgroup/dev-mqueue.mount/memory.zswap.current
/sys/fs/cgroup/dev-mqueue.mount/memory.zswap.writeback
/sys/fs/cgroup/dev-mqueue.mount/memory.zswap.max
/sys/fs/cgroup/user.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-permission-store.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-permission-store.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-permission-store.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/dbus-broker.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/dbus-broker.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/dbus-broker.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-document-portal.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-document-portal.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-document-portal.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-desktop-portal.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-desktop-portal.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/xdg-desktop-portal.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-ksmserver.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-ksmserver.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-ksmserver.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/pipewire-pulse.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/pipewire-pulse.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/pipewire-pulse.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-kwin_wayland.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-kwin_wayland.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-kwin_wayland.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/wireplumber.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/wireplumber.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/wireplumber.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-kded6.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-kded6.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-kded6.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-xdg-desktop-portal-kde.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-xdg-desktop-portal-kde.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-xdg-desktop-portal-kde.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/at-spi-dbus-bus.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/at-spi-dbus-bus.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/at-spi-dbus-bus.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/pipewire.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/pipewire.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/pipewire.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-kactivitymanagerd.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-kactivitymanagerd.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-kactivitymanagerd.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-polkit-agent.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-polkit-agent.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-polkit-agent.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-xembedsniproxy.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-xembedsniproxy.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-xembedsniproxy.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-ksystemstats.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-ksystemstats.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-ksystemstats.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-baloorunner.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-baloorunner.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-baloorunner.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-gmenudbusmenuproxy.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-gmenudbusmenuproxy.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-gmenudbusmenuproxy.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-krunner.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-krunner.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-krunner.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-powerdevil.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-powerdevil.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/plasma-powerdevil.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/kde-baloo.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/kde-baloo.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/background.slice/kde-baloo.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/docker-0d87b50f14a904e7129eba1dd65ec83488d4e74b9349fc01dbdf808c7f532f03.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/docker-0d87b50f14a904e7129eba1dd65ec83488d4e74b9349fc01dbdf808c7f532f03.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/docker-0d87b50f14a904e7129eba1dd65ec83488d4e74b9349fc01dbdf808c7f532f03.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/docker-fad9e7fda659446a395e26afe8c3fa62600c75760588f7c4f4662fc5ec53a766.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/docker-fad9e7fda659446a395e26afe8c3fa62600c75760588f7c4f4662fc5ec53a766.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/docker-fad9e7fda659446a395e26afe8c3fa62600c75760588f7c4f4662fc5ec53a766.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/user.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-3250211.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-3250211.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-3250211.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.plasma\x2dsystemmonitor-ee71bda014c045d0a906997e9c95e989.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.plasma\x2dsystemmonitor-ee71bda014c045d0a906997e9c95e989.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.plasma\x2dsystemmonitor-ee71bda014c045d0a906997e9c95e989.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.gnome.Geary.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.gnome.Geary.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.gnome.Geary.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-f69f45e747414d8e854bac8a34d37993.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-f69f45e747414d8e854bac8a34d37993.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-f69f45e747414d8e854bac8a34d37993.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.freedesktop.Akonadi.Control.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.freedesktop.Akonadi.Control.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.freedesktop.Akonadi.Control.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.68\x2dorg.a11y.atspi.Registry.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.68\x2dorg.a11y.atspi.Registry.slice/dbus-:1.68-org.a11y.atspi.Registry@0.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.68\x2dorg.a11y.atspi.Registry.slice/dbus-:1.68-org.a11y.atspi.Registry@0.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.68\x2dorg.a11y.atspi.Registry.slice/dbus-:1.68-org.a11y.atspi.Registry@0.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.68\x2dorg.a11y.atspi.Registry.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.68\x2dorg.a11y.atspi.Registry.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.usebottles.bottles-440869.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.usebottles.bottles-440869.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.usebottles.bottles-440869.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-1f87c55e99614844beac40cc17b058cf.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-1f87c55e99614844beac40cc17b058cf.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-1f87c55e99614844beac40cc17b058cf.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.discover.notifier@autostart.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.discover.notifier@autostart.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.discover.notifier@autostart.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-plasmashell-ec46b7633214481395ea58a7e4de020e.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-plasmashell-ec46b7633214481395ea58a7e4de020e.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-plasmashell-ec46b7633214481395ea58a7e4de020e.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-3250552.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-3250552.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-3250552.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/docker.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/docker.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/docker.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-dev.vencord.Vesktop-37773.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-dev.vencord.Vesktop-37773.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-dev.vencord.Vesktop-37773.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-kaccess@autostart.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-kaccess@autostart.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-kaccess@autostart.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kdeconnect.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kdeconnect.slice/dbus-:1.4-org.kde.kdeconnect@0.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kdeconnect.slice/dbus-:1.4-org.kde.kdeconnect@0.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kdeconnect.slice/dbus-:1.4-org.kde.kdeconnect@0.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kdeconnect.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kdeconnect.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-geoclue\x2ddemo\x2dagent@autostart.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-geoclue\x2ddemo\x2dagent@autostart.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-geoclue\x2ddemo\x2dagent@autostart.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-a7376d92ad6348feafbfa257744ea162.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-a7376d92ad6348feafbfa257744ea162.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-a7376d92ad6348feafbfa257744ea162.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.KSplash.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.KSplash.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.KSplash.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.spectacle.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.spectacle.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.spectacle.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-c23a7ac7f43c430596adeb145ae4fcfb.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-c23a7ac7f43c430596adeb145ae4fcfb.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-c23a7ac7f43c430596adeb145ae4fcfb.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kate-6d19521e44de48fd81e0e4dc789ca5be.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kate-6d19521e44de48fd81e0e4dc789ca5be.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kate-6d19521e44de48fd81e0e4dc789ca5be.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dconf.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dconf.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dconf.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kate-29ff91028cb74612b320c9077a516ab7.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kate-29ff91028cb74612b320c9077a516ab7.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kate-29ff91028cb74612b320c9077a516ab7.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dbus.socket/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dbus.socket/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/dbus.socket/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/evolution-source-registry.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/evolution-source-registry.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/evolution-source-registry.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/flatpak-session-helper.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/flatpak-session-helper.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/flatpak-session-helper.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-a937c181162347939f9da239806d3f4f.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-a937c181162347939f9da239806d3f4f.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-a937c181162347939f9da239806d3f4f.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.freedesktop.Notifications.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.freedesktop.Notifications.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.freedesktop.Notifications.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/flatpak-portal.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/flatpak-portal.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/flatpak-portal.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-electron28-34bf7446c22a4b0588f5b349a3bf2b3b.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-electron28-34bf7446c22a4b0588f5b349a3bf2b3b.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-electron28-34bf7446c22a4b0588f5b349a3bf2b3b.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-systemsettings-e1c4d71a7f0b4bb3b680a3f7466122fc.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-systemsettings-e1c4d71a7f0b4bb3b680a3f7466122fc.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-systemsettings-e1c4d71a7f0b4bb3b680a3f7466122fc.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-\x2fhome\x2frohan\x2fPostman\x2fPostman-2c580b13d77649418a5bcc36d7d843fa.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-\x2fhome\x2frohan\x2fPostman\x2fPostman-2c580b13d77649418a5bcc36d7d843fa.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-\x2fhome\x2frohan\x2fPostman\x2fPostman-2c580b13d77649418a5bcc36d7d843fa.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-9cc9d60911194d12994a01908360fd5c.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-9cc9d60911194d12994a01908360fd5c.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.dolphin-9cc9d60911194d12994a01908360fd5c.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dolphin-b56ee24a7ca148ac888b42ec05af508a.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dolphin-b56ee24a7ca148ac888b42ec05af508a.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dolphin-b56ee24a7ca148ac888b42ec05af508a.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-06d101eeedfd4ca899d46f335cafcba1.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-06d101eeedfd4ca899d46f335cafcba1.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-firefox-06d101eeedfd4ca899d46f335cafcba1.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.LogoutPrompt.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.LogoutPrompt.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.LogoutPrompt.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.xfce.Xfconf.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.xfce.Xfconf.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.xfce.Xfconf.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/gpg-agent.service/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/gpg-agent.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/gpg-agent.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.usebottles.bottles-706096.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.usebottles.bottles-706096.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.usebottles.bottles-706096.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kwalletmanager5.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kwalletmanager5.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.kwalletmanager5.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kmail2-72b8049b9b304253b1cbb3a8badae922.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kmail2-72b8049b9b304253b1cbb3a8badae922.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.kde.kmail2-72b8049b9b304253b1cbb3a8badae922.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.fontinst.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.fontinst.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-dbus\x2d:1.4\x2dorg.kde.fontinst.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-dev.vencord.Vesktop-37799.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-dev.vencord.Vesktop-37799.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-dev.vencord.Vesktop-37799.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.raggesilver.BlackBox-403798.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.raggesilver.BlackBox-403798.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.raggesilver.BlackBox-403798.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/init.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/init.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/init.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/session-2.scope/memory.zswap.current
/sys/fs/cgroup/user.slice/user-1000.slice/session-2.scope/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/session-2.scope/memory.zswap.max
/sys/fs/cgroup/user.slice/user-1000.slice/memory.zswap.writeback
/sys/fs/cgroup/user.slice/user-1000.slice/memory.zswap.max
/sys/fs/cgroup/user.slice/memory.zswap.max
/sys/fs/cgroup/sys-kernel-tracing.mount/memory.zswap.current
/sys/fs/cgroup/sys-kernel-tracing.mount/memory.zswap.writeback
/sys/fs/cgroup/sys-kernel-tracing.mount/memory.zswap.max
/sys/fs/cgroup/init.scope/memory.zswap.current
/sys/fs/cgroup/init.scope/memory.zswap.writeback
/sys/fs/cgroup/init.scope/memory.zswap.max
/sys/fs/cgroup/system.slice/var-log.mount/memory.zswap.current
/sys/fs/cgroup/system.slice/var-log.mount/memory.zswap.writeback
/sys/fs/cgroup/system.slice/var-log.mount/memory.zswap.max
/sys/fs/cgroup/system.slice/containerd.service/memory.zswap.current
/sys/fs/cgroup/system.slice/containerd.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/containerd.service/memory.zswap.max
/sys/fs/cgroup/system.slice/systemd-udevd.service/memory.zswap.current
/sys/fs/cgroup/system.slice/systemd-udevd.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/systemd-udevd.service/memory.zswap.max
/sys/fs/cgroup/system.slice/dbus-broker.service/memory.zswap.current
/sys/fs/cgroup/system.slice/dbus-broker.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/dbus-broker.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-drkonqi\x2dcoredump\x2dprocessor.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-drkonqi\x2dcoredump\x2dprocessor.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-drkonqi\x2dcoredump\x2dprocessor.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-gpg\x2dagent.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-gpg\x2dagent.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-gpg\x2dagent.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/boot.mount/memory.zswap.current
/sys/fs/cgroup/system.slice/boot.mount/memory.zswap.writeback
/sys/fs/cgroup/system.slice/boot.mount/memory.zswap.max
/sys/fs/cgroup/system.slice/polkit.service/memory.zswap.current
/sys/fs/cgroup/system.slice/polkit.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/polkit.service/memory.zswap.max
/sys/fs/cgroup/system.slice/rtkit-daemon.service/memory.zswap.current
/sys/fs/cgroup/system.slice/rtkit-daemon.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/rtkit-daemon.service/memory.zswap.max
/sys/fs/cgroup/system.slice/\x2esnapshots.mount/memory.zswap.current
/sys/fs/cgroup/system.slice/\x2esnapshots.mount/memory.zswap.writeback
/sys/fs/cgroup/system.slice/\x2esnapshots.mount/memory.zswap.max
/sys/fs/cgroup/system.slice/home.mount/memory.zswap.current
/sys/fs/cgroup/system.slice/home.mount/memory.zswap.writeback
/sys/fs/cgroup/system.slice/home.mount/memory.zswap.max
/sys/fs/cgroup/system.slice/accounts-daemon.service/memory.zswap.current
/sys/fs/cgroup/system.slice/accounts-daemon.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/accounts-daemon.service/memory.zswap.max
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.zswap.current
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.zswap.writeback
/sys/fs/cgroup/system.slice/dev-zram0.swap/memory.zswap.max
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-systemd\x2dzram\x2dsetup.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/passim.service/memory.zswap.current
/sys/fs/cgroup/system.slice/passim.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/passim.service/memory.zswap.max
/sys/fs/cgroup/system.slice/wpa_supplicant.service/memory.zswap.current
/sys/fs/cgroup/system.slice/wpa_supplicant.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/wpa_supplicant.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-modprobe.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-modprobe.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-modprobe.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.backlighthelper.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.backlighthelper.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.backlighthelper.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/systemd-journald.service/memory.zswap.current
/sys/fs/cgroup/system.slice/systemd-journald.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/systemd-journald.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.chargethresholdhelper.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.chargethresholdhelper.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.chargethresholdhelper.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/fwupd.service/memory.zswap.current
/sys/fs/cgroup/system.slice/fwupd.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/fwupd.service/memory.zswap.max
/sys/fs/cgroup/system.slice/NetworkManager.service/memory.zswap.current
/sys/fs/cgroup/system.slice/NetworkManager.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/NetworkManager.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-systemd\x2dcoredump.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-systemd\x2dcoredump.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-systemd\x2dcoredump.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/flatpak-system-helper.service/memory.zswap.current
/sys/fs/cgroup/system.slice/flatpak-system-helper.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/flatpak-system-helper.service/memory.zswap.max
/sys/fs/cgroup/system.slice/tmp.mount/memory.zswap.current
/sys/fs/cgroup/system.slice/tmp.mount/memory.zswap.writeback
/sys/fs/cgroup/system.slice/tmp.mount/memory.zswap.max
/sys/fs/cgroup/system.slice/systemd-userdbd.service/memory.zswap.current
/sys/fs/cgroup/system.slice/systemd-userdbd.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/systemd-userdbd.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.discretegpuhelper.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.discretegpuhelper.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.powerdevil.discretegpuhelper.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-dirmngr.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-dirmngr.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dirmngr.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.kded.smart.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.kded.smart.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.kded.smart.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/upower.service/memory.zswap.current
/sys/fs/cgroup/system.slice/upower.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/upower.service/memory.zswap.max
/sys/fs/cgroup/system.slice/sddm.service/memory.zswap.current
/sys/fs/cgroup/system.slice/sddm.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/sddm.service/memory.zswap.max
/sys/fs/cgroup/system.slice/var-cache-pacman-pkg.mount/memory.zswap.current
/sys/fs/cgroup/system.slice/var-cache-pacman-pkg.mount/memory.zswap.writeback
/sys/fs/cgroup/system.slice/var-cache-pacman-pkg.mount/memory.zswap.max
/sys/fs/cgroup/system.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.kinfocenter.dmidecode.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.kinfocenter.dmidecode.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-dbus\x2d:1.2\x2dorg.kde.kinfocenter.dmidecode.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/udisks2.service/memory.zswap.current
/sys/fs/cgroup/system.slice/udisks2.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/udisks2.service/memory.zswap.max
/sys/fs/cgroup/system.slice/systemd-timesyncd.service/memory.zswap.current
/sys/fs/cgroup/system.slice/systemd-timesyncd.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/systemd-timesyncd.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dbrowser.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dbrowser.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dbrowser.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-getty.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-getty.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-getty.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dextra.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dextra.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dextra.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/system-keyboxd.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-keyboxd.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-keyboxd.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/avahi-daemon.service/memory.zswap.current
/sys/fs/cgroup/system.slice/avahi-daemon.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/avahi-daemon.service/memory.zswap.max
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dssh.slice/memory.zswap.current
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dssh.slice/memory.zswap.writeback
/sys/fs/cgroup/system.slice/system-gpg\x2dagent\x2dssh.slice/memory.zswap.max
/sys/fs/cgroup/system.slice/systemd-logind.service/memory.zswap.current
/sys/fs/cgroup/system.slice/systemd-logind.service/memory.zswap.writeback
/sys/fs/cgroup/system.slice/systemd-logind.service/memory.zswap.max
/sys/fs/cgroup/proc-sys-fs-binfmt_misc.mount/memory.zswap.current
/sys/fs/cgroup/proc-sys-fs-binfmt_misc.mount/memory.zswap.writeback
/sys/fs/cgroup/proc-sys-fs-binfmt_misc.mount/memory.zswap.max
/sys/fs/cgroup/memory.zswap.writeback
/sys/fs/cgroup/dev-hugepages.mount/memory.zswap.current
/sys/fs/cgroup/dev-hugepages.mount/memory.zswap.writeback
/sys/fs/cgroup/dev-hugepages.mount/memory.zswap.max
/sys/module/zswap
/sys/module/zswap/uevent
/sys/module/zswap/parameters
/sys/module/zswap/parameters/same_filled_pages_enabled
/sys/module/zswap/parameters/enabled
/sys/module/zswap/parameters/shrinker_enabled
/sys/module/zswap/parameters/max_pool_percent
/sys/module/zswap/parameters/compressor
/sys/module/zswap/parameters/non_same_filled_pages_enabled
/sys/module/zswap/parameters/zpool
/sys/module/zswap/parameters/exclusive_loads
/sys/module/zswap/parameters/accept_threshold_percent
/usr/lib/modules/6.8.4-arch1-1/build/include/linux/zswap.h
```
However, looking at the `/proc/cmdline` file on my system, thr `zswap` feature seems to be disabled with the `zswap.enabled=0` kernel parameter...

zram configuration file: `/etc/systemd/zram-generator.conf` \

## Linux swappiness
`vm.swappiness` kernel parameter delegates between prioritizing freeing up anonymous (stack/heap) memory or
file pages from RAM! 
https://www.howtogeek.com/449691/what-is-swapiness-on-linux-and-how-to-change-it/ \
Set the `vm.swappiness` value in the bootloader config to change it!
Value of 100 completely balances the priority\
Virtual file system (VFS): https://www.usenix.org/legacy/publications/library/proceedings/usenix01/full_papers/kroeger/kroeger_html/node8.html

## Disk partitioning and memory swap setup
Linux filesystem type uuid in GPT (partition table scheme that's better than MBR):\
`0FC63DAF-8483-4772-8E79-3D69D8477DE4`

Result of running `fdisk -l /dev/nvme0n1` on my system:
```
Disk /dev/nvme0n1: 1.82 TiB, 2000398934016 bytes, 3907029168 sectors
Disk model: Samsung SSD 990 PRO with Heatsink 2TB   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 98B655AF-F448-42E0-95A7-EFB7568C9B62

Device           Start        End    Sectors  Size Type
/dev/nvme0n1p1    2048    1050623    1048576  512M EFI System
/dev/nvme0n1p2 1050624 3907026943 3905976320  1.8T Linux filesystem
```

New storage partition endpoint: 3222276096 (each sector is 512 bytes, and 512 * value = 1.5 TiB (1.5 * 1024^4 bytes))

swap partition type: `0657FD6D-A4AB-43C4-84E5-0933C84B4F4F` (type 19 in GPT paroitition scheme with fdisk)

`lsblk` - for listing block devices\
`blkid` - to listing block device id's
`fdisk -l` - for inpecting disks and parititions, and `fdisk <dev>` for partitioning disks
parted - another interface for parititoning disks (though fdisk is better since it doesn't immediately write changes to the disk)\
`cryptsetup` - utility for working with LUKS-encrypted partitions
`mkswap` - utility for creating swap file system (assigns new UUID to device, and can assign labels! See Arch wiki page for"persistent dblock device naming")

New /dev/nvme0n1p3 swap partition:\
UUID=`364f2c1a-e241-425b-ac75-b96a4f6a3ea7`\
PARTUUID=`364f2c1a-e241-425b-ac75-b96a4f6a3ea7`\
LABEL=`SWAP`\
Can also find all these persistent name mappings under `/dev/disk/by-*` with a bunch of symlinks!\
See: https://wiki.archlinux.org/title/persistent_block_device_naming

PROCEDURE FOR MOUNTING A SWAP PARTITION:\
FIRST CREATE A PARTITION using `fdisk <disk>` WITH THE "Linux swap" filesystem type (nothing too special about it...) \
THEN
```sh
$ sudo mkswap /dev/<disk>
$ sudo swapon --label=LABEL /dev/<disk>
```
THEN FINALLY ADD A NEW ENTRY TO `/etc/fstab` AS FOLLOWS:
```
LABEL=LABEL none  swap  defaults,pri=<number> 0 0
```
YOU CAN DISABLE/UNMOUNT THE SWAP PARTITION USING `swapoff`

TO CREATE A SWAP FILE IN BTRFS, EXECUTE THE FOLLOWING
```sh
$ sudo truncate -s 0 /swapfile # Create empty file at root
$ sudo chattr +C /swapfile # No Copy-on-Write (COW) permission, e.g. for subvolume snapshots
$ sudo chmod 0600 /swapfile # Set permissions
$ sudo fallocate -l <size> /swapfile # Set swapfile size
$ sudo mkswap /swapfile # Create the proper swapfile type
$ sudo swapon /swapfile # Mount the swapfile
```
THEN TO MAKE IT MOUNT AFTER REBOOT, ADD THE FOLLOWING TO the end of `/etc/fstab` (columns separated by tabs)
```
/swapfile none  swap  defaults,pri=100  0 0
```
TO DISABLE THE SWAPFILE, USE `swapoff`\
USE `swapon -s` or `free -h` to display swap usage stats!

## Setting up hibernation in Arch
Finally, to use this swapfile (or any swap partition) for hibernating
* First get the btrfs disk offset for swap files using
  ```sh
  $ btrfs inspect-internal map-swapfile -r /swapfile # See btrfs online docs for more info
  ```
  Then write this offset using `echo <offset> | sudo tee /sys/power/resume_offset`
* Then add the following as kernel parameters to the `/boot/loader/entries/*.conf` boot
  config file at the end of the `options` line
  ```
  resume=/dev/<device> resume_offset=<offset>
  ```
  NOTE: resume_offset is NOT REQUIRED for swap partitions (just set the `resume` option to partition device, e.g. `/dev/nvme0n1p3`)\
  NOTE: for swap files, `resume` contains the block device (under `/dev`) for the file system containing the swap file
* You also MUST add the `resume` hook to the HOOKS listing in the `/etc/mkinitcpio.conf` initramfs image config file 
  (which is pretty much just like a Dockerfile for initramfs/early user space images -- also, as aside, `cpio` is a compression scheme). 
  Then rebuild the initramfs image(s) using `sudo mkinitcpio -P`
* FINALLY, to hibernate immediately by shutting down and commit the kernel changes, write the swap file root filesystem (or swap partition) 
  device location to `/sys/power/resume` by invoking the following: \
  For example, in btrfs, the root filesystem device for a LUKS encrypted partition is given by `/dev/mapper/root`
  ```
  $ echo /dev/<device> | sudo tee /sys/power/resume
  $ echo shutdown | sudo tee /sys/power/disk
  $ echo disk | sudo tee /sys/power/state
  ```
* You can also modify the /etc/systemd/sleep.conf config file and invoke hibernation (in a safer way) using
  ```sh
  $ sudo systemctl hibernate
  ```
  See https://wiki.archlinux.org/title/Power_management/Suspend_and_hibernate and https://man.archlinux.org/man/systemd-sleep.8 for full details

`dmidecode --type 17` -- list memory (RAM) specs

`/usr/lib/initcpio/` -> contains `initramfs` hook run and build scripts!! This is how disk decryption occcurs using the `encrypt` hook!\
`/etc/mkinitcpio.conf` -> specifies the resources included in the `initramfs` file which is mounted as an early user space tmpfs/ramfs type filesystem in RAM 
so the necessary setup steps can occur, such as decrypting the disk and resuming from the hibernation image!

## Kernel parameters and Disk/filesystem stats
`sysctl` - set and probe kernel parameters\
`systemctl (for systemd)` - manage system services/daemons launched during `init` late in the boot process, when the main userspace is spawned\
`modprobe` - hotload and probe kernel modules (such as zram/zswap) while the systerm is running

`filefrag` - list fragmentation status and diswk offset of a given file\
`btrfs` - utility for creating and managing btrfs-formatted file systems\
`dmsetup` - Linux utility for creating and managing logical block devices that can fuse multiple physical volumes together! Underlies the LVM technology!
          Kernel feature known as "disk mapping". Pretty darn cool! Used for secure encrypted disk I/O using the Linux kernel's Crypto API too!\
          Learn more: https://man7.org/linux/man-pages/man8/dmsetup.8.html\
          Think of disk mapping as making a block device that communicates with (multiple) other devices, while also possibly encrypting/decrypting data!
          For axample, you can make a linear mapping to two other drives that appear under one block device interface! Really neat!
          Use `dmsetup` to query about the status of the virtual block devices created that map to other storage devices!

## Block/character special files
Block and character special *device* files can be created using `mknod` and are special buffered (block) or unbuffered (character) 
interfaces to physical devices, which are interfaced with using device drivers loaded in by the kernel, with the device files created under 
`/dev` by `udev` and attached during boot to the correct drivers according to the device's major number! 
Every device file has a major (which designates the device type) and minor (which deignates different devices under the same major number/driver) 
number, which can be used to uniquely identify the device (e.g., 259:2 for /dev/nvme0n1p2)! 
See https://www.kernel.org/doc/Documentation/admin-guide/devices.txt for an exhuastive device numbers reference.
`ls -l` can be used to obtain device types and numbers, for example:
```
crw-rw----+ 1 root video 226, 1 Apr 15 06:39 /dev/dri/card1
```
The first character in the first column indicates character (c) or block (b) special
The comma separated values represent the major:minor numbers 
(e.g. 226:1 for the device above, which designates rendering infrastructure)
`udev` is the main daemon for handling device events, and `udevadm` is the utility for interfacing with `udev`
https://man7.org/linux/man-pages/man7/udev.7.html\
All `/devices/**` paths returned by `udevadm info /dev/<dev>` for some device are under the `/sys/` sysfs Linux interface!
The `/sys/devices` path contains configured parameters for different devices (like all kernel paramters are under `/sys/kernel` 
with a different file for each ending parameter the intermediary values being directories, e.g. `net.io.speed` is stored in `/sys/kernel/net/io/speed`).
Use `udefadm info -a` to traverse the parameter tree for a given device.
Device rule files are located under `/lib/udev` among other locations...\
NOTE: `/dev/nvme0` is the NVMe *memory controller* that communicates over PCIem while `/dev/nvme0n1` is the actual NVMe drive! Then `/dev/nvme0n1p<n>` is the n'th partition!

## Disk encryption
`cryptsetup` - used to encrypt/decrypt LUKS devices using the kernel feature, and invokes `dmsetup` to create the necessary logical (virtual)
             block device mapping under `/dev/mapper` to the decrypted disk volume, so that data is encrypted/decrypted while *passing through* the block device as handled (and buffered) by the configured Linux kernel driver!
             This means that the disk is never actually fully decrypted and exposed, but rather the virtual mapping is made so the disk is accessible and 
             encryption/decryption of data is done on the fly using the Linux kernel's Crypto API as the user reads and write to the disk!
             Learn more: https://man7.org/linux/man-pages/man8/cryptsetup.8.html, https://en.wikipedia.org/wiki/Device_mapper\
             Think of `cryptsetup` as LUKS functionality for the `dmutil` "crypt" target (aka dm-crypt)!
             Use `cryptsetup` to get information about the *still encrypted* volume device, and `dmutil` to get information about the virtual block device!
             `cryptsetup` encrypts the drives themselves, allows for creating the password, specifies the proper crypt target and table spec for creating the block device with `dmsetup`, etc.,
             while `dmutil` just provides a virtual device interface for communicating with the encrypted volume in a secure way according the the encryption method.

NOTE: Device files _don't_ actually take up space on the system! They are like named pipes, just there to interface with the physical/virtual devices!

Something interesting:\
Try to create the virtual block device mapping from the encrypted `/dev/nvme0n1p2` partition device (using `cryptsetup open /dev/nvme0n1p2 root`),
which will create the mapping on `/dev/mapper/root`, which is symlinked to the actual `/dev/dm-0` virtual block device file. Then use 
`dmsetup table /dev/mapper/root` to get the following output:
```
0 3221192705 crypt aes-xts-plain64 :64:logon:cryptsetup:8c018527-ba92-43eb-9b1d-8508ec7c43d5-d0 0 259:2 32768
```
The second value minus the first gives the number of sectors writable on the block device, starting from volume sector
32768, in the count of 512 byte sectors. Hence multiplying the difference by 512 gives the total number of writable bytes on the volume.
Now, use `btrfs inspect-internal dump-super /dev/mapper/root` top get the following output of the device's _superblock_ (basically the main filesystem header -- learn more: https://archive.kernel.org/oldwiki/btrfs.wiki.kernel.org/index.php/On-disk_Format.html):
```
superblock: bytenr=65536, device=/dev/mapper/root
---------------------------------------------------------
csum_type               0 (crc32c)
csum_size               4
csum                    0x3cfa606c [match]
bytenr                  65536
flags                   0x1
                        ( WRITTEN )
magic                   _BHRfS_M [match]
fsid                    c754e01e-710e-413d-bdc3-307abb4545c6
metadata_uuid           00000000-0000-0000-0000-000000000000
label
generation              19309
root                    814055424
sys_array_size          129
chunk_root_generation   19249
root_level              0
chunk_root              23068672
chunk_root_level        1
log_root                800866304
log_root_transid (deprecated)   0
log_root_level          0
total_bytes             1649267441664
bytes_used              254290964480
sectorsize              4096
nodesize                16384
leafsize (deprecated)   16384
stripesize              4096
root_dir                6
num_devices             1
compat_flags            0x0
compat_ro_flags         0x3
                        ( FREE_SPACE_TREE |
                          FREE_SPACE_TREE_VALID )
incompat_flags          0x361
                        ( MIXED_BACKREF |
                          BIG_METADATA |
                          EXTENDED_IREF |
                          SKINNY_METADATA |
                          NO_HOLES )
cache_generation        0
uuid_tree_generation    19309
dev_item.uuid           547b5791-e37d-4d95-81ce-79c95bfe3d9f
dev_item.fsid           c754e01e-710e-413d-bdc3-307abb4545c6 [match]
dev_item.type           0
dev_item.total_bytes    1649267441664
dev_item.bytes_used     263091912704
dev_item.io_align       4096
dev_item.io_width       4096
dev_item.sector_size    4096
dev_item.devid          1
dev_item.dev_group      0
dev_item.seek_speed     0
dev_item.bandwidth      0
dev_item.generation     0
```
and take note of the `dev_item.total_bytes` value. This is the total size, in bytes, the file system, and notice how this is bigger from the product found above, and by exactly 32767 bytes. This is 
because the writable area for filesystem on the volume starts at sector 32768, _after_ the 32757 byte security header generated for the 
filesystem by `cryptsecret` when the filesystem was first generated and encrypted!
Now, because of this, if the `/dev/mapper/root` device were to be mounted using `mount /dev/mapper/root /mnt`, or inspected using 
`btrfs check --force /dev/mapper/root` (--force is needed for a mounted filesystem), the error 
```
block device size is smaller than total_bytes in device item, has 1649250664960 expect >= 1649267441664
```
is generated. However, this is okay and the device is not misaligned with the partition's filesystem area! It's simply because of the way `cryptsetup`
sets the partition up with where it writes the file system that this happens, and the allocated block device is set up to start writing/reading encrypted data at the sector where the
filesystem begins, and the security header (containing the encryption key) is written along with the filesystem.

## Git commit signing using `gpg` and how key pairs work
Sign and verify commit signatures using git:\
https://medium.com/@petehouston/quick-guide-to-sign-your-git-commits-c11ce58c22e9 \
https://www.cloudwithchris.com/blog/gpg-git-part-2/ \
All about subkeys!: https://wiki.debian.org/Subkeys \
Use `gpg` for creating code-signing keys/sub-keys that you can then publish to the ubuntu keyshare and add to GitHub! Private sub-keys are used for signing/decryption, while the primary key is only ever used for making _major_ changes to the keypair, like changing the password. \
All you have to do is generate a signing key-pair on the machine using `gpg`, then add the _public_ key in ASCII-armor format (given by `gpg --armor --export <keyid>`) to your GitHub profile! You
then just tell your local `git` install to sign your commits using your _private_ key by setting `git config --global user.signingkey=<keyid>` and then telling `git` to use
your local `gpg` install for signing with `git config --global gpg.program=$(which gpg)`.\
Also, if there's an error like `gpg: signing failed: Inappropriate ioctl for device` while committing, run `export GPG_TTY=$(tty)` and add it to `~/.bashrc`.\
See https://docs.github.com/en/authentication/managing-commit-signature-verification \
You _encrypt_ the message that's _sent_ with the recipient's _public_ key, and then the recipient _decrypts_ it with their _private_ key. And you _verify_ the data that's _received_ with the sender's _public_ key, which they _sign_ using their _private_ key. Take sending and receiving data from your account on GitHub for instance. First you add your SSH _public_ key to your GitHub profile. Then when receiving data over SSH for the first time from GitHub, their _public_ key is given to you. Then you can _verify_ that the data indeed came from GitHub using their _public_ key and, you can _decrypt_ the data using your _private_ key, which they _encrypted_ using your _public_ key and _signed_ using their _private_ key! In the opposite direction, when _sending_ data to GitHub, you _encrypt_ it using GitHub's _public_ key and _sign_ it using your _private_ key, and then they can only _decrypt_ it using their _private_ key (so you can be sure that only GitHub can read the data) and they _verify_ that it came from you using your _public_ key! Notice that GitHub _only_ needs your public key and you _only_ need their public key for this all to work, and the private key never leaves the owner's possession! Look at `~/.ssh/known_hosts` for GitHub's public keys. This is pretty much how _any_ communication over SSH takes place, where you place your public key on the server and you place their's in `~/.ssh/known_hosts`!\
Separating SSH and GPG keys this way ensures that even if someone else manages to get ahold of your SSH private key and can access your account, the commit would still show up as unverified if they don't also have one of your private GPG sub-keys, which you can easily deactivate and regenerate from your primary private key if it were also compromised.\
You can also publish your public GPG keys on online keyshares such as `https://keyserver.ubuntu.com/` so others can easily find them! Use `gpg --send-keys <keyid>` to do this. You can also search for keys on the keyservers by going to the website or using `gpg --search-keys <url> <search string>`. \
Key servers: https://en.wikipedia.org/wiki/Key_server_(cryptographic)

## Modifying `sudo` and `PAM` behavior
Configure `sudo` behavior using `/etc/sudoers` file with the "Defaults" directive: https://www.sudo.ws/docs/man/sudoers.man/#SUDOERS_OPTIONS\
Adding the line `Defaults insults, passwd_tries=5, timestamp_timeout=30` results in some interesting behavior now lol..\
It also makes it so that max 5 attempts (instead of the default 3) are allowed, and user is authenticated for 30 min (instead of default 5)\
NOTE: MODIFY THE /etc/sudoers FILE BY ONLY INVOKING THE FOLLOWING
```sh
$ EDITOR="code -r --no-sandbox --user-data-dir=/.vscode --wait" visudo
```
SINCE A LOCKFILE IS CREATED IN THAT CASE\
Note that `sudo` interally uses Linux PAM (Pluggable Authentication Modules) for authentication, which is a set of kernel
libraries for performing modular authentication (i.e. configuring custom authentication methods for different programs),
with the program configs specified under `/etc/pam.d/`. In particular, the `/etc/pam.d/sudo` file specifies the configration
for `sudo`, which itself just derives from the built-in `/etc/pam.d/system-auth` default auth scheme. In short, PAM works by invoking
different modules (really compiled C object files) with certain option arguments for handling different parts of the auth flow 
(learn more: https://man.archlinux.org/man/core/pam/PAM.8.en).\
Take note of the `pam_faillock.so` module in particular, which 
handles whether the user is rejected after authentication is attempted: how this is handled is configured in `/etc/security/faillock.conf`,
which specifies all the options that could also be passed when the module is invoked, such as the max no. of authentication attempts before
rejection, and the (irritiating) lockout period for the user after the max allowed attempts is reached. (NOTE: Modifying this file will be effective
immediately since `faillock.so` isn't really a running daemon/service but a program that's invoked which reads the config).
The interesting bit is how the lockout period and other options seem to have an immediate effect on `sudo` usage, yet changing the max number of
attempts allowed doesn't seem to change anything. This is because this is overridden by `sudo` itself, and the option in `/etc/security/faillock.conf`
just sets the default for _all_ programs that don't override it! Therefore, to change the max number of attempts, you must modify the `sudoers` file
using `visudo`, but all other (tested) behavior can be changed in `faillock.conf`.\
LEARN MORE: https://man.archlinux.org/man/core/pam/faillock.conf.5.en\
NOTE: The `faillock` command line utility can be used to reset the current user's failed attempts (tracked in `/var/run/faillock/<user>`) using `faillock --reset` 
thereby bypassing the lockout. Also, `sudo -k` can be used toi reset the current user's root auth status (so they have to enter their password on the next usage)

## Using the Arch User Repository (AUR)
Download and install packages from source on ARCH from the AUR using PKGBUILD files: https://wiki.archlinux.org/title/Arch_User_Repository \
Simply clone the repo, `cd` into it, then run `make -sic` to build and install the package! Just be sure to VET the repo thoroughly though
since it's all user contributed stuff and not at all verified for security! Look through the PKGBUILD file, consider the
popularity of the package, look through comments, look at how recent the latest update was, etc...There are also helpers made for this process, such as `yay`, but they're really not needed...

## Querying GPU/CPU stats
Use `radeontop` or `nvtop` to query status of AMD CPU/GPU hardware (which can be installed using the main `pacman -S` package manager in Arch)