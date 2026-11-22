#!/bin/sh
# SPDX-License-Identifier: MIT
# Builds the GPU scan. Requires the Vulkan SDK headers, libvulkan and glslc.
set -e
cd "$(dirname "$0")"
glslc -O --target-env=vulkan1.2 bow_draw_block64.comp -o bow_draw_block64.spv
gcc -O2 bow_draw_gpu.c -lvulkan -o bow_draw_gpu
echo built
