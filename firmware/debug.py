import gc
import os
import sys
import machine


# -------------------------------------------------
# Separator
# -------------------------------------------------

def separator():

    print(
        "--------------------------------"
    )


# -------------------------------------------------
# RAM
# -------------------------------------------------

def ram():

    gc.collect()

    free = gc.mem_free()
    allocated = gc.mem_alloc()
    total = free + allocated

    print(
        "RAM free:",
        free,
        "bytes"
    )

    print(
        "RAM used:",
        allocated,
        "bytes"
    )

    print(
        "RAM total:",
        total,
        "bytes"
    )


# -------------------------------------------------
# Files
# -------------------------------------------------

def files(path="/"):

    print(
        "Files in:",
        path
    )

    for filename in os.listdir(path):

        try:

            file_path = (
                path.rstrip("/")
                + "/"
                + filename
            )

            size = os.stat(
                file_path
            )[6]

            print(
                filename,
                "-",
                size,
                "bytes"
            )

        except OSError:

            print(
                filename,
                "- directory"
            )


# -------------------------------------------------
# Flash storage
# -------------------------------------------------

def flash():

    try:

        stats = os.statvfs("/")

        block_size = stats[0]
        total_blocks = stats[2]
        free_blocks = stats[3]

        total = (
            block_size
            * total_blocks
        )

        free = (
            block_size
            * free_blocks
        )

        used = (
            total
            - free
        )

        print(
            "Flash free:",
            free,
            "bytes"
        )

        print(
            "Flash used:",
            used,
            "bytes"
        )

        print(
            "Flash total:",
            total,
            "bytes"
        )

    except Exception as error:

        print(
            "Flash information unavailable:",
            error
        )


# -------------------------------------------------
# System information
# -------------------------------------------------

def system():

    print(
        "MicroPython:",
        sys.implementation
    )

    print(
        "Platform:",
        sys.platform
    )

    print(
        "CPU frequency:",
        machine.freq(),
        "Hz"
    )


# -------------------------------------------------
# Complete information
# -------------------------------------------------

def info():

    separator()

    print(
        "CW Trainer Debug"
    )

    separator()

    ram()

    separator()

    flash()

    separator()

    system()

    separator()